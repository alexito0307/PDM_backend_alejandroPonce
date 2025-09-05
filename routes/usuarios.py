from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from flask_bcrypt import Bcrypt

from config.db import get_db_connection

import os
from dotenv import load_dotenv

# Cargamos las variables de entorno
load_dotenv()

# Creamos el blueprint
usuarios_bp = Blueprint('usuarios', __name__)

# Inicializamos a Bcrypt
bcrypt = Bcrypt()

@usuarios_bp.route('/registrar',methods=['POST'])
def registrar():
  # Obtener del body los datos
  data = request.get_json()

  nombre = data.get('nombre')
  email = data.get('email')
  password = data.get('password')

  #Validacion
  if not nombre or not email or not password:
    return jsonify({"error": "Faltan datos datos"}), 400
  #Obtener el cursor
  cursor = get_db_connection()

  try: 
    # Verificamos que el usuario no exista
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
      return jsonify({"error":"Ese usuario ya existe"}),400
    
    # Hacemos hash al password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Insertar el registro del nuevo usuario en la base de datos
    cursor.execute('''INSERT INTO USUARIOS (nombre, email, password) values (%s,%s,%s)''',
                   (nombre, email, hashed_password,))
    cursor.connection.commit()
    return jsonify({"message": "Usuario creado correctamente"})
  except Exception as e:
    return jsonify({"error":F"Error al registrar al usuario: {str(e)}" })
  finally:
    # Nos aseguramos de cerrar el cursor
    cursor.close()

@usuarios_bp.route('/login', methods=['POST'])
def login():
  data = request.json()

  email = data.get('email')
  password = data.get('password')
  if not email or not password:
    return jsonify({"error": "Faltan datos"}), 400
  cursor = get_db_connection()
  cursor.execute("SELECT ")
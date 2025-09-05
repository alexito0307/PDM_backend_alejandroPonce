from flask import Blueprint, request, jsonify
from config.db import get_db_connection

# Crear el blueprint
tareas_bp = Blueprint('tareas', __name__)

#Crear un endpoint obtener tareas
@tareas_bp.route('/obtener', methods=['GET'])
def get():
  return jsonify({
    "mensaje": "Estas son tus tareas"
  })
# Crear endpoint con post recibiendo datos desd eel body
@tareas_bp.route('/crear', methods=['POST'])
def crear():
  #Obtener los datos del body
  data = request.get_json()
  descripcion = data.get('descripcion')
  if not descripcion:
    return jsonify({"error": "Debes teclear una descripcion"}),400


  # Obtenemos el cursor
  cursor = get_db_connection()

  # Hacemos el insert
  try:
    cursor.execute('INSERT INTO tareas (descripcion) VALUES (%s)', (descripcion,))

    return jsonify({"message":"Tarea creada"}), 201
  except Exception as e:
    return jsonify({"Error": f"No se pudo crear la tarea {e}"}), 400
  finally:
    # Cierro la conexion
    cursor.close()

@tareas_bp.route('/modificar/<int:user_id>', methods=['PUT'])
def modificar(user_id):
  # Obtenemos los datos del body
  data = request.get_json()
  nombre = data.get('nombre')
  apellido = data.get('apellido')

  mensaje = f"Usuario con id: {user_id} y nombre: {nombre} {apellido}"
  return jsonify({"saludo": mensaje})
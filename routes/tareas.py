from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from config.db import get_db_connection


# Crear el blueprint
tareas_bp = Blueprint('tareas', __name__)

#Crear un endpoint obtener tareas
@tareas_bp.route('/obtener', methods=['GET'])
@jwt_required()
def get():
    current_user = get_jwt_identity()

    # get_db_connection YA devuelve un cursor
    cursor = get_db_connection()

    query = """
        SELECT a.id_usuario, a.descripcion, b.nombre, b.email, a.creado_en
        FROM tareas AS a
        INNER JOIN usuarios AS b ON b.id_usuario = a.id_usuario
        WHERE a.id_usuario = %s
    """
    cursor.execute(query, (current_user,))
    lista = cursor.fetchall()
    cursor.close()

    if not lista:
        return jsonify({"error": "El usuario no tiene tareas"}), 404
    return jsonify({"lista": lista}), 200


# Crear endpoint con post recibiendo datos desd eel body
@tareas_bp.route('/crear', methods=['POST'])
@jwt_required()
def crear():
  current_user = get_jwt_identity()
  #Obtener los datos del body
  data = request.get_json()
  descripcion = data.get('descripcion')
  
  if not descripcion:
    return jsonify({"error": "Debes teclear una descripcion"}),400


  # Obtenemos el cursor
  cursor = get_db_connection()

  # Hacemos el insert
  try:
    cursor.execute('INSERT INTO tareas (descripcion, id_usuario) VALUES (%s, %s)', (descripcion, current_user))
    cursor.connection.commit()
    return jsonify({"message":"Tarea creada"}), 201
  except Exception as e:
    return jsonify({"Error": f"No se pudo crear la tarea {e}"}), 400
  finally:
    # Cierro la conexion
    cursor.close()

@tareas_bp.route('/modificar/<int:id_tarea>', methods=['PUT'])
@jwt_required()
def modificar(id_tarea):
  # Obtenemos la identidad del dueño
  current_user = get_jwt_identity()

  # Obtenemos los datos del body
  data = request.get_json()

  # Obtenemos el cursor
  cursor = get_db_connection()

  descripcion = data.get('descripcion')
  if not descripcion:
     return jsonify({"error":"Faltan datos"})
  
  # Verificamos si existe la tarea
  query = " SELECT * FROM tareas WHERE id_tarea = %s "
  cursor.execute(query, (id_tarea,))
  tarea = cursor.fetchone() # tarea = (1,2 ..) 
  if not tarea:
     cursor.close()
     return jsonify({"error": "No existe esa tarea"}), 404
  if not tarea[1] == int(current_user):
     cursor.close()
     return jsonify({"error": "Credenciales incorrectas"}),401
  
  # Actualizar los datos
  try:
     cursor.execute("UPDATE tareas SET descripcion = %s WHERE id_tarea = %s", (descripcion, id_tarea))
     cursor.connection.commit()
     return jsonify({"mensaje": "Tarea actualizada exitosamente"}),200
  except Exception as e:
     return jsonify({"error": f"Error al actualizar los datos: {str(e)}"}),400
  finally:
     cursor.close()

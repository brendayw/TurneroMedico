from flask import Blueprint, jsonify, request
from modelos.pacientes import obtener_pacientes, obtener_paciente_por_id, editar_paciente_por_id, crear_paciente, eliminar_paciente_por_id

#get ppacientes
#get paciente por id
#post paciente nuevo
#put paciente por id
#delete paciente por id

pacientes_bp = Blueprint('pacientes', __name__)

@pacientes_bp.route('/pacientes', methods=['GET'])
def buscar_pacientes():
    pacientes = obtener_pacientes()
    if len(pacientes) > 0:
        return jsonify(pacientes), 200
    else:
        return jsonify({'error': 'No hay pacientes'}), 404
    
@pacientes_bp.route('/pacientes/<int:id>', methods=['GET'])
def buscar_paciente_por_id(id):
    paciente = obtener_paciente_por_id(id)

    if paciente:
        return jsonify(paciente), 200
    else:
        return jsonify({'error': 'No se encontró el paciente'}), 404
    
@pacientes_bp.route('/pacientes', methods=['POST'])
def nuevo_paciente():
    if request.is_json:
        nuevo = request.get_json()
        if 'dni' in nuevo and 'nombre' in nuevo and 'apellido' in nuevo and 'telefono' in nuevo and 'email' in nuevo and 'direccion_calle' in nuevo and 'direccion_numero' in nuevo:
            nuevo_paciente = crear_paciente(nuevo['dni'], nuevo['nombre'], nuevo['apellido'], nuevo['telefono'], nuevo['email'], nuevo['direccion_calle'], nuevo['direccion_numero'])
            return jsonify(nuevo_paciente), 201
        else:
            return jsonify({'error': 'Datos incompletos'}), 400
    else:
        return jsonify({'error': 'La solicitud debe ser en formato JSON'}), 400 

@pacientes_bp.route('/pacientes/<int:id>', methods=['PUT'])
def editar_paciente(id):
    if request.is_json:
        editar = request.get_json()

        if 'dni' in editar and 'nombre' in editar and 'apellido' in editar and 'telefono' in editar and 'email' in editar and 'direccion_calle' in editar and 'direccion_numero' in editar:

            editar_paciente = editar_paciente_por_id(id, editar['dni'], editar['nombre'], editar['apellido'], editar['telefono'], editar['email'], editar['direccion_calle'], editar['direccion_numero'])
            
            if editar_paciente:
                return jsonify(editar_paciente), 200
            else:
                return jsonify({'error': 'No se encontró el paciente'}), 404
        else:
            return jsonify({'error': 'Datos incompletos'}), 400
    else:
        return jsonify({'error': 'La solicitud debe ser en formato JSON'}), 400
    
@pacientes_bp.route('/pacientes/<int:id>', methods=['DELETE'])
def eliminar_paciente(id):
    paciente = eliminar_paciente_por_id(id)
    if paciente:
        return jsonify({'mensaje': 'Paciente eliminado exitosamente'}), 200
    else:
        return jsonify({'error': 'No se encontró el paciente'}), 404

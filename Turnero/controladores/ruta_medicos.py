from flask import Blueprint, jsonify, request
from modelos.medicos import obtener_medicos, obtener_medico_por_id, editar_lista_medicos_por_id, deshabilitar_medico_por_id, crear_medico

#Obtener detalles de un médico por su ID (GET).
#Agregar un nuevo médico (POST).
#Actualizar la información de un médico por su ID (PUT).
#Deshabilitar un médico (PUT). Inhabilitar un médico 
# deberá prohibirle entregar nuevos turnos, pero no 
# influye a los turnos asignados.

medicos_bp = Blueprint('medicos', __name__)

@medicos_bp.route('/medicos', methods=['GET'])
def buscar_medicos():
    medico =  obtener_medicos()
    if len(medico) > 0:
        return jsonify(medico), 200
    else:
        return jsonify({'error': 'No hay medicos'}), 404

@medicos_bp.route('/medicos/<int:id>', methods=['GET'])
def buscar_medico_por_id(id):
    medico = obtener_medico_por_id(id)

    if medico:
        return jsonify(medico), 200
    else:
        return jsonify({'error': 'No se encontró el médico'}), 404

@medicos_bp.route('/medicos', methods=['POST'])
def nuevo_medico():
    if request.is_json:
        nuevo = request.get_json()
        if 'dni' in nuevo and 'nombre' in nuevo and 'apellido' in nuevo and 'matricula' in nuevo and 'telefono' in nuevo and 'email' in nuevo and 'habilitado' in nuevo:
            nuevo_medico = crear_medico(nuevo['dni'], nuevo['nombre'], nuevo['apellido'], nuevo['matricula'], nuevo['telefono'], nuevo['email'], nuevo['habilitado'])
            return jsonify(nuevo_medico), 201
        else:
            return jsonify({'error': 'Datos incompletos'}), 400
    else:
        return jsonify({'error': 'La solicitud debe ser en formato JSON'}), 400

@medicos_bp.route('/medicos/<int:id>', methods=['PUT'])
def editar_medico(id):
    if request.is_json:
        editar = request.get_json()
        if 'dni' in editar and 'nombre' in editar and 'apellido' in editar and 'matricula' in editar and 'telefono' in editar and 'email' in editar and 'habilitado' in editar:
            
            editar_medico = editar_lista_medicos_por_id(id, editar['dni'], editar['nombre'], editar['apellido'], editar['matricula'], editar['telefono'], editar['email'], editar['habilitado'])
            
            if editar_medico:
                return jsonify(editar_medico), 200
            else:
                return jsonify({'error': 'No se encontró el médico'}), 404
        else:
            return jsonify({'error': 'Datos incompletos'}), 400
    else:
        return jsonify({'error': 'La solicitud debe ser en formato JSON'}), 400

@medicos_bp.route('/medicos/<int:id>', methods=['PUT'])
def deshabilitar_medico(id):
    medico = deshabilitar_medico_por_id(id)
    if request.is_json:
        deshabilitar = request.get_json()
        if 'habilitado' in deshabilitar:
            if deshabilitar['habilitado'] == False:
                return jsonify(medico), 200
            else:
                return jsonify({'error': 'Medico no encontrado'}), 404
        else:
            return jsonify({'error': 'Faltan campos'}),400     
    else:
        return jsonify({'error': 'La solicitud debe ser en formato JSON'}), 400             
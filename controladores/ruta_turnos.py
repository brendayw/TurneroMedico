from flask import Blueprint, request, jsonify
from modelos.turnos import obtener_turnos, obtener_turnos_pendientes, obtener_turnos_por_medico, crear_turno, eliminar_turno


turnos_bp = Blueprint('turnos', __name__)

@turnos_bp.route('/turnos', methods=['GET'])
def todos_turnos():
    todos = obtener_turnos()
    if todos:
        return jsonify(todos), 200
    else:
        return jsonify({'error': 'No hay turnos disponibles'}), 404


@turnos_bp.route('/turnos/<int:id>', methods=['GET'])
def buscar_turnos(id):
    turnos_medico = obtener_turnos_por_medico(id)
    if len(turnos_medico) > 0:
        return jsonify(turnos_medico), 200
    else:
        return jsonify({'error': 'no hay turnos'}), 404

@turnos_bp.route('/turnos/pendientes/<int:id>', methods=['GET'])
def buscar_turnos_pendientes(id):
    turnos_pendientes = obtener_turnos_pendientes(id)
    if len (turnos_pendientes) > 0:
        return jsonify(turnos_pendientes), 200
    else:
        return jsonify({'error': 'No hay turnos pendientes para mostrar'}), 404

@turnos_bp.route('/turnos', methods=['POST'])
def crear_turno():
    if request.is_json:
        nuevo = request.get_json()
        if 'id_turno' in nuevo and 'id_medico' in nuevo and 'id_paciente' in nuevo and 'hora_turno' in nuevo and 'fecha_solicitud' in nuevo:
            nuevo = crear_turno(nuevo['id_turno'], nuevo['id_medico'], nuevo['id_paciente'], nuevo['hora_turno'], nuevo['fecha_solicitud'])
            return jsonify(nuevo), 201
        else:
            return jsonify({'error': 'Datos incompletos'}), 400
    else:
        return jsonify({'error': 'La solicitud debe ser en formato JSON'}), 400

@turnos_bp.route('/turnos/<int:id>', methods=['DELETE'])
def eliminar_turno(id):
    turno = eliminar_turno(id)
    if turno:
        return jsonify({'mensaje': 'Turno eliminado exitosamente'}), 200
    else:
        return jsonify({'error': 'No se encontró el turno'}), 404
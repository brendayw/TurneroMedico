from flask import Blueprint, request, jsonify
from modelos.agendamedicos import obtener_horarios_habilitados, cargar_agenda, agregar_horario, modificar_horario, eliminar_dias_de_atencion, ruta_agenda
from modelos.medicos import existe_medico

agendamedicos_bp = Blueprint('agendamedicos', __name__)

#get todos los medicos habilitados
@agendamedicos_bp.route('/agendamedicos', methods=['GET'])
def obtener_agendamedicos():
    agenda_medicos = obtener_horarios_habilitados()
    if len(agenda_medicos) > 0:
        return jsonify(agenda_medicos), 200
    else:
        return jsonify({'error': 'No hay agendas'}), 404

#post agregar nuevo horario y dia
@agendamedicos_bp.route('/agendamedicos/<int:id_medico>', methods=['POST'])
def nuevo_horario(id_medico):
    if request.is_json:
        nuevo = request.get_json()
        if 'id_medico' in nuevo and 'dia_numero' in nuevo and 'hora_inicio' in nuevo and 'hora_fin' in nuevo and 'fecha_actualizacion' in nuevo:
            if existe_medico(nuevo['id_medico']):
                crear_horario = agregar_horario(nuevo['id_medico'], nuevo['dia_numero'], nuevo['hora_inicio'], nuevo['hora_fin'], nuevo['fecha_actualizacion'])
                return jsonify({'mensaje': 'Horario agregado exitosamente'}), 201
            else:
                return jsonify({'error': 'El médico no existe'}), 404
        else:
                return jsonify({'error': 'Datos incompletos'}), 400
    else:
        return jsonify({'error': 'La solicitud no es JSON'}), 400

#editar horario de atencion
@agendamedicos_bp.route('/agendamedicos/<int:id_medico>', methods=['PUT'])
def modificar_horario_route(id_medico):
    data = request.json
    modificaciones = data.get('modificaciones')

    if modificaciones:
        resultado = modificar_horario(id_medico, modificaciones)
        if resultado:
            return jsonify({'mensaje': 'Horario modificado exitosamente'}), 200
        else:
            return jsonify({'error': 'No se pudo modificar el horario'}), 400
    else:
        return jsonify({'error': 'Datos incompletos'}), 400

#eliminar dias de atencion de medico por id
@agendamedicos_bp.route('/agendamedicos/<int:id_medico>', methods=['DELETE'])
def eliminar_dias_de_atencion(id_medico):
    cargar_agenda(ruta_agenda)

    eliminar_dias_de_atencion(id_medico)

    return jsonify({'mensaje': f'Días de atención del medico con id {id_medico} eliminados exitosamente'}), 200
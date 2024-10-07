import os, csv
from datetime import datetime, timedelta
from modelos.agendamedicos import agenda

turnos = []
id_turno = 1
ruta_archivo_turnos = r'C:\Users\Usuario\Downloads\Brenda\Universidad\TUP\1er Año\Programacion2\Turnero\modelos\turnos.csv'

def inicializar_turnos():
    global id_turno
    if os.path.exists(ruta_archivo_turnos):
        importar_datos_desde_csv()

def importar_datos_desde_csv():
    global turnos, id_turno
    turnos = []
    with open(ruta_archivo_turnos, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            fila['id_turno'] = int(fila['id_turno'])
            fila['id_medico'] = int(fila['id_medico'])
            fila['id_paciente'] = int(fila['id_paciente'])
            fila['hora_turno'] = fila['hora_turno']
            fila['fecha_solicitud'] = fila['fecha_solicitud']
            turnos.append(fila)

        if len(turnos) > 0:
            id_turno = turnos[-1]['id_turno'] + 1
        else:
            id_turno = 1

def exportar_a_csv():
    with open(ruta_archivo_turnos, 'w', newline='', encoding='utf-8') as archivo:
        campos = ['id_turno', 'id_medico', 'id_paciente', 'hora_turno', 'fecha_solicitud']
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()

        for turno in turnos:
            escritor.writerow(turno)

def obtener_turnos():
    return turnos

def obtener_turnos_por_medico(id_medico):
    for turno in turnos:
        if turno['id_medico'] == id_medico:
            return turno
    return None

def obtener_turnos_pendientes(id_medico):
    turnos_pendientes = [
        turno for turno in turnos
        if turno['id_medico'] == id_medico and datetime.strptime(turno['fecha_solicitud'], '%Y-%m-%d').date() >= datetime.now().date()    
    ]
    return turnos_pendientes

def crear_turno(id_medico, id_paciente, hora_turno,fecha_solicitud):
    global turnos, id_turno

    fecha_turno = datetime.strptime(fecha_solicitud, '%Y-%m-%d').date()
    hora_turno_obj = datetime.strptime(hora_turno, '%H:%M').time()

    if not (datetime.now().date() <= fecha_turno <= datetime.now().date() + timedelta(days=30)):
        return False, "La fecha del turno debe ser igual o posterior a la fecha actual."
    
    dias_horarios_medico = [horario for horario in agenda if horario['id_medico'] == id_medico and horario['dia_numero'] == fecha_turno.weekday() + 1]
    if not dias_horarios_medico:
        return False, "El médico no tiene horario disponible en la fecha seleccionada."
    
    for dia_horario in dias_horarios_medico:
        hora_inicio = datetime.strptime(dia_horario['hora_inicio'], '%H:%M').time()
        hora_fin = datetime.strptime(dia_horario['hora_fin'], '%H:%M').time()
        if hora_inicio <= hora_turno_obj <= hora_fin:
            break
    else:
        return False, "La hora solicitada está fuera del horario de atención del médico."

    for turno in turnos:
        if turno['id_medico'] == id_medico and turno['hora_turno'] == hora_turno and turno['fecha_solicitud'] == fecha_solicitud:
            return False, "El turno ya está ocupado."
        

    turnos.append({
        'id_turno': id_turno,
        'id_medico': id_medico,
        'id_paciente': id_paciente,
        'hora_turno': hora_turno,
        'fecha_solicitud': fecha_solicitud
    })
    id_turno += 1
    exportar_a_csv()
    return True, "Turno registrado exitosamente."

def eliminar_turno(id_turno):
    global turnos
    turnos = [turno for turno in turnos if turno['id_turno'] != id_turno]
    exportar_a_csv()
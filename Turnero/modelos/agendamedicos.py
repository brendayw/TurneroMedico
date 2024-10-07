import os, csv
from datetime import datetime

agenda = []
ruta_agenda = r'C:\Users\Usuario\Downloads\Brenda\Universidad\TUP\1er Año\Programacion2\Turnero\modelos\agendamedicos.csv'

def inicializar_agenda():
    global agenda
    if os.path.exists(ruta_agenda):
        cargar_agenda()

def cargar_agenda():
    global agenda
    agenda = []

    with open(ruta_agenda, 'r', newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            fila['id_medico'] = int(fila['id_medico'])
            fila['dia_numero'] = int(fila['dia_numero'])
            fila['hora_inicio'] = datetime.strptime(fila['hora_inicio'], '%H:%M:%S').time()
            fila['hora_fin'] = datetime.strptime(fila['hora_fin'], '%H:%M:%S').time()

            if 'fecha_actualizacion' in fila and fila['fecha_actualizacion']:
                fila['fecha_actualizacion'] = datetime.strptime(fila['fecha_actualizacion'], '%Y-%m-%d %H:%M:%S')
            else:
                fila['fecha_actualizacion'] = datetime.now()

            agenda.append(fila)
    return agenda

def obtener_horarios_habilitados():
    agenda_ordenada = sorted(agenda, key=lambda x: (x['id_medico'], x['dia_numero']))
    horarios_habilitados = {}

    for entrada in agenda_ordenada:
        id_medico = entrada['id_medico']
        dia_numero = entrada['dia_numero']

        if id_medico not in horarios_habilitados:
            horarios_habilitados[id_medico] = []

        horarios_habilitados[id_medico].append({
            'dia_numero': dia_numero,
            'hora_inicio': entrada['hora_inicio'].strftime('%H:%M:%S'),
            'hora_fin': entrada['hora_fin'].strftime('%H:%M:%S'),
        })

    return horarios_habilitados

def agregar_horario(id_medico, dia_numero, hora_inicio, hora_fin):
    global agenda

    hora_inicio = datetime.strptime(hora_inicio, '%H:%M:%S').time()
    hora_fin = datetime.strptime(hora_fin, '%H:%M:%S').time()

    agenda.append({
        'id_medico': id_medico,
        'dia_numero': dia_numero,
        'hora_inicio': hora_inicio.strftime('%H:%M:%S'),
        'hora_fin': hora_fin.strftime('%H:%M:%S'),
        'fecha_actualizacion': datetime.now().date()
    })

    exportar_datos_a_csv()

def modificar_horario(id_medico, modificaciones):
    global agenda
    cambios_realizados = False

    for modificacion in modificaciones:
        dia_numero = modificacion['dia_numero']
        hora_inicio = datetime.strptime(modificacion['hora_inicio'], '%H:%M:%S').time()
        hora_fin = datetime.strptime(modificacion['hora_fin'], '%H:%M:%S').time()

        for horario in agenda:
            if horario['id_medico'] == id_medico and horario['dia_numero'] == dia_numero:
                horario['hora_inicio'] = hora_inicio.strftime('%H:%M:%S')
                horario['hora_fin'] = hora_fin.strftime('%H:%M:%S')
                horario['fecha_actualizacion'] = datetime.now().date()
                cambios_realizados = True
                break

    if cambios_realizados:
        exportar_datos_a_csv()
        return True
    else:
        return False
    
def eliminar_dias_de_atencion(id_medico):
    global agenda
    agenda = [horario for horario in agenda if horario['id_medico'] != id_medico]
    exportar_datos_a_csv()

def exportar_datos_a_csv():
    global agenda
    
    with open(ruta_agenda, 'w', newline='', encoding='utf-8') as archivo:
        campos = ['id_medico', 'dia_numero', 'hora_inicio', 'hora_fin', 'fecha_actualizacion']
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for registro in agenda:
            escritor.writerow(registro)

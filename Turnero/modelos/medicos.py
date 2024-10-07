import os, csv, requests

# Globales
medicos = []
id_medico = 1
ruta_archivo_medicos = r'C:\Users\Usuario\Downloads\Brenda\Universidad\TUP\1er Año\Programacion2\Turnero\modelos\medicos.csv'

# Inicializa los médicos
def inicializar_medicos():
    global id_medico
    if os.path.exists(ruta_archivo_medicos):
        importar_datos_desde_csv()

# Exporta médicos al archivo
def exportar_a_csv():
    with open(ruta_archivo_medicos, 'w', newline='', encoding='utf-8') as archivo: 
        campos = ['id', 'dni', 'nombre', 'apellido', 'matricula', 'telefono', 'email', 'habilitado']
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        
        for medico in medicos:
            escritor.writerow(medico)

# Importa los médicos desde el archivo
def importar_datos_desde_csv():
    global medicos
    global id_medico
    medicos = []
    with open(ruta_archivo_medicos, newline='', encoding='utf-8') as archivo:  # Se asegura de usar utf-8
        lector = csv.DictReader(archivo)
        for fila in lector:
            fila['id'] = int(fila['id'])
            fila['dni'] = fila['dni']
            fila['matricula'] = fila['matricula']
            fila['telefono'] = fila['telefono']
            medicos.append(fila)

        if len(medicos) > 0:
            id_medico = medicos[-1]['id'] + 1
        else:
            id_medico = 1
            
# Obtiene todos los médicos
def obtener_medicos():
    return medicos

# Obtiene un médico por ID
def obtener_medico_por_id(id):
    for medico in medicos:
        if medico['id'] == id:
            return medico
    return None

# Crea un nuevo médico
def crear_medico(dni, nombre, apellido, matricula, telefono, email, habilitado):
    global id_medico

    nuevo_medico = {
        'id': id_medico,
        'dni': dni,
        'nombre': nombre,
        'apellido': apellido,
        'matricula': matricula,
        'telefono': telefono,
        'email': email,
        'habilitado': habilitado
    }
    medicos.append(nuevo_medico)
    id_medico += 1
    exportar_a_csv()

    return nuevo_medico

# Actualiza la información de un médico por ID
def editar_lista_medicos_por_id(id, dni, nombre, apellido, matricula, telefono, email, habilitado):
    for medico in medicos:
        if medico['id'] == id:
            medico['dni'] = dni
            medico['nombre'] = nombre
            medico['apellido'] = apellido
            medico['matricula'] = matricula
            medico['telefono'] = telefono
            medico['email'] = email
            medico['habilitado'] = habilitado
            exportar_a_csv()
            return medico
    return None

# Deshabilita un médico por ID
def deshabilitar_medico_por_id(id):
    global medicos
    medicos = [medico for medico in medicos if medico['id'] != id]
    exportar_a_csv()

def existe_medico(id):
    return any(medico['id'] == id for medico in medicos)

# Crea médicos desde la API
def crear_medico_desde_api():
    url = 'https://randomuser.me/api/?results=5&inc=name,email,login,phone,id'
    response = requests.get(url)
    data = response.json()['results']

    nuevos_medicos = []
    for medico_data in data:
        dni = medico_data['id']['value']
        matricula = medico_data['login']['password']

        nuevo_medico = crear_medico(
            dni=dni,
            nombre=medico_data['name']['first'],
            apellido=medico_data['name']['last'],
            matricula=matricula,
            telefono=medico_data['phone'],
            email=medico_data['email'],
            habilitado=True
        )
        nuevos_medicos.append(nuevo_medico)

    return nuevos_medicos

nuevos_medicos_desde_api = crear_medico_desde_api()
for medico in nuevos_medicos_desde_api:
    print(medico)

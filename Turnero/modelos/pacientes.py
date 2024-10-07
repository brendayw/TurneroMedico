import os, csv, requests

pacientes = []
id_paciente = 1
ruta_archivo_pacientes = r'C:\Users\Usuario\Downloads\Brenda\Universidad\TUP\1er Año\Programacion2\Turnero\modelos\pacientes.csv'

def inicializar_pacientes():
    global id_paciente
    if os.path.exists(ruta_archivo_pacientes):
        importar_datos_desde_csv()
        
#exporta pacientes a csv
def exportar_a_csv():
    with open(ruta_archivo_pacientes, 'w', newline='', encoding='utf-8') as archivo:
        campos = ['id', 'dni', 'nombre', 'apellido', 'telefono', 'email', 'direccion_calle', 'direccion_numero']
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        
        for paciente in pacientes:
            escritor.writerow(paciente)

# Importa los médicos desde el archivo
def importar_datos_desde_csv():
    global pacientes
    global id_paciente
    pacientes = []
    with open(ruta_archivo_pacientes, newline='', encoding='utf-8') as archivo:  # Asegurarse de usar utf-8
        lector = csv.DictReader(archivo)
        for fila in lector:
            fila['id'] = int(fila['id'])
            fila['dni'] = fila['dni']
            fila['telefono'] = fila['telefono']
            fila['direccion_numero'] = fila['direccion_numero']
            pacientes.append(fila)

        if len(pacientes) > 0:
            id_paciente = pacientes[-1]['id'] + 1
        else:
            id_paciente = 1

#obtener todos los pacientes
def obtener_pacientes():
    return pacientes

#obtener paciente por id
def obtener_paciente_por_id(id):
    for paciente in pacientes:
        if paciente['id'] == id:
            return paciente
    return None

#crear paciente
def crear_paciente(dni, nombre, apellido,telefono,email,direccion_calle,direccion_numero):
    global id_paciente

    pacientes.append({
        'id': id_paciente,
        'dni': dni,
        'nombre': nombre,
        'apellido': apellido,
        'telefono': telefono,
        'email': email,
        'direccion_calle': direccion_calle,
        'direccion_numero': direccion_numero
    })
    id_paciente += 1
    exportar_a_csv()

    return pacientes[-1]

#actualizar info de paciente por id
def editar_paciente_por_id(id, dni, nombre, apellido, telefono, email, direccion_calle, direccion_numero):
    for paciente in pacientes:
        if paciente['id'] == id:
            paciente['dni'] = dni
            paciente['nombre'] = nombre
            paciente['apellido'] = apellido
            paciente['telefono'] = telefono
            paciente['email'] = email
            paciente['direccion_calle'] = direccion_calle
            paciente['direccion_numero'] = direccion_numero
            exportar_a_csv()
            return paciente
    return None

#eliminar paciente por id
def eliminar_paciente_por_id(id_paciente):
    global pacientes
    pacientes = {paciente for paciente in pacientes if paciente['id'] != id_paciente}
    exportar_a_csv()
    if len(pacientes) > 0:
        return pacientes
    else:
        return None
    
#comprueba si existe paciente
def existe_paciente(id):
    for paciente in pacientes:
        if pacientes['id'] == id:
            return True
    return False

#datos de api
def crear_paciente_desde_api():
    url = 'https://randomuser.me/api/?results=10&inc=name,location,email,phone,id'
    response = requests.get(url)
    data = response.json()['results']

    pacientes = []
    for paciente_data in data:
        dni = paciente_data['id']['value']

        paciente = crear_paciente(
            dni=dni,
            nombre=paciente_data['name']['first'],
            apellido=paciente_data['name']['last'],
            telefono=paciente_data['phone'],
            email=paciente_data['email'],
            direccion_calle=paciente_data['location']['street']['name'],
            direccion_numero=paciente_data['location']['street']['number']
        )
        pacientes.append(paciente)

    return pacientes

nuevos_pacientes_desde_api = crear_paciente_desde_api()
for paciente in nuevos_pacientes_desde_api:
    print(paciente)
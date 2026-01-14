import base64
import os
import requests
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config_imp.ini')
file_path = config['file']['file_path']
file_name_head = config['file']['file_name_head']
file_name_line = config['file']['file_name_line']
file_ext = config['file']['file_ext']
# Rutas de los archivos que deseas subir
file_path_head = os.path.join(file_path, file_name_head+file_ext)
file_path_line = os.path.join(file_path, file_name_line+file_ext)
# Función para leer y convertir el contenido del archivo a base64


def encode_file_to_base64(file_path):
    with open(file_path, 'rb') as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    return encoded_string


# Leer y convertir los archivos a base64
file_content_head = encode_file_to_base64(file_path_head)
file_content_line = encode_file_to_base64(file_path_line)
# URL del servicio de Odoo
url = config['odoo_data']['URL']
model_name = config['odoo_data']['model_name']
name_proces = config['odoo_data']['name_proces']
type = config['odoo_data']['type']
doc = config['odoo_data']['doc']
program = config['odoo_data']['program']
user = config['odoo_data']['user']
active_proces = config['odoo_data']['active_proces']
# Datos a enviar en la solicitud POST
data = {
    'head': file_content_head,
    'line': file_content_line,
    'model_name': model_name,
    'name_proces': name_proces,
    'type': type,
    'doc': doc,
    'program': program,
    'user': user,
    'active_proces': active_proces,
}
# Enviar la solicitud POST con requests
response = requests.post(url, json=data)
# Mostrar la respuesta para depuración
print(f'Response: {response.text}')

# Verificar la respuesta y mover los archivos si la subida fue exitosa
if 'success' in response.text:
    path_backup = config['file']['path_backup']
    if not os.path.exists(path_backup):
        os.makedirs(path_backup)

    # Obtener la fecha y hora actual
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Mover los archivos con el nuevo nombre que incluye la fecha y hora
    new_file_name_head = f'{file_name_head}_{current_time}{file_ext}'
    new_file_name_line = f'{file_name_line}_{current_time}{file_ext}'

    os.rename(file_path_head, os.path.join(path_backup, new_file_name_head))
    os.rename(file_path_line, os.path.join(path_backup, new_file_name_line))

    print(
        f'Archivos movidos a la carpeta {path_backup} con los nuevos nombres: {new_file_name_head}, {new_file_name_line}.')
else:
    print('Error al subir los archivos.')

import base64
import os
import requests
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config_exp.ini')

file_path = config['file']['file_path']
file_name_head = config['file']['file_name_head']
file_name_line = config['file']['file_name_line']
file_ext = config['file']['file_ext']

# Rutas de los archivos que deseas subir
file_path_head = os.path.join(file_path, file_name_head+file_ext)
file_path_line = os.path.join(file_path, file_name_line+file_ext)

# URL del servicio de Odoo
url = config['odoo_data']['URL']
model_name = config['odoo_data']['model_name']
name_proces = config['odoo_data']['name_proces']
type = config['odoo_data']['type']
doc = config['odoo_data']['doc']
program = config['odoo_data']['program']
user = config['odoo_data']['user']

# Datos a enviar en la solicitud POST
data = {
    'model_name': model_name,
    'name_proces': name_proces,
    'type': type,
    'doc': doc,
    'program': program,
    'user': user,
}

# Enviar la solicitud POST con requests
response = requests.post(url, json=data)

if response.status_code == 200:
    # Verificar la respuesta y mover los archivos si la subida fue exitosa
    data_json = response.json()
    if data_json.get('result').get('status') == 'success':
        files_data = data_json.get('result').get('message', [])
        # Crear archivos
        for i, file_info in enumerate(files_data):
            file_data = file_info.get('file_data')
            if file_data:
                path = ""
                if (file_info.get('type') == 'head'):
                    patch = file_path_head
                else:
                    patch = file_path_line
                # Decodificar y guardar
                content = base64.b64decode(file_data)
                with open(patch, 'wb') as f:
                    f.write(content)
            else:
                print('Error al subir los archivos.')

else:
    print(f"❌ Error HTTP: Status Code {response.status_code}")
    # Primeros 500 caracteres
    print(f"   Respuesta del servidor: {response.text}...")

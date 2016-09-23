import json
import os
import requests
import polizas

BATCH_FILES_DIR = os.path.join(os.path.dirname(polizas.__file__), 'batch')


def run():

    """
    Hacer la peticion al servicio web, revisar el estado
    de la peticion y, si es correcta, guardar
    los datos recibidos en el archivo prueba.json
    """
    r = requests.get('https://dev.paguelofacil.com/rest/ccprocessing')
    if r.ok:
        with open(os.path.join(BATCH_FILES_DIR, 'prueba.json'), 'w') as prueba:
            prueba.write(json.dumps(r.json(), indent=2))

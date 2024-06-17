import json
import yaml
from jsonschema import validate, exceptions

def load_json_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def validate_data(schema_file, data_file):
    # Cargar el esquema y los datos
    schema = load_json_file(schema_file)
    file_type = detect_file_type(data_file)
    if file_type == 'JSON':
        data = load_json_file(data_file)
    elif file_type == 'YAML':
        data = yaml_to_json(data_file)
    else:
        print(f"El archivo {data_file} no es un archivo YAML ni JSON")
        return

    try:
        # Validar los datos contra el esquema
        validate(instance=data, schema=schema)
        print(f"---> El documento {file_type} {data_file} es válido según el esquema.\n")
    except exceptions.ValidationError as e:
        print(f"---> El documento {file_type} {data_file} no es válido: {e}\n")

# Convierte el archivo YAML a un diccionario Python
def yaml_to_json(yaml_file):
    with open(yaml_file, 'r') as f:
        yaml_content = yaml.safe_load(f) # Cargar el archivo YAML
    return yaml_content

# Comprueba si el archivo es JSON o YAML
def detect_file_type(file_path):
    try:
        with open(file_path, 'r') as file:
            # Intentar cargar el archivo como JSON
            json.load(file)
            return "JSON"
    except json.JSONDecodeError:
        pass

    try:
        with open(file_path, 'r') as file:
            # Intentar cargar el archivo como YAML
            yaml.safe_load(file)
            return "YAML"
    except yaml.YAMLError:
        pass
    return "Unknown"

if __name__ == "__main__":
    #validate_data('schemas/schema.json', 'datas/data.json')
    #validate_data('schemas/schema.json', 'datas/wrongData1.json')
    #validate_data('schemas/schema.json', 'datas/wrongData2.json')
    #validate_data('schemas/schemaService.json', 'datas/dataService.json')
    #validate_data('schemas/schemaDeployment.json', 'datas/dataDeployment.json')
    validate_data('schemas/schemaService.json', 'yamls/service.yaml')

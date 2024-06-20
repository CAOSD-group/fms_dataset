import json
import yaml

jsonFile = 'schemas/schemaDeploymentStandalone.json'

# Definir la lista de atributos a eliminar
attributes_to_remove = [
    "description",  # Descripcion del atributo
    #"enum", # Enumera los valores posibles para ese atributo
    #"type", # Dice el tipo de dato que puede ser
    "additionalProperties",
    "format",
    "x-kubernetes-list-type",
    "x-kubernetes-patch-strategy",
    "required", 
    #"items",
    "x-kubernetes-map-type",
    "x-kubernetes-list-map-keys",
    "x-kubernetes-patch-merge-key",
    #"oneOf",
    "x-kubernetes-unions",
    "fields-to-discriminateBy",
]

def main():
    # Leer el archivo JSON
    with open(jsonFile, 'r') as file:
        schema = json.load(file)

    # Extraer el metamodelo y eliminar atributos innecesarios
    metamodel = extract_properties(remove_attributes(schema, attributes_to_remove))

    # Convertir el diccionario del metamodelo a YAML
    yaml_data = yaml.dump(metamodel, default_flow_style=False)
    print(yaml_data)

    # Eliminar la palabra "properties"
    cleaned_yaml_data = remove_properties_key(metamodel)

    # Escribir el YAML a un archivo
    with open('yamls/YAML_kubernetes_v1.yaml', 'w') as file:
        file.write(yaml_data)
    with open('yamls/YAML_kubernetes_v2.yaml', 'w') as file:
        yaml.dump(cleaned_yaml_data, file, default_flow_style=False)


# Función para eliminar propiedades "description"
def remove_attributes(data, attributes_to_remove):
    if isinstance(data, dict):
        return {key: remove_attributes(value, attributes_to_remove) for key, value in data.items() if key not in attributes_to_remove}
    elif isinstance(data, list):
        return [remove_attributes(item, attributes_to_remove) for item in data]
    else:
        return data

# Extrae los atributos del modelo
def extract_properties(schema):
    if "properties" in schema:
        properties = schema["properties"]
        for prop, value in properties.items():
            if "properties" in value:
                value["properties"] = extract_properties(value)
        return properties
    return {}

# Función para eliminar la linea "properties" y "items"
def remove_properties_key(data):
    if isinstance(data, dict):
        if "items" in data:
            return {key: remove_properties_key(value) for key, value in data["items"].items()}
        elif "properties" in data:
            return {key: remove_properties_key(value) for key, value in data["properties"].items()}
        else:
            return {key: remove_properties_key(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [remove_properties_key(item) for item in data]
    else:
        return data

main()

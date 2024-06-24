import json
import yaml



def main():

    # Esquema del que obtener los datos
    schema = 'schemas/schemaDeploymentStandalone.json'

    # Lista de nombres de subdiccionarios a eliminar manteniendo su contenido
    nombres_a_eliminar = [
        "properties",
        "items",
    ]

    # Lista de claves de subdiccionarios que eliminar con todo su contenido
    keysToRemove = [
        "description", # Descripcion del atributo
        'oneOf', # Indica si el atributo puede tener diferentes tipos
        'enum', # enumera los valores especificos que puede tener el atributo
        "type", # el tipo de dato que puede ser
        'format', # formato de la variable que almacena el valor
        'required', # indica que atributos son obligatorias
        'additionalProperties',
        "x-kubernetes-list-type",
        "x-kubernetes-patch-strategy",
        "x-kubernetes-map-type",
        "x-kubernetes-list-map-keys",
        "x-kubernetes-patch-merge-key",
        "x-kubernetes-unions",
        'x-kubernetes-group-version-kind', # informacion sobre el group y version de la apiVersion
        '$schema'
    ]
    
    data = loadSchema(schema)
    remove_keys(data, keysToRemove) # funciona
    eliminar_subdiccionarios_especificos(data, nombres_a_eliminar)

    #saveDataJSON(data)
    saveDataYAML(data)

# Elimina subdicionarios con un nombre especificado, pero manteniendo su contenido
def eliminar_subdiccionario_especifico(dic, nombre):
    # Listas para almacenar las claves de los subdiccionarios a eliminar y el contenido a agregar
    claves_a_eliminar = []
    contenido_a_agregar = {}

    for key, value in dic.items():
        if isinstance(value, dict):
            # Si el nombre del subdiccionario está en la lista de nombres a eliminar
            if key == nombre:
                # Almacenar el contenido del subdiccionario para agregarlo al diccionario padre
                contenido_a_agregar.update(value)
                # Marcar el subdiccionario para eliminación
                claves_a_eliminar.append(key)
            # Recursivamente llamar a la función para subdiccionarios
            eliminar_subdiccionario_especifico(dic[key], nombre)

    # Eliminar subdiccionarios marcados
    for key in claves_a_eliminar:
        dic.pop(key)
    
    # Agregar contenido de subdiccionarios eliminados al diccionario padre
    dic.update(contenido_a_agregar)

# Elimina todos los subdiccionarios cuyos nombres aparezcan en una lista dada, pero manteniendo su contenido
def eliminar_subdiccionarios_especificos(data, nombres_a_eliminar):
  for nombre in nombres_a_eliminar:
    eliminar_subdiccionario_especifico(data, nombre)

# Elimina los subdiccionarios de una lista dada
def remove_keys(data, keys_to_remove):
    if isinstance(data, dict):
        # Crear una copia de las claves actuales del diccionario
        keys = list(data.keys())
        for key in keys:
            if key in keys_to_remove:
                del data[key]
            else:
                # Aplicar recursivamente la función a los valores
                data[key] = remove_keys(data[key], keys_to_remove)
    elif isinstance(data, list):
        # Si es una lista, aplicar la función a cada elemento
        data = [remove_keys(item, keys_to_remove) for item in data]
    return data

# Carga el schema (JSON)
def loadSchema(schema):
    with open(schema, 'r') as f:
        data = json.load(f)
    return data

# Guarda los resultados en un archivo JSON
def saveDataJSON(data):
    with open('rdo.json', "w") as f:
        json.dump(data, f, indent=2)

# Guarda los resultados en un archivo YAML
def saveDataYAML(data):
    yaml_data = yaml.dump(data, indent=2, default_flow_style=False)
    with open('rdo.yaml', 'w') as file:
        file.write(yaml_data)

main()
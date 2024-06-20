import json
import yaml



# Definir la lista de atributos a eliminar
attributes_to_remove = [
    "description",  
    #"enum", # Enumera los valores posibles para ese atributo
    #"type", # Dice el tipo de dato que puede ser
    "additionalProperties",
    "format",
    "required", 
    #"items",
    #"oneOf",
]

def main():
    schema = 'schemas/schemaDeploymentStandalone.json'
    keysToRemove = [
        "description", # Descripcion del atributo
        #"type", # el tipo de dato que puede ser
        "x-kubernetes-list-type",
        "x-kubernetes-patch-strategy",
        "x-kubernetes-map-type",
        "x-kubernetes-list-map-keys",
        "x-kubernetes-patch-merge-key",
        "x-kubernetes-unions",
        ]
    
    keysToRemoveAndSave = [
        "items",
        "properties",
        ]
    
    data = loadSchema(schema)

    data = remove_keys(data, keysToRemove)
    data = remove_keys_saving_data(data, keysToRemoveAndSave)
    data = remove_specific_types(data)

    saveData(data)

# Elimina los diccionarios que tengan como key las que aparecen en una lista
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

# Elimina los diccionarios de una lista pero anexando su contenido al diccionario superior
def remove_keys_saving_data(data, keys_to_remove):
    if isinstance(data, dict):
        keys = list(data.keys())
        for key in keys:
            if key in keys_to_remove:
                value = data[key]
                del data[key]
                if isinstance(value, dict):
                    # Promover los elementos del diccionario
                    for sub_key, sub_value in value.items():
                        data[sub_key] = sub_value
                elif isinstance(value, list):
                    for sub_value in value:
                        if isinstance(sub_value, dict):
                            for sub_key, sub_sub_value in sub_value.items():
                                data[sub_key] = sub_sub_value
                        else:
                            # Si la lista no contiene diccionarios, esto los agregará como valores únicos
                            data.setdefault(sub_value, sub_value)
            else:
                data[key] = remove_keys_saving_data(data[key], keys_to_remove)
    elif isinstance(data, list):
        data = [remove_keys_saving_data(item, keys_to_remove) for item in data]
    return data

# Elimina las keys que son type que son referencia del tipo de dato
def remove_specific_types(data):
    if isinstance(data, dict):
        keys = list(data.keys())
        for key in keys:
            value = data[key]
            if key == "type" and (isinstance(value, list) or isinstance(value, str)):
                del data[key]
            else:
                data[key] = remove_specific_types(value)
    elif isinstance(data, list):
        data = [remove_specific_types(item) for item in data]
    return data



# Cargar el schema (JSON)
def loadSchema(schema):
    with open(schema, 'r') as f:
        data = json.load(f)
    return data

def saveData(data):
    with open('rdo.json', "w") as f:
        json.dump(data, f, indent=2)


main()
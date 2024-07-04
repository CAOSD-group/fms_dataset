# script para comparar dos diccionarios (dos JSON sacados del script YAML_to_JSON.py) para ver que 
# diferencias existen entre ambos. Puede ser una buena herramienta para unificarlos

from pprint import pprint
from deepdiff import DeepDiff
import json


def main():
  dict1 = loadSchema('generatedJSON/Deployment.json')
  dict2 = loadSchema('generatedJSON/service.json')

  diff = DeepDiff(dict1, dict2)
  print(f'--- Elementos añadidos --- \n')
  pprint(diff['dictionary_item_added'])
  print(f'\n--- Elementos eliminados --- \n')
  pprint(diff['dictionary_item_removed'])

# Carga el schema (JSON)
def loadSchema(schema):
    with open(schema, 'r') as f:
        data = json.load(f)
    return data

main()
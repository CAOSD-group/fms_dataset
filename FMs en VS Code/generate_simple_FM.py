# script para simplificar y adaptar un modelo de caracteristicas para poder trabajar
# con la herramienta de flamapy (tambien borra las restricciones)

import re

fm_original = 'Feature Models\Kubernetes_manifest_v2.uvl'
fm_simplified = 'Feature Models\Kubernetes_manifest_v2_simplified.uvl'


# Función para procesar el texto
def generate_fm_simplified(fm_original, fm_simplified, palabras_a_eliminar):
    # Leer el archivo original
    with open(fm_original, 'r', encoding='utf-8') as f:
        text = f.read()

    # Eliminar y reemplazar las palabras o caracteres especificados
    for palabra in palabras_a_eliminar:
        text = text.replace(palabra, '')  
    text = text.replace('.', '_')

    # Separ el modelo de caracteristicas en dos partes, las caracteristicas y las restricciones
    tree = re.split(r'^\s*constraints', text, maxsplit=1, flags=re.MULTILINE)[0]
    restrictions = re.split(r'^\s*constraints', text, maxsplit=1, flags=re.MULTILINE)[1]

    # Eliminar las restricciones no soportadas actualmente por flamapy
    lines_restrictions = restrictions.split('\n')
    simplified_restrictions = []
    for line in lines_restrictions:
        if any(c in line for c in characters_to_delete):
            continue
        else:
            simplified_restrictions.append(line)

    # Guardar el texto modificado en un nuevo archivo
    with open(fm_simplified, 'w', encoding='utf-8') as f:
        f.write(tree)
        f.write('constraints')
        for line in simplified_restrictions:
            f.write(line)
            f.write('\n')


# Palabras o caracteres a eliminar
words_to_delete = ['String ', 'Integer ', 'Boolean ', 'cardinality', '[0..*]']  # Ajusta estas palabras
characters_to_delete = [' < ', ' > ', ' <=> ', ' == ', '//']

# Llamar a la función para procesar el archivo
generate_fm_simplified(fm_original, fm_simplified, words_to_delete)

print(f"El archivo procesado se ha guardado como {fm_simplified}")

# script para simplificar y adaptar un modelo de caracteristicas para poder trabajar
# con la herramienta de flamapy (tambien borra las restricciones)

import re

fm_original = 'Feature Models\Kubernetes_manifest_v2.uvl'
fm_simplified = 'Feature Models\Kubernetes_manifest_v2_simplified.uvl'


# Función para procesar el texto
def generate_fm_simplified(fm_original, fm_simplified, palabras_a_eliminar):
    # Leer el archivo original
    with open(fm_original, 'r', encoding='utf-8') as f:
        texto = f.read()

    # Eliminar y reemplazar las palabras o caracteres especificados
    for palabra in palabras_a_eliminar:
        texto = texto.replace(palabra, '')  
    texto = texto.replace('.', '_')
    # Eliminar restricciones
    texto = re.split(r'^\s*constraints', texto, maxsplit=1, flags=re.MULTILINE)[0]

    # Guardar el texto modificado en un nuevo archivo
    with open(fm_simplified, 'w', encoding='utf-8') as f:
        f.write(texto)

# Palabras o caracteres a eliminar
words_to_delete = ['String ', 'Integer ', 'Boolean ', 'cardinality', '[0..*]']  # Ajusta estas palabras

# Llamar a la función para procesar el archivo
generate_fm_simplified(fm_original, fm_simplified, words_to_delete)

print(f"El archivo procesado se ha guardado como {fm_simplified}")

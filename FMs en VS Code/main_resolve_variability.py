import os
import argparse
import csv
import sys
from typing import Any

import jinja2

from spl_implementation.utils import utils
from spl_implementation.models import VEngine



def print_without_blank_lines(text, file):
    for line in text.splitlines():
        if line.strip():  # Verifica si la línea no está en blanco
            sys.stdout.write(line + '\n')  # Escribe la línea en stdout
            file.write(line + '\n')

# CONSTANTS

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Variability resolution with Jinja templates.')
    # parser.add_argument('-c', '--configs', dest='configs_dir', type=str, required=True, 
    #                     help='Directory with the configurations files (.json).')
    # parser.add_argument('-t', '--template', dest='template_file', type=str, required=True, 
    #                     help='Template file (.jinja) over which the variability is resolved.')
    # parser.add_argument('-m', '--mapping', dest='mapping_file', type=str, required=True, 
    #                     help='File with the mapping between the variation points and the templates (.csv).')
    # args = parser.parse_args()

    # # Get parameters
    # configurations_files = utils.get_filepaths(args.configs_dir, ['.json'])
    # template_file = args.template_file
    # mapping_file = args.mapping_file

    # print('CONFIGURATION FILES:')
    # for i, config_file in enumerate(configurations_files, 1):
    #     print(f'|-{i}: {config_file}')
    # if not configurations_files:
    #     print('|-Warning: No configurations files detected. Use a folder with .json files.')
    
    # print('TEMPLATE FILES:')
    # if template_file.endswith('.jinja'):
    #     print(f'|-{template_file}')
    # else:
    #     print('|-Error: Wrong template file extension. Use a .jinja file.')

    # print('MAPPING MODEL:')
    # if mapping_file.endswith('.csv'):
    #     print(f'|-{mapping_file}')
    # else:
    #     print('|-Error: Wrong mapping model file extension. Use a .csv file.')

    vengine = VEngine()

    # Dockerfile_conf
    #vengine.load_configuration('configurations/Dockerfile_conf.uvl.json')
    #vengine.load_mapping_model('mapping_models/dockerfile_conf_mapping.csv')
    #vengine.load_template('templates/dockerfile_conf_template.txt.jinja')
 

    #Docker_compose
    #vengine.load_configuration('configurations/Docker_compose.uvl.json')
    #vengine.load_mapping_model('mapping_models/docker_compose_mapping.csv')
    #vengine.load_template('templates/Docker_compose/docker_compose_template.txt.jinja')

    #Kubernetes_manifest
    vengine.load_configuration('configurations/Kubernetes_manifest.uvl.json')
    vengine.load_mapping_model('mapping_models/Kubernetes_manifest_mapping.csv')
    vengine.load_template('templates/Kubernetes_manifest/Kubernetes_manifest_template.txt.jinja')


    result = vengine.resolve_variability()

    with open("salida.txt", "w") as f:
        print_without_blank_lines(result, f)
        


    
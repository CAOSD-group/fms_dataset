import os

from flamapy.metamodels.fm_metamodel.transformations import UVLReader

import utils


MODELS_DIR = 'models'


def main():
    for model_path in utils.get_filepaths(MODELS_DIR, ['.uvl']):
        # Get feature model name
        path, filename = os.path.split(model_path)
        filename = '.'.join(filename.split('.')[:-1])

        fm_model = UVLReader(model_path).transform()
        
        print(fm_model)
        print(f'Features: {[f.name for f in fm_model.get_features()]}')

if __name__ == '__main__':
    main()
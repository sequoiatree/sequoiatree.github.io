from os import listdir
from os.path import join

from flask import Markup

from utils import *

def get_utils():
    UTILS = {}
    UTILS['sequence'] = sequence
    UTILS['md_sequence'] = md_sequence
    return UTILS

def sequence(resource, name):
    contents = tuple(resource.assets[f'{name}'])
    captions = load_diagram_assets(resource, name)
    return package_diagram_components(contents, captions)

def md_sequence(resource, name):
    contents = load_diagram_assets(resource, f'{name}-contents')
    captions = load_diagram_assets(resource, f'{name}-captions')
    return package_diagram_components(contents, captions)

def package_diagram_components(contents, captions):
    assert len(contents) == len(captions), 'Every sequence frame requires exactly one caption.'
    return tuple(zip(contents, captions))

def load_diagram_assets(resource, name):
    assets_dir = join(resource.assets_dir, name)
    assets = [
        Markup(read(join(assets_dir, file)))
        for file in sorted(listdir(assets_dir), key=lambda key: (len(key), key))
    ]
    return assets

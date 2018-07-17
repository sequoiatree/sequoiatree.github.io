from os import listdir
from os.path import join

from flask import Markup

from utils import *

def get_utils():
    UTILS = {}
    UTILS['sequence'] = sequence
    return UTILS

def sequence(resource, name):
    contents = tuple(resource.assets[f'{name}'])
    captions_dir = join(resource.assets_dir, name)
    captions = [Markup(read(join(captions_dir, file)))
                for file in sorted(listdir(captions_dir), key=lambda key: (len(key), key))]
    assert len(contents) == len(captions), 'Every pyagram frame requires exactly one caption.'
    return tuple(zip(contents, captions))

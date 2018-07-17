from os import listdir, remove
from os.path import isdir, join, pardir
from shutil import rmtree

import main

if __name__ == '__main__':
    SRC_DIRECTORIES = {'.git', 'src', 'webenv', 'TEMPORARY'}
    remove(join(pardir, 'index.html'))
    for directory in listdir(pardir):
        if isdir(directory) and directory not in SRC_DIRECTORIES:
            rmtree(join(pardir, directory))
    main.freezer.freeze()

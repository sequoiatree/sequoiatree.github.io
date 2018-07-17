from os import listdir, remove
from os.path import join, pardir

import main

if __name__ == '__main__':
    SRC_FILES = {
        '.gitignore',
        'requirements.txt',
        'README.md',
        'LICENSE.md',
        'src',
        'webenv',
        'TEMPORARY',
    }
    for file in listdir(pardir):
        if file not in SRC_FILES:
            remove(join(pardir, file))
    main.freezer.freeze()

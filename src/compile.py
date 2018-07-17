from os import listdir, remove
from sys import argv

# Usage: python3 compile.py svg-name
# Compiles the contents of {..., 3.svg, 2.svg, 1.svg} into svg-name.svg,

def read_line(file, line):
    with open(file, 'r') as file:
        for _ in range(line):
            content = file.readline()
    return content

def write(file, *args, **kwargs):
    with open(file, 'w') as file:
        file.write(*args, **kwargs)

if __name__ == '__main__':
    svgs = sorted((file for file in listdir() if '.' in file and file.split('.')[1] == 'svg'),
                  key=lambda filename: (len(filename), filename))
    contents = (read_line(svg, 2) for svg in reversed(svgs))
    write(f'{argv[1]}.svg', '\n'.join(contents))
    for svg in svgs:
        remove(svg)

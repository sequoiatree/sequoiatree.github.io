from os import mkdir
from os.path import join
from re import match, sub
from shutil import rmtree

from flask import Markup
from markdown import markdown

from md_utils import *

MARKDOWN_EXTENSIONS = (
    'extra',
    'toc',
    'pymdownx.arithmatex',
    'pymdownx.keys',
    'pymdownx.superfences',
)

def read_md(file, assets_dir=None):
    return parse_md(read(file), assets_dir)

def parse_md(text, assets_dir=None):
    text = fix_indentation(text)
    text = trim_codefence_whitespace(text)
    text = evaluate_macros(text, assets_dir)
    text = md_to_html(text)
    text = allow_subscripts_globally(text)
    return text

def fix_indentation(text):
    fix_indentation = True
    lines = text.split('\n')
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith('```'):
            fix_indentation = not fix_indentation
        if fix_indentation:
            indentation_match = match('(   )+\S', line)
            if indentation_match:
                indentation = len(indentation_match.group(0)) - 1
                new_indentation = 4 * indentation // 3
                spaces = ' ' * new_indentation
                lines[i] = f'{spaces}{line[indentation:]}'
    return '\n'.join(lines)

def trim_codefence_whitespace(text):
    # Before indented code fence.
    text = sub('\n\n +```', lambda match: match.group(0)[1:], text)
    # After indented code fence.
    text = sub(' +```\n\n', lambda match: match.group(0)[:-1], text)
    return text

def md_to_html(text):
    return markdown(text, extensions=MARKDOWN_EXTENSIONS, output_format='html5')

def allow_subscripts_globally(text):
    text = sub(
        '~(\S+)~',
        lambda match: Markup(f'<sub>{match.group(1)}</sub>'),
        text
    )
    return text

def evaluate_macros(text, assets_dir):
    text = evaluate_asset_macros(text)
    text = evaluate_image_macros(text)
    if assets_dir:
        text = evaluate_pyagram_macros(assets_dir, text)
    return text

def evaluate_asset_macros(text):
    base = 'ASSET '
    text = sub(
        f'{base}([0-9a-z-]+)',
        lambda match: f"{{{{ resource.assets['{match.group(0)[len(base):]}'] }}}}",
        text
    )
    return text

def evaluate_image_macros(text):
    text = sub(
        'IMG-([A-Z]+) ([0-9a-z-]+)',
        lambda match: f"{{{{ macros.image('{match.group(2)}', '{match.group(1).lower()}') }}}}",
        text
    )
    return text

def evaluate_pyagram_macros(assets_dir, text):
    pattern = 'STARTPYAGRAM ([0-9a-z-]+)\n\n([\S\s]*?)\n\nENDPYAGRAM'
    def rule(match):
        name = match.group(1)
        captions = match.group(2).split('\n\n---\n\n')
        load_pyagram_captions(assets_dir, name, captions)
        return f"{{{{ macros.slider('{name}', sequence(resource, '{name}')) }}}}"
    text = sub(pattern, rule, text)
    return text

def load_pyagram_captions(assets_dir, name, captions):
    pyagram_dir = join(assets_dir, name)
    try:
        rmtree(pyagram_dir)
    except FileNotFoundError:
        None
    mkdir(pyagram_dir)
    for i in range(len(captions)):
        caption = captions[i]
        write(join(pyagram_dir, f'{name}-{i}.html'), parse_md(caption))

from datetime import date
from os import mkdir
from os.path import join
from re import match, search, sub
from shutil import rmtree

from flask import Markup
from markdown import markdown

MARKDOWN_EXTENSIONS = (
    'extra',
    'toc',
    'pymdownx.arithmatex',
    'pymdownx.keys',
    'pymdownx.superfences',
)

def hyphen_case(text):
    ILLEGAL_CHARS = {' ': '-', '/': '-', '&': 'and', '_': ''}
    text = text.lower()
    for char in ILLEGAL_CHARS:
        text = text.replace(char, ILLEGAL_CHARS[char])
    return text

def snake_case(text):
    return hyphen_case(text).replace('-', '_')

def read(file):
    with open(file, 'r') as file:
        content = file.read()
    return content

def write(file, *args, **kwargs):
    with open(file, 'w') as file:
        file.write(*args, **kwargs)

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

def process_svg(svg):
    pattern = '<svg (.*?)>'
    width, height = None, None
    strip_units = lambda value: match('(\d+)[a-z]*', value).group(1)
    def rule(match):
        nonlocal width, height
        head = match.group(0)
        width = get_attribute('width', head)
        height = get_attribute('height', head)
        head = set_attribute('width', head, '"100%"')
        head = set_attribute('height', head, '"100%"')
        head = add_attribute('viewbox', head, f'"0 0 {strip_units(width)} {strip_units(height)}"')
        return head
    svg = sub(pattern, rule, svg)
    assert not svg.startswith('<!DOCTYPE')
    assert width is not None and height is not None
    return Markup(wrap_svg(svg, {'width': width, 'height': height}))

def get_attribute(attribute, head):
    return search(f'{attribute}="(.*?)"', head).group(1)

def set_attribute(attribute, head, value):
    return sub(f'{attribute}=(.*?) ', lambda match: f'{attribute}={value} ', head)

def add_attribute(attribute, head, value):
    return sub('(<.+? )', lambda match: f'{match.group(0)}{attribute}={value} ', head)

def wrap_svg(svg, style):
    style_html = ''.join(f'{attribute}:{value};' for attribute, value in style.items())
    return f'<div class="svg-wrapper" style="{style_html}">{svg}</div>'

def get_age():
    today, birth = date.today(), date(2000, 2, 17)
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

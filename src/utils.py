from datetime import date
from markdown import markdown
from re import match, search, sub

from flask import Markup

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

def read_md(file):
    fix_indentation = True
    with open(file, 'r') as file:
        lines = file.readlines()
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
        content = ''.join(lines)
    return content

def parse_markdown(text):
    return process_html(markdown(text, extensions=MARKDOWN_EXTENSIONS, output_format='html5'))

def process_html(text):
    text = allow_subscripts_globally(text)
    return text

def allow_subscripts_globally(text):
    text = sub(
        '~(\S+)~',
        lambda match: Markup(f'<sub>{match.group(1)}</sub>'),
        text
    )
    return text

def get_age():
    today, birth = date.today(), date(2000, 2, 17)
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

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

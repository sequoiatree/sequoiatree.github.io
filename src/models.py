from importlib import import_module
from os import listdir, mkdir
from os.path import join
from re import sub
from shutil import rmtree

from flask import Markup

from textbooks.published import PUBLISHED
from textbook_utils import get_utils
from utils import *

class FileSystemObject():

    def __init__(self, head, tail):
        assert isinstance(head, FileSystemObject) or isinstance(head, str)
        assert isinstance(tail, str)
        self.head = head
        self.tail = tail

    @property
    def path(self):
        if isinstance(self.head, FileSystemObject):
            return join(self.head.path, self.tail)
        else:
            return join(self.head, self.tail)

class Textbook(FileSystemObject):

    def __init__(self, head, tail):
        super().__init__(head, tail)
        self.route = tail
        self.title = read(join(self.path, 'meta.txt'))
        self.chapters = [
            Chapter(self, tail) for tail in
            import_module('{}.published'.format(self.path.replace('/', '.'))).PUBLISHED
        ]

class TextbookResource(FileSystemObject):

    utils = get_utils()

    def __init__(self, head, tail):
        super().__init__(head, tail)

    def load_file(self, in_file):
        dir_files = listdir(self.path)
        in_file = '{}.md'.format(in_file)
        out_file = join(self.path, self.template)
        if in_file in dir_files and self.template not in dir_files:
            template = read('templates/textbook-content.html')
            in_content = self.process_input(read_md(join(self.path, in_file)))
            out_content = template.replace(
                '{{ TEXTBOOK CONTENT }}',
                parse_markdown(in_content)
            )
            write(out_file, out_content)

    def process_input(self, text):
        text = self.trim_codefence_whitespace(text)
        text = self.evaluate_pyagram_macros(text)
        text = self.evaluate_asset_macros(text)
        text = self.evaluate_image_macros(text)
        return text

    def trim_codefence_whitespace(self, text):
        # Before indented code fence.
        text = sub('\n\n +```', lambda match: match.group(0)[1:], text)
        # After indented code fence.
        text = sub(' +```\n\n', lambda match: match.group(0)[:-1], text)
        return text

    def evaluate_pyagram_macros(self, text):
        pattern = 'STARTPYAGRAM ([0-9a-z-]+)\n\n([\S\s]*?)\n\nENDPYAGRAM'
        def rule(match):
            name = match.group(1)
            captions = match.group(2).split('\n\n---\n\n')
            self.load_pyagram_captions(name, captions)
            return f"{{{{ macros.slider('{name}', sequence(resource, '{name}')) }}}}"
        text = sub(pattern, rule, text)
        return text

    def load_pyagram_captions(self, name, captions):
        pyagram_dir = join(self.assets_dir, name)
        try:
            rmtree(pyagram_dir)
        except FileNotFoundError:
            None
        mkdir(pyagram_dir)
        for i in range(len(captions)):
            caption = captions[i]
            write(join(pyagram_dir, f'{name}-{i}.html'), parse_markdown(caption))

    def evaluate_asset_macros(self, text):
        base = 'ASSET '
        text = sub(
            f'{base}([0-9a-z-]+)',
            lambda match: f"{{{{ resource.assets['{match.group(0)[len(base):]}'] }}}}",
            text
        )
        return text

    def evaluate_image_macros(self, text):
        text = sub(
            'IMG-([A-Z]+) ([0-9a-z-]+)',
            lambda match: f"{{{{ macros.image('{match.group(2)}', '{match.group(1).lower()}') }}}}",
            text
        )
        return text

    @property
    def assets_dir(self):
        ASSETS_DIR = 'assets'
        if ASSETS_DIR in listdir(self.path):
            return join(self.path, ASSETS_DIR)
        else:
            return None

    @property
    def renderer(self):
        return snake_case(self.route)

    @property
    def template(self):
        return '{}.html'.format(self.filename)

class Chapter(TextbookResource):

    def __init__(self, head, tail):
        self.textbook = head
        super().__init__(self.textbook, tail)
        self.filename = self.tail
        self.route = join(self.textbook.route, self.filename)
        self.title = read(join(self.path, 'meta.txt'))
        self.assets = self.load_assets()
        self.practice = self.load_practice()
        self.load_file('Chapter')

    def load_assets(self):
        assets = {}
        if self.assets_dir:
            for file in listdir(self.assets_dir):
                if '.' in file:
                    name, extension = file.split('.')
                    if extension in {'html', 'svg'}:
                        assets[name] = self.load_asset(file, extension)
        return assets

    def load_asset(self, file, extension):
        content = Markup(read(join(self.assets_dir, file)))
        if extension == 'html':
            return content
        elif extension == 'svg':
            svgs = content.split('\n')
            if len(svgs) == 1:
                return process_svg(svgs[0])
            else:
                return tuple(map(process_svg, svgs))

    def load_practice(self):
        practice = Practice(self)
        return practice if practice.template in listdir(self.path) else None

class Practice(TextbookResource):

    def __init__(self, chapter):
        self.chapter = chapter
        self.textbook = self.chapter.textbook
        super().__init__(self.chapter.head, self.chapter.tail)
        self.filename = '{}-practice'.format(self.chapter.filename)
        self.route = join(self.textbook.route, self.filename)
        self.title = '{} Practice'.format(self.chapter.title)
        self.assets = self.chapter.assets
        self.load_file('Practice')

TEXTBOOKS = [Textbook('textbooks', tail) for tail in PUBLISHED]

CHAPTERS = sum([textbook.chapters for textbook in TEXTBOOKS], [])

BIO = {
    'age': get_age(),
    'contact': read('static/bio/contact.txt'),
}

from importlib import import_module
from os import listdir, mkdir
from os.path import join

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
            in_content = read_md(join(self.path, in_file), self.assets_dir)
            out_content = template.replace('{{ TEXTBOOK CONTENT }}', in_content)
            write(out_file, out_content)

    @property
    def assets_dir(self):
        assets_dir = 'assets'
        src_relative_dir = join(self.path, assets_dir)
        if assets_dir not in listdir(self.path):
            mkdir(src_relative_dir)
        return src_relative_dir

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

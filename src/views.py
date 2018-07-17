from flask import render_template

from app import app
from models import TEXTBOOKS, CHAPTERS, BIO
from utils import *

def rename(name):
    def rename_decorator(function):
        function.__name__ = name
        return function
    return rename_decorator

def make_textbook_template(resource, is_practice):
    @app.route(f'/{resource.route}.html')
    @rename(resource.renderer)
    def render_resource():
        return render_template(resource.template,
                               resource=resource,
                               is_practice=is_practice,
                               **resource.utils)

@app.route('/')
def render_index():
    return render_template('index.html', TEXTBOOKS=TEXTBOOKS, **BIO)

for chapter in CHAPTERS:
    make_textbook_template(chapter, False)
    if chapter.practice:
        make_textbook_template(chapter.practice, True)

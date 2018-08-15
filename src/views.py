from flask import render_template

from app import app
from models import TEXTBOOKS, CHAPTERS, BIO
from utils import *

def rename(name):
    def rename_decorator(function):
        function.__name__ = name
        return function
    return rename_decorator

def make_template(route, renderer, template_function, *template_args):
    @app.route(f'/{route}.html')
    @rename(renderer)
    def render():
        return template_function(*template_args)

def make_textbook_template(resource, is_practice):
    return make_template(
        resource.route,
        resource.renderer,
        lambda resource: render_template(
            resource.template, resource=resource, is_practice=is_practice, **resource.utils
        ),
        resource
    )

@app.route('/')
def render_index():
    return render_template('index.html', TEXTBOOKS=TEXTBOOKS, **BIO)

for chapter in CHAPTERS:
    make_textbook_template(chapter, False)
    if chapter.practice:
        make_textbook_template(chapter.practice, True)

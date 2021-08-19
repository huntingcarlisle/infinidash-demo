import os
from io import BytesIO 
from flask import Flask, render_template, send_file
from flask.helpers import send_file

def create_app(test_config=None):
    import charts
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', default='dev')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)


    return app
import config
import click
from flask import Flask, url_for, render_template, escape, redirect, Blueprint
from flask.cli import FlaskGroup


app = Flask(__name__, static_url_path='/static')
app.config.from_object(config)
app.use_reloader = False
app.debug = True


def create_app(info=None):
    return app

cli = FlaskGroup(create_app=create_app)


@app.route('/')
def index():
    return render_template('base/index.html')

if __name__ == '__main__':
    cli()
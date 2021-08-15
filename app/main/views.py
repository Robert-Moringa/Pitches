from flask import render_template, redirect, url_for,abort,request
from . import main

@main.route('/')
def index():
    tittle= 'Welcome to your one stop Pitches Website'
    return render_template('index.html', title = tittle)
#!usr/bin/python3
from flask import Flask, render_template, flash, redirect, request

import re

app = Flask(__name__) # Creating Flask Application Instance


@app.route('/')
@app.route('/index', methods=['GET', 'POST']) # App Route Decorator
def submit(): # Method to be executed when above route/endpoint are hit
    pass

if __name__ == '__main__':
    app.run()

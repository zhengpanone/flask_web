# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/4 17:21
"""

# import lib
from random import randint

from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder="../dist/static", template_folder="../dist")

cors = CORS(app, resources={'/api/*': {"origins": "*"}})


@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 10)
    }
    return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')


"""
@app.route('/')
def index():
    return render_template("index.html")
    
"""

if __name__ == '__main__':
    app.run(debug=True)

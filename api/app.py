#!/usr/bin/python3
from flask import Flask, render_template
from model import storage

app = Flask(__name__)

@app.route("/")
def home():
    obj = storage.jop()

    return render_template('home.html', obj=obj)

if __name__ == '__main__':
    app.run(debug=True, port=4998)

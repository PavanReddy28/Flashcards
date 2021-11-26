from flask import Flask, request, render_template
from flask import current_app as app


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/review")
def review():
    return render_template('review.html')


@app.route("/library")
def library():
    return render_template('library.html')

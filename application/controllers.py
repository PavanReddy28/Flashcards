from flask import Flask, request, render_template, redirect
from flask import current_app as app, session
import flask_login
from flask_security import login_required
from .database import db
from application.models import Decks, User


@app.route("/")
def index():
    user = db.session.query(User).all()
    # app.logger.debug(user)
    return render_template('index.html')

@app.route("/review")
@login_required
def review():
    return render_template('review.html')

@app.route("/library")
@login_required
def library():
    return render_template('library.html')

@app.route("/dashbaord")
@login_required
def dashboard():
    
    ## Get user information
    # uid = session['_user_id']
    # print(uid)
    user = flask_login.current_user

    ## Get decks information
    decks = db.session.query(Decks).filter(Decks.id==3)
    
    return render_template('dashboard.html', user=user, decks=decks)
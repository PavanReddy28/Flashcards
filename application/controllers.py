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
    ## Get decks information
    decks = db.session.query(Decks).filter(Decks.id==3)    
    return render_template('review.html', decks=decks)

@app.route("/library")
@login_required
def library():
    ## Get decks information
    decks = db.session.query(Decks).filter(Decks.id==3)   
    return render_template('library.html', decks=decks)

@app.route("/dashbaord")
@login_required
def dashboard():
    
    ## Get user information
    # uid = session['_user_id']
    # print(uid)
    user = flask_login.current_user

    ## Get decks information
    decks = db.session.query(Decks).filter(Decks.id==3).limit(3)

    # incomplete
    # recent decks -  top 3
    # need to be reviewed - top 3
    # not attempted - Show all
    
    return render_template('dashboard.html', user=user, decks=decks)
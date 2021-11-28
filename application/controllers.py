from datetime import datetime
from flask import Flask, request, render_template, redirect
from flask import current_app as app, session
import flask_login
from flask_security import login_required
from .database import db
from application.models import Cards, Decks, User
import csv


@app.route("/")
def index():
    user = db.session.query(User).all()
    # app.logger.debug(user)
    return render_template('index.html')

@app.route("/review")
@login_required
def review():
    ## Get decks information
    user = flask_login.current_user
    print(user.id)
    decks = db.session.query(Decks).filter(Decks.id==user.id)    
    return render_template('review.html', decks=decks)

@app.route("/library")
@login_required
def library():
    ## Get decks information
    user = flask_login.current_user
    decks = db.session.query(Decks).filter(Decks.id==user.id)   
    return render_template('library.html', decks=decks)

@app.route("/dashbaord")
@login_required
def dashboard():
    
    ## Get user information
    # uid = session['_user_id']
    # print(uid)
    user = flask_login.current_user

    ## Get decks information
    decks = db.session.query(Decks).filter(Decks.id==user.id).limit(3)

    # incomplete
    # recent decks -  top 3
    # need to be reviewed - top 3
    # not attempted - Show all
    
    return render_template('dashboard.html', user=user, decks=decks)


@app.route("/editDecks", methods=["GET", "POST"])
@login_required
def editDecks():
    
    ## Get user information
    user = flask_login.current_user

    
    return render_template('edit_decks.html', user=user)

@app.route("/deck/<int:deck_id>")
@login_required
def Decks(deck_id):
    deck = db.session.query(Cards).filter( Cards.deck_id==deck_id)    
    return render_template('decks.html', deck=deck)

@app.route("/addDecks", methods=["GET", "POST"])
@login_required
def addDecks():
    ## Get user information
    user = flask_login.current_user
    if request.method == 'POST':
        name = request.form["deck_name"]
        desc = request.form["deck_desc"]
        file = request.files["csvFile"]
        deck = Decks(deck_name=name, deck_description=desc, id=user.id, access_time=datetime.now())
        db.session.add(deck)
        db.session.commit()
        db.session.flush()

        if file:
            file_contents = file.stream.read().decode("utf-8")
            csv_input = csv.reader(file_contents)
            
        else:
            keys = request.form.keys()
            count=1
            for i in range(2, len(keys), 5):
                front = request.form["front_"+str(count)]
                back = request.form["back_"+str(count)]
                lang = request.form["lang_"+str(count)]
                lang2 = request.form["lang2_"+str(count)]
                diff = request.form["diff_"+str(count)]
                count+=1
                card = Cards(front=front, back=back, lang_front = lang, lang_back=lang2, score=diff, deck_id=deck.deck_id)
                db.session.add(card)
                db.session.commit()
    
    return render_template('add_decks.html', user=user)
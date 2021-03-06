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
    decks=[]
    # decks = Decks.query.filter(Decks.id==user.id).limit(3)
    decks = db.session.query(Decks).filter(Decks.id==user.id).filter(Decks.last_review!=None).order_by(Decks.last_review.desc())   
    review = db.session.query(Decks).filter(Decks.id==user.id).filter(Decks.last_review==None).order_by(Decks.access_time.desc())
    return render_template('review.html', decks=decks, review=review)

@app.route("/library")
@login_required
def library():
    ## Get decks information
    user = flask_login.current_user
    decks=[]
    # decks = Decks.query.filter(Decks.id==user.id).limit(3)
    decks = db.session.query(Decks).filter(Decks.id==user.id).order_by(Decks.access_time.desc(), Decks.last_review.desc())
    return render_template('library.html', decks=decks)

@app.route("/dashbaord")
@login_required
def dashboard():
    
    ## Get user information
    # uid = session['_user_id']
    # print(uid)
    user = flask_login.current_user

    ## Get decks information
    decks=[]
    decks = db.session.query(Decks).filter(Decks.id==user.id).order_by(Decks.access_time.desc(), Decks.last_review.desc()).limit(3)

    review = db.session.query(Decks).filter(Decks.id==user.id).filter(Decks.last_review==None).order_by(Decks.access_time.desc()).limit(3)

    # incomplete
    # recent decks -  top 3
    # need to be reviewed - top 3
    
    return render_template('dashboard.html', user=user, decks=decks, review=review)


@app.route("/editDecks/<int:deck_id>")
@login_required
def editDecks(deck_id):    
    ## Get user information
    user = flask_login.current_user
    cards = db.session.query(Cards).filter( Cards.deck_id==deck_id ).all()    
    print(cards, deck_id, type(deck_id))
    deck = db.session.query(Decks).filter(Decks.deck_id == deck_id).first()
    return render_template('edit_decks.html', user=user, deck=deck, cards=cards)

@app.route("/deck/<int:deck_id>")
@login_required
def deck(deck_id):
    cards = db.session.query(Cards).filter( Cards.deck_id==deck_id ).all()    
    print(cards, deck_id, type(deck_id))
    deck = db.session.query(Decks).filter(Decks.deck_id == deck_id).first()
    deck_write = Decks.query.get_or_404(deck.deck_id)
    deck_write.last_review = datetime.now()
    db.session.commit()
    return render_template('decks.html', cards=cards, deck=deck)

@app.route("/score/<int:deck_id>", methods=["GET"])
@login_required
def score(deck_id):
  deck = db.session.query(Cards).filter(Cards.deck_id==deck_id).all()
  print(deck, deck[0])
  score = 0
  for card in deck:
    score += card.score 
  score = int(( score/ (len(deck)*3)) * 100 )
  deck_write = Decks.query.get_or_404(deck_id)
  deck_write.score = score
  db.session.commit()
  print(score)
  return render_template('score.html', cards=deck, score=score)

@app.route("/addDecks", methods=["GET", "POST"])
@login_required
def addDecks():
    ## Get user information
    user = flask_login.current_user      
    if request.method == 'POST':
        name = request.form["deck_name"]
        desc = request.form["deck_desc"]
        file = request.files["csvFile"]
        deck = Decks(deck_name=name, deck_description=desc, id=user.id, access_time=datetime.now(), score=0)
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
                diff = 0
                count+=1
                card = Cards(front=front, back=back, lang_front = lang, lang_back=lang2, score=diff, deck_id=deck.deck_id)
                db.session.add(card)
                db.session.commit()
        return redirect('/library')
    
    return render_template('add_decks.html', user=user)
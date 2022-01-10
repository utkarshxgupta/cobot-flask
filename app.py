import aiml
import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Chats(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=False)
    bot = db.Column(db.String(300), nullable=False)
    
kernel = aiml.Kernel()
    
if os.path.isfile("bot_brain.brn"):
   kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles="startup.aiml", commands=["load a", "load b"])
    
@app.route('/delete')
def delete():
    db.session.query(Chats).delete()
    db.session.commit()
    return redirect("/")

@app.route('/', methods=['GET', 'POST'])
def chatbot():    
    chat="Talk to me"
    if request.method=='POST':
        chat = request.form['chat']
        msgs = Chats(user=chat, bot=kernel.respond(chat))        
        db.session.add(msgs)
        db.session.commit()
    
    allMsgs = Chats.query.all()
    now = datetime.now()
    tm = now.strftime("%H:%M")         
    return render_template('index.html',allMsgs=allMsgs, tm=tm)
    
kernel.saveBrain("bot_brain.brn")

if __name__ == "__main__":
    app.run(debug=True)
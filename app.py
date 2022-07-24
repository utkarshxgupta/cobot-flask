import aiml
import os
from chatbot import chatbot
from flask import Flask, render_template, request

app = Flask(__name__)
    
kernel = aiml.Kernel()
    
if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles="startup.xml", commands="load a")
    
@app.route('/darkmode')
def dark():
    pass

@app.route('/')
def home():
    return render_template("index.html")
    
@app.route('/get')
def get_bot_response():
    userText = request.args.get('msg')
    ans = str(kernel.respond(userText))
    if ans=="NOTA":
        ans = str(chatbot.get_response(userText))
    if ans.startswith("The current time"):
        ans = "I don't know that yet. You can ask me about Covid19, its symptoms, precautions, vaccines and treatments. I can also tell jokes and fun facts!. 😄"
    return ans

kernel.saveBrain("bot_brain.brn")

if __name__ == "__main__":
    app.run(debug=True)
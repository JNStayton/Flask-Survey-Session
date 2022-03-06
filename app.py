import re
from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey, personality_quiz, surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title = title, instructions = instructions)
    

@app.route('/questions/<int:idx>')
def survey(idx):
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/alldone')
    if len(responses) < idx or len(responses) > idx:
        flash('Invalid question ID! Please proceed in order.', 'error')
        return redirect(f'/questions/{len(responses)}')
    else: 
        question = satisfaction_survey.questions[idx].question
        choices = satisfaction_survey.questions[idx].choices
        return render_template('questions.html', question=question, choices=choices)

@app.route('/answer', methods=['POST'])
def handle_question():
    responses.append(request.form['answer'])
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/alldone')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/alldone')
def complete():
    return render_template('alldone.html')
from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey, personality_quiz, surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def home():
    """Renders the home template, with survey name and instructions"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title = title, instructions = instructions)
    

@app.route('/start_session', methods=['POST'])
def start_session():
    """Starts the flask session to store survey responses"""
    session["responses"] = []
    return redirect('/questions/0')


@app.route('/questions/<int:idx>')
def survey(idx):
    """Checks the number of responses stored and redirects the survey-taker to the correct question"""
    responses = session["responses"]
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
    """Saves the responses to session; redirects user to next question OR to the completion page if finished"""
    responses = session["responses"]
    responses.append(request.form['answer'])
    session["responses"] = responses
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/alldone')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/alldone')
def complete():
    """Renders the page for a finished survey"""
    return render_template('alldone.html')
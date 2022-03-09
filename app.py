from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, personality_quiz, surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def choose_survey():
    """Choose the survey you want to take; renders the page for that survey"""
    keys = surveys.keys()
    return render_template('choose.html', keys=keys)


@app.route('/survey', methods = ['POST'])
def load_survey():
    survey = request.form['surveys']
    session['survey'] = survey

    return redirect('/survey')

@app.route('/survey')
def home():
    """Renders the home template, with survey name and instructions"""
    key = session['survey']
    survey = surveys[key]
    title = survey.title
    instructions = survey.instructions

    return render_template('home.html', title = title, instructions = instructions)

    
@app.route('/start_session', methods=['POST'])
def start_session():
    """Starts the flask session to store survey responses"""
    session["responses"] = []
    return redirect('/questions/0')


@app.route('/questions/<int:idx>')
def survey(idx):
    """Checks the number of responses stored and redirects the survey-taker to the correct question"""
    key = session['survey']
    survey = surveys[key]
    responses = session["responses"]

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/alldone')
    if len(responses) < idx or len(responses) > idx:
        flash('Invalid question ID! Please proceed in order.', 'error')
        return redirect(f'/questions/{len(responses)}')
    else: 
        question = survey.questions[idx].question
        choices = survey.questions[idx].choices
        allow_text =  survey.questions[idx].allow_text

        return render_template('questions.html', question=question, choices=choices, allow_text=allow_text)


@app.route('/answer', methods=['POST'])
def handle_question():
    """Saves the responses to session; redirects user to next question OR to the completion page if finished"""
    answer = request.form['answer']
    text = request.form.get("text", "")

    responses = session["responses"]
    responses.append({"answer": answer, "text": text})
    session["responses"] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/alldone')
    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/alldone')
def complete():
    """If survey complete, renders alldone.html and displays survey questions and answers"""
    key = session['survey']
    survey = surveys[key]
    questions = [survey.questions[idx].question for idx in range(len(survey.questions))]
    answers = session['responses']
    survey_responses = zip(questions, answers)
    
    """Renders the page for a finished survey"""
    return render_template('alldone.html', survey_responses=survey_responses)
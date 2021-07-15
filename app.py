from flask import Flask, json, request, render_template, redirect, flash, make_response, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "cool"
app.config['TESTING'] = True
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


boggle_game = Boggle()


@app.route("/", methods=['GET', 'POST'])
def boggle_home():
    board = boggle_game.make_board()
    session["board"] = board
    highscore = session.get("highscore", 0)
    num_of_plays = session.get("num_of_plays", 0)

    return render_template("boggle_home.html", board=board, highscore=highscore, num_of_plays=num_of_plays)


@app.route("/check-guess/")
def check_guess():
    guess = request.args["guess"]
    board = session["board"]
    result = boggle_game.check_valid_word(board, guess)
    return jsonify({"result": result})


@app.route("/end-game", methods=["POST"])
def end_game():

    score = request.json['score']
    highscore = session.get('highscore', 0)
    num_of_plays = session.get('num_of_plays', 0)

    session['num_of_plays'] = num_of_plays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(newRecord=score > highscore)

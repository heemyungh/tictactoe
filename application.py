from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

BOARD = 3


@app.route("/")
def index():
    if "board" not in session:
        session["board"] = [[None, None, None], 
                            [None, None, None], 
                            [None, None, None]]
        session["turn"] = "X"
    
    return render_template("game.html", board=session["board"], turn=session["turn"])


@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    session["turn"] = "O" if session["turn"] == "X" else "X"

    if win(session["board"], row, col):
        return render_template("win.html", win=win(session["board"], row, col), board=session["board"])
  
    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    try:
        del session["board"]
        del session["turn"]
    except KeyError:
        pass
    return redirect(url_for("index"))


# checks if the move has ended game
def win(board, row, col):
    piece = board[row][col]
    # check row
    if board[row][wrap(col+1)] == piece and board[row][wrap(col+2)] == piece:
        return piece, (row, col), (row, wrap(col+1)), (row, wrap(col+2))
    # check col
    if board[wrap(row+1)][col] == piece and board[wrap(row+2)][col] == piece:
        return piece, (row, col), (wrap(row+1), col), (wrap(row+2), col)
    # see if piece is on diagonal
    if row == col:
        # down-right diagonal
        if board[wrap(row+1)][wrap(col+1)] == piece and board[wrap(row+2)][wrap(col+2)] == piece:
            return piece, (row, col), (wrap(row+1), wrap(col+1)), (wrap(row+2), wrap(col+2))
    if row + col == 2:
        # down-left diagonal
        if board[wrap(row+1)][wrap(col-1)] == piece and board[wrap(row+2)][wrap(col-2)] == piece:
            return piece, (row, col), (wrap(row+1), wrap(col-1)), (wrap(row+2), col(row-2))
    # either tie or incomplete
    for i in range(3):
        for j in range(3):
            # unplayed move exists
            if not board[i][j]:
                return None
    return "tie"


# lets indices wrap around board
def wrap(n):
    return n % BOARD
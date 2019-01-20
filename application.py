from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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

    if win(session["board"], row, col):
        return render_template("win.html", win=win(session["board"], row, col), board=session["board"])
  
    session["turn"] = "O" if session["turn"] == "X" else "X"
    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    try:
        del session["board"]
        del session["turn"]
    except:
        print("no board")

    return redirect(url_for("index"))


# checks if the move has ended game
def win(board, row, col):
    piece = board[row][col]
    # check row
    if board[row][(col+1)%3] == piece and board[row][(col+2)%3] == piece:
        return piece
    # check col
    elif board[(row+1)%3][col] == piece and board[(row+2)%3][col] == piece:
        return piece
    # see if piece is on diagonal
    if row == 1 and col == 1:
        # check both diagonals
        if (board[0][0] == piece and board[2][2] == piece) or (board[0][2] == piece and board[2][0] == piece):
            return piece
    elif row != 1 and col != 1:
        # check one diagonal
        if row == col:
            if board[(row+1)%3][(col+1)%3] == piece and board[(row+2)%3][(col+2)%3] == piece:
                return piece
        else:
            if board[(row+1)%3][(col-1)%3] == piece and board[(row+2)%3][(col-2)%3] == piece:
                return piece
    # check tie scenario?
    else:
        for i in range(3):
            for j in range(3):
                # unplayed move exists
                if not board[i][j]:
                    return None
        return "tie"

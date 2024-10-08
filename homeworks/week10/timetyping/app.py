import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///typing.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    portfolio = db.execute(
        "SELECT symbol, shares, price, total FROM stock WHERE id = ? ORDER BY symbol", user_id
    )

    user_cash = db.execute(
        "SELECT cash FROM users WHERE id = ?", user_id
    )[0]["cash"]
    
    total_cash = db.execute(
        "SELECT SUM(total) + ? AS total_cash FROM stock WHERE id = ?", user_cash, user_id
    )[0]["total_cash"]
    if total_cash is None:
        total_cash = user_cash

    return render_template("index.html",
                           portfolio=portfolio, user_cash=user_cash, total_cash=total_cash
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        elif request.form.get("password") != request.form.get("confirm_password"):
            return apology("confirm password", 403)
        
        rows = db.execute(
            "SELECT * FROM users WHERE username = :username", username=request.form.get("username")
        )
        if len(rows) > 0:
            return apology("username already exists", 403)
        
        if len(rows) == 0:
            username=request.form.get("username")
            hash=generate_password_hash(request.form.get("password"))

            rows = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
            session["user_id"] = request.form.get("id")

            return redirect("/")

    else:
        return render_template("register.html")

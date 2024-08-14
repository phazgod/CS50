import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
        "SELECT symbol, shares, price, total FROM stock WHERE id = ?", user_id
    )
    
    aggregated_portfolio = {}
    for stock in portfolio:
        symbol = stock['symbol']
        if symbol not in aggregated_portfolio:
            aggregated_portfolio[symbol] = {
                'shares': 0,
                'price': stock['price'],
                'total': 0
            }
        aggregated_portfolio[symbol]['shares'] += stock['shares']
        aggregated_portfolio[symbol]['total'] += stock['total']

    user_cash = db.execute(
        "SELECT cash FROM users WHERE id = ?", user_id
    )[0]["cash"]
    
    total_cash = db.execute(
        "SELECT SUM(total) + ? AS total_cash FROM stock WHERE id = ?", user_cash, user_id
    )[0]["total_cash"]
    
    return render_template("index.html",
                           portfolio=aggregated_portfolio, user_cash=user_cash, total_cash=total_cash
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("q"):
            return apology("missing symbol", 403)
        elif not request.form.get("shares"):
            return apology("missing shares", 403)
        
        q = request.form.get("q")
        quote_data = lookup(q)
        if lookup(q) == None:
            return apology("invalid symbol", 400)
        
        price = quote_data["price"]
        shares = int(request.form.get("shares"))
        total_cost = price * shares
        user_id = session["user_id"]

        user_cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", user_id
        )[0]["cash"]


        if total_cost <= user_cash:
            db.execute(
                "UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id
            )
            db.execute(
                "INSERT INTO stock (id, symbol, shares, price, total) VALUES (?, ?, ?, ?, ?)",
                user_id, q, shares, price, total_cost
            )
            return redirect("/")
        else:
            return apology("Not enough money", 403)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        q = request.form.get("q")
        quote_data = lookup(q)
        if lookup(q) == None:
            return apology("invalid symbol", 400)
        return render_template("quote.html", symbol=quote_data["symbol"], price=quote_data["price"])
    else:
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    if request.method == "POST":
        symbol = request.form.get("symbol")
        input_shares = int(request.form.get("shares"))
        shares = db.execute(
            "SELECT shares FROM stock WHERE id = ? AND symbol = ?", user_id, symbol
        )[0]["shares"]
        if input_shares > shares:
            return apology("too many shares", 400)
        else:
            price = db.execute(
                "SELECT price FROM stock WHERE id = ? AND symbol = ?", user_id, symbol
            )[0]["price"]
            sale_amount = price * input_shares
            
            db.execute(
                "UPDATE stock SET shares = shares - ? WHERE id = ? AND symbol = ?", input_shares, user_id, symbol
            )
            db.execute(
                "DELETE FROM stock WHERE id = ? AND symbol = ? AND shares = 0", user_id, symbol
            )
            db.execute(
                "UPDATE users SET cash = cash + ? WHERE id = ?", sale_amount, user_id
            )
            return redirect("/")
    else:
        symbols = db.execute(
            "SELECT DISTINCT symbol FROM stock WHERE id = ?", user_id
        )
        return render_template("sell.html", symbols=symbols)

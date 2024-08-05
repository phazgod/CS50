import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    # TODO: Add the user's entry into the database
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        if "add_button" in request.form:
            if not name:
                return redirect("/")

            if not month:
                return redirect("/")
            try:
                month = int(month)
            except ValueError:
                return redirect("/")
            if month < 1 or month > 12:
                return redirect("/")

            if not day:
                return redirect("/")
            try:
                day = int(day)
            except ValueError:
                return redirect("/")
            if day < 1 or day > 31:
                return redirect("/")
            
            db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)
            return redirect("/")
        
        if "remove_button" in request.form:
            db.execute("DELETE FROM birthdays WHERE name = ? AND month = ? AND day = ?", name, month, day)
            return redirect("/")

    else:
        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)
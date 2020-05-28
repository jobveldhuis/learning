import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
import time
import re


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # User cash
    user = db.execute("SELECT cash FROM users WHERE id = :id", id = session['user_id'])
    cash = user[0]["cash"]
    value = cash

    # User stocks
    stocks = db.execute("SELECT symbol, amount FROM portfolio WHERE user_id = :user_id AND amount IS NOT 0", user_id = session['user_id'])

    lookup_values = {}
    for stock in stocks:
        lookup_values[stock["symbol"]] = lookup(stock["symbol"])
        value = value + (lookup_values[stock["symbol"]]["price"] * stock["amount"])

    return render_template("index.html", stocks = stocks, lookup_values = lookup_values, cash = cash, total = value)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])

        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Could not find symbol")
        symbol = request.form.get("symbol")
        amount = request.form.get("shares")

        if not int(amount) > 0:
            return apology("You must buy at least 1 share")

        # Only perform the buy operation when enough cash is present
        new_balance = float(cash[0]["cash"]) - (float(stock["price"]) * float(request.form.get("shares")))

        if new_balance >= 0:
            # Remove the money needed for the transaction
            db.execute("UPDATE users SET cash = :new_balance WHERE id = :user_id", \
                new_balance = new_balance, \
                user_id = session["user_id"])

            # Include this transaction into the history
            db.execute("INSERT INTO transaction_history (user_id, symbol, amount, price, timestamp) \
                VALUES (:user_id, :symbol, :amount, :price, :timestamp)", \
                user_id = session["user_id"], \
                symbol = symbol, \
                amount = int(amount), \
                price = stock["price"], \
                timestamp = time.time())

            # Add this to the portfolio of user, first checking whether or not this already exists
            current = db.execute("SELECT amount FROM portfolio WHERE user_id = :user_id AND symbol = :symbol", \
                user_id = session["user_id"], \
                symbol = symbol)

            if not current:
                db.execute("INSERT INTO portfolio (user_id, symbol, amount, last_updated) VALUES (:user_id, :symbol, :amount, :now)", \
                    user_id = session["user_id"], \
                    symbol = symbol, \
                    amount = amount, \
                    now = time.time())

            else:
                new_amount = int(current[0]["amount"]) + int(amount)
                db.execute("UPDATE portfolio SET amount = :amount WHERE user_id = :user_id AND symbol = :symbol", \
                    amount = new_amount, \
                    user_id = session["user_id"], \
                    symbol = symbol)

            flash("Stock was added to your portfolio")
            return redirect('/')

        else:
            return apology("Insufficient cash")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Get the history for user from the database
    history = db.execute("SELECT * FROM transaction_history WHERE user_id = :user_id ORDER BY timestamp DESC", user_id = session["user_id"])

    # Lookup values for each symbol
    lookup_values = {}
    times = {}
    for entry in history:
        lookup_values[entry["symbol"]] = lookup(entry["symbol"])
        times[entry["timestamp"]] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry["timestamp"]))
        entry["price"] = entry["price"] * -1

    return render_template("history.html", history = history, lookup_values = lookup_values, times = times)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
        stock = lookup(request.form.get("symbol"))

        # Check if exists
        if not stock:
            return apology("Could not find symbol")

        return render_template("quoted.html", stock=stock)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Check if username value was inputted
        if not request.form.get("username"):
            return apology("Please provide a valid username")

        # Check if password was inputted
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Please provide a password")

        # Check if passwords match
        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("Passwords do not match")

        # Check if password is safe enough
        # https://www.geeksforgeeks.org/python-program-check-validity-password/
        password = request.form.get("password")
        if (len(password) < 8):
            return apology("Password should contain at least 8 characters")
        if not re.search("[a-z]", password):
            return apology("Password should contain at least one lowercase letter")
        if not re.search("[A-Z]", password):
            return apology("Password should contain at least one uppercase letter")
        if not re.search("[0-9]", password):
            return apology("Password should contain at least one number")
        if not re.search("[_@$!#%^&*()]", password):
            return apology("Password should contain at least one special character")
        if re.search("\s", password):
            return apology("Password should not contain whitespace characters")

        # Check if user already exists in database
        exists = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get('username'))
        if exists:
            return apology("User already exists")

        user = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",\
            username=request.form.get('username'), hash=generate_password_hash(request.form.get('password')))

        session['user_id'] = user
        flash("Welcome! You were succesfully registered!")
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        amount = request.form.get("shares")
        stock = lookup(request.form.get("symbol"))
        # Check if user is in posession of said stock
        user_stock = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id AND symbol = :symbol", \
            user_id = session["user_id"], \
            symbol = symbol)

        if not int(amount) > 0:
            return apology("You must sell at least 1 share")

        if not user_stock:
            return apology("You do not own this stock")

        if int(user_stock[0]["amount"]) < int(amount):
            return apology("You do not have enough stock to sell")

        # Log this new transaction into the database
        db.execute("INSERT INTO transaction_history (user_id, symbol, amount, price, timestamp) \
                VALUES (:user_id, :symbol, :amount, :price, :timestamp)", \
                user_id = session["user_id"], \
                symbol = symbol, \
                amount = -1 * int(amount), \
                price = stock["price"], \
                timestamp = time.time())

        # Update the portfolio
        new_amount = int(user_stock[0]["amount"]) - int(amount)
        db.execute("UPDATE portfolio SET amount = :amount WHERE user_id = :user_id AND symbol = :symbol", \
            amount = new_amount, \
            user_id = session["user_id"], \
            symbol = symbol)

        # Update the users cash
        current_cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
        new_cash = float(current_cash[0]["cash"]) + float(stock["price"]) * int(amount)
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", \
            cash = new_cash, \
            id = session["user_id"])

        flash("Stock was succesfully sold")
        return redirect("/")
    else:
        return render_template("sell.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

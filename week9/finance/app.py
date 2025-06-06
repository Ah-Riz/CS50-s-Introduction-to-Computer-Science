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
    total = 0
    portfolio = []
    try:
        raw_data = check_portfolio(session["user_id"])
        if raw_data != []:
            for row in raw_data:
                portfolio.append(
                    {
                        "id": row["id"],
                        "symbol": row["stock_name"],
                        "shares": row["shares"],
                        "price": usd(row["average_price"]),
                        "total": usd(row["average_price"] * row["shares"]),
                    }
                )
                total += row["shares"] * row["average_price"]
    except Exception:
        pass
    user_cash = get_user_balance(session["user_id"])
    total += user_cash

    return render_template("index.html",portfolio = portfolio, cash = usd(user_cash), total = usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol or not shares:
            return apology("must provide symbol and shares", 400)
        if not shares.isdigit():
            return apology("shares must be a positive integer", 400)
        shares = int(shares)
        
        stock_data = lookup(symbol)
        if not stock_data:
            return apology("invalid symbol", 400)
        price = stock_data["price"]
        
        result = transaction(session["user_id"], "BUY", symbol, shares, price)
        if result == True:
            return redirect("/")
        else:
            return apology("error", 400)
        

        
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    raw_data = get_history(session["user_id"])
    data = []
    for row in raw_data:
        # stock_name, transaction_type, shares, price_per_share, transaction_date
        data.append(
            {
                "symbol": row["stock_name"],
                "type": row["transaction_type"],
                "shares": row["shares"],
                "price": usd(row["price_per_share"]),
                "timestamp": row["transaction_date"],
            }
        )
        # row["price"] = usd(row["price"])
        # row["timestamp"] = row["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
    return render_template("history.html", data=data)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

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
        data = lookup(request.form.get("symbol"))
        if not data:
            return apology("invalid symbol", 400)
        result = {
            "name": data["name"],
            "price": usd(data["price"]),
            "symbol": data["symbol"]
        }
        return render_template("quote.html", result=result)
    
    return render_template("quote.html", result=None)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        print(request.form)
        u_name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not u_name:
            return apology("must provide username", 400)
        elif not password or not confirmation:
            return apology("must provide password", 400)
        elif password != confirmation:
            return apology("password does not match", 400)
        
        if check_username(u_name) > 0:
            return apology("username already exists", 400)

        if not insert_new_user(u_name, password):
            return apology("error", 400)
        else:
            get_id = get_user_id(u_name)
            if not get_id:
                return apology("error retrieving user ID", 400)
            session["user_id"] = get_id
            return redirect("/")
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        print("post")
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol or not shares:
            return apology("must provide symbol and shares", 400)
        if not shares.isdigit():
            return apology("shares must be a positive integer", 400)
        shares = int(shares)
        
        stock_data = lookup(symbol)
        if not stock_data:
            return apology("invalid symbol", 400)
        price = stock_data["price"]

        result = transaction(session["user_id"], "SELL", symbol, shares, price)
        if result == True:
            return redirect("/")
        else:
            return apology("error", 400)
    else:
        return render_template("sell.html", symbols=get_user_symbols(session["user_id"]))

def check_username(username):
    """Check if username already exists in the database."""
    result = db.execute("SELECT * FROM users WHERE username = ?", username)
    return len(result)

def insert_new_user(username, password):
    """Insert a new user into the database."""
    try:
        return db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",username,generate_password_hash(password))
    except Exception as e:
        print(f"Error inserting new user: {e}")
        return False

def get_user_id(username):
    """Get the user ID based on the username."""
    result = db.execute("SELECT id FROM users WHERE username = ?", username)
    return result[0]["id"] if result else None

def transaction(user_id, mode, symbol, shares, price):
    if mode == "BUY":
        balance = get_user_balance(user_id)
        print("q,", balance, price * shares)
        if balance < (price * shares):
            return apology("not enough cash", 400)
    elif mode == "SELL":
        cur_shares = get_user_shares(user_id, symbol)
        if shares > cur_shares:
            return apology("not enough shares", 400)
        
    if update(user_id, mode, symbol, shares, price):
        return True
    else:
        return apology("error", 400)


def get_user_balance(user_id):
    """Get the user's balance based on the user ID."""
    result = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    return result[0]["cash"] if result else None

def update(user_id, mode, symbol, shares, price):
    result = [False, False, False]
    result[0] = update_user_cash(user_id, shares, price, mode)
    result[1] = update_transaction_history(user_id, symbol, shares, price, mode)
    result[2] = update_user_portfolio(user_id, symbol, shares, price, mode)
    if False in result:
        return False
    return True

def update_user_cash(user_id, shares, price, mode):
    """Update the user's cash balance in the database."""
    amount = price * shares
    if mode == "BUY":
        amount = amount * -1
    return db.execute(f"UPDATE users SET cash = cash + (?) WHERE id = ?", amount, user_id)

def update_transaction_history(user_id, symbol, shares, price, mode):
    """Update the transaction history in the database."""
    return db.execute("INSERT INTO transactions (user_id, transaction_type, stock_name, shares, price_per_share, total_amount) VALUES (?, ?, ?, ?, ?, ?)", user_id, mode, symbol, shares, price, shares*price)

def update_user_portfolio(user_id, symbol, shares, price, mode):
    """Update the user's portfolio in the database."""
    print("0")
    if mode == "BUY":
        if check_portfolio(user_id, symbol) != []:
            result = update_portfolio(user_id, symbol, shares, price)
            print("1")
        else:
            result = new_portfolio(user_id, symbol, shares, price)
            print("2")
    else:
        shares = shares * -1
        result = update_portfolio(user_id, symbol, shares, price)
        print("3")
    return result

def check_portfolio(user_id, stock_name = None):
    """Check if the user has the stock in their portfolio."""
    if stock_name:
        result = db.execute("SELECT * FROM portfolio WHERE user_id = ? AND stock_name = ? AND shares >= 0", user_id, stock_name)
    else:
        result = db.execute("SELECT * FROM portfolio WHERE user_id = ? AND shares >= 0", user_id)
    return result

def new_portfolio(user_id, symbol, shares, price):
    """Create a new portfolio entry for the user."""
    res = db.execute("INSERT INTO portfolio (user_id, stock_name, shares, average_price) VALUES (?, ?, ?, ?)", user_id, symbol, shares, price)
    return res

def update_portfolio(user_id, symbol, shares, price):
    """Update the user's portfolio in the database."""
    get_current_data = check_portfolio(user_id, symbol)
    cur_shares = get_current_data[0]["shares"]
    cur_avg_price = get_current_data[0]["average_price"]
    cur_avg_price = (cur_avg_price * cur_shares + price * shares) / shares+cur_shares
    print("cur_shares",cur_shares)
    print("cur_avg_price",cur_avg_price)
    print("price",price)
    print("shares",shares)
    shares = cur_shares + shares

    return db.execute("UPDATE portfolio SET shares = ?, last_updated = CURRENT_TIMESTAMP WHERE user_id = ? AND stock_name = ?", shares, user_id, symbol)

def get_user_symbols(user_id):
    """Get the user's symbols based on the user ID."""
    result = db.execute("SELECT stock_name FROM portfolio WHERE user_id = ? AND shares >= 0", user_id)
    return [row["stock_name"] for row in result]

def get_user_shares(user_id, symbol):
    """Get the user's shares based on the user ID and symbol."""
    result = db.execute("SELECT shares FROM portfolio WHERE user_id = ? AND stock_name = ? AND shares >= 0", user_id, symbol)
    return result[0]["shares"] if result else None

def get_history(user_id):
    """Get the user's transaction history based on the user ID."""
    result = db.execute("SELECT stock_name, transaction_type, shares, price_per_share, transaction_date FROM transactions WHERE user_id = ?", user_id)
    return result
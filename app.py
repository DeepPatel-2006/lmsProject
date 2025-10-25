from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Simple in-memory user store (use a database in real apps)
users = {}

@app.route('/')
def home():
    if "username" in session:
        return render_template("home.html", username=session["username"])
    return redirect(url_for("login"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["username"] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            flash("Username already exists!", "warning")
            return redirect(url_for("signup"))
        else:
            users[username] = password
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("login"))

    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.pop("username", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)

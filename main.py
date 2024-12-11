from flask import Flask, render_template, g, request, redirect, url_for, flash, session
import sqlite3
app = Flask(__name__)
app.secret_key = 'He4D8fi2CtE9Wg7f'
db_location = 'var/talentsphere.db'

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
    return db

@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema3.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        db.execute(
            "INSERT INTO users (firstname, lastname, email, password) VALUES (?, ?, ?, ?)",
            (firstname, lastname, email, password),
        )
        db.commit()

        flash(f"Welcome, {firstname}!  You successfully registered an account.")
        return redirect(url_for("index"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password),
        ).fetchone()
        if user:
            session["user"] = {"email": email, "firstname": user[1]}

            flash(f"Welcome back, {user[1]}")

            return redirect(url_for("index"))
        else:

            flash("Invalid email or password")
            return render_template("login.html")

    return render_template("login.html")

@app.route("/dash")
def dash():
    if "user" in session:
        user = session["user"]
        return f"Welcome, {user['firstname']} {user['lastname']}! logged in"
    else:
        return redirect("/login")

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    flash("You have been logged out.")
    return redirect(url_for("index"))


@app.route("/")
def index():

    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM events WHERE ID = 7 OR ID = 11 OR ID = 3;')
    data = cursor.fetchall()

    return render_template('index.html', data=data)

@app.route("/event/<int:event_id>")
def event_details(event_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()

    if event:
        return render_template('event_details.html', event=event, event_id=event_id)
    else:
        return "Event not found", 404

@app.route("/purchase/<int:event_id>", methods=["POST"])
def purchase(event_id):
    if "user" not in session:
        flash("Please login to purchase a ticket or register if you haven't already.")
        return redirect(url_for("login"))

    db = get_db()
    event = db.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()

    if not event:
        flash("NOT FOUND")
        return redirect(url_for("index"))

    firstname = session["user"].get("firstname")
    email = session["user"].get("email")
    flash(f"Thank you, {firstname}!  Your ticket has been successfully purchased.")

    return render_template("ticket.html", event=event, firstname=firstname, email=email)



@app.route("/inherit")
def inheritsindex():
    return render_template('base.html')

@app.route("/inherit2")
def inheritshome():
    return render_template('home.html')

@app.route("/music")
def music():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM events WHERE category = "music"')
    data = cursor.fetchall()

    return render_template('events.html', pagetitle='Music Events', upcomingtitle='Upcoming Music Events', data=data)

@app.route("/comedy")
def comedy():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM events WHERE category = "comedy"')
    data = cursor.fetchall()

    return render_template('events.html', pagetitle='Comedy Events', upcomingtitle='Upcoming Music Events', data=data)

@app.route("/other")
def allevents():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM events WHERE event_name = 'Event 2'")
    data = cursor.fetchall()

    return render_template('events.html', pagetitle='All Events', data=data)


@app.route("/local")
def local():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM local')
    data = cursor.fetchall()

    return render_template('local.html', pagetitle='Local Events', data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
from flask import Flask, g
import sqlite3

app = Flask(__name__)
db_location = 'var/test.db'

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
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route("/initialdata")
def root():
    db = get_db()
    db.cursor().execute('insert into events ("event_name", "event_date", "event_time", "graphic") values ("test1", "2024-12-12", "12:00:00", "graphic.jpg"), ("test3", "2024-12-12", "12:00:00", "graphic.jpg"), ("test2", "2024-12-12", "12:00:00", "graphic.jpg")')
    db.commit()


    page = []
    page.append('<html><ul>')
    sql = "SELECT id, * FROM events ORDER BY event_name"
    for row in db.cursor().execute(sql):
        page.append('<li>')
        page.append(str(row))
        page.append('</li>')

    page.append('</ul><html>')
    return ''.join(page)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
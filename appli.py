from flask import Flask, g
import mysql.connector

app = Flask(__name__)

def get_db():
    try:
        if 'dbs' not in g:
            g.dbs = mysql.connector.connect(
            host="Inventfk.mysql.pythonanywhere-services.com",
            user="Inventfk",
            password="Cuentauser21",
            database="Inventfk$sqlent"
        )
        return g.dbs
    except Exception as e:
        return str(e)

@app.teardown_appcontext
def close_db(error):
    db = g.pop('dbs', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)

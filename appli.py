from flask import Flask, g
import mysql.connector

app = Flask(__name__)

def get_db():
    if 'dbs' not in g:
        g.dbs = mysql.connector.connect(
            host="InvWeb.mysql.pythonanywhere-services.com",
            user="InvWeb",
            password="Contra21db",
            database="InvWeb$ocdb"
        )
    return g.dbs

@app.teardown_appcontext
def close_db(error):
    db = g.pop('dbs', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)

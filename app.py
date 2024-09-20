from flask import Flask, render_template, request, redirect, url_for, session, g
import mysql.connector
import base64
import requests
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

def b64encode_filter(data):
    if data:
        return base64.b64encode(data).decode('utf-8')
    return ''

app.jinja_env.filters['b64encode'] = b64encode_filter

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
    db = g.pop('db', None)
    if db is not None:
        db.close()

def fetch_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print(f"Error al obtener imagen: {e}")
        return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'office_admin' and password == 'AdminOffice$2024':  
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Credenciales inválidas", 401
    return render_template('login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' in session:
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute('SELECT * FROM Productos')
        products = cur.fetchall()
        return render_template('admin_dashboard.html', products=products)
    else:
        return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if 'admin' in session:
        if request.method == 'POST':
            nombre = request.form['nombre']
            codigo = request.form['codigo']
            precio = request.form['precio']
            img_url = request.form['img_url']

            img_blob = None
            if 'img_file' in request.files:
                img_file = request.files['img_file']
                img_blob = img_file.read()
            elif img_url:
                img_blob = fetch_image(img_url)

            if img_blob is None:
                return "ERROR 400: No se pudo cargar la imagen", 400

            db = get_db()
            cursor = db.cursor()
            cursor.execute('INSERT INTO Productos (nombre, codigo, precio, img) VALUES (%s, %s, %s, %s)', (nombre, codigo, precio, img_blob))
            db.commit()
            return redirect(url_for('admin_dashboard'))

        return render_template('add_product.html')
    else:
        return redirect(url_for('login'))

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'admin' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM Productos WHERE idProducto = %s', (product_id,))
        db.commit()
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/products')
def products():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute('SELECT * FROM Productos')
    products = cur.fetchall()
    return render_template('products.html', products=products)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

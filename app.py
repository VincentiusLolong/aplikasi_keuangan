import email
from unittest import result
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
  
app = Flask(__name__)
  
app.secret_key = 'xyz'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'keuanganku'
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            # membuat variabel untuk mengakses dari form
            username = request.form['username']
            password = request.form['password']
            # mengecek apakah akun sudah ada di mysql 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = %s AND passwords = %s', (username, password))
            # mengambil data dan mengembalikannya dengan respon return
            account = cursor.fetchone()
                # jika ada akun yang terdaftar 
            if account:
                # maka session akan dibuat dibawah ini :
                session['loggedin'] = True
                session['id'] = account['user_id']
                session['username'] = account['username']
                # diarahkan ke homepage
                return redirect(url_for('home'))
            else:
                # akun tidak ada di database
                flash("Incorrect username/password!")
    return render_template('login.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    # check apakah username sudah terdaftar sebelumnya atau belum
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # mengecek akun yang di ketik di mysql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute( "SELECT * FROM accounts WHERE username LIKE %s", [username] )
        account = cursor.fetchone()
        # jika akun tersedia maka error akan muncul seperti :
        if account:
            # serro jika nama akun sudah tersedia
            flash("Account already exists!")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash("Username must contain only characters and numbers!")
        elif not username or not password or not email:
            flash("Incorrect username/password!")
        else:
        # jika akun tidak ada maka data yang dimasukkan di form register valid dan akan diteruskan di mysql database
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username,password,email))
            mysql.connection.commit()
            flash("You have successfully registered!", "success")
            return redirect(url_for('login'))

    elif request.method == 'POST':
        # form tidak diisi maka feedbacknya seperti dibawah ini :
        flash("Please fill out the form!")
    # render template register sebagai main register page
    return render_template('register.html')

@app.route('/home')
def home():
    # check apakah user sudah login
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts_accounting WHERE user_id = %s', ([session['id']]))
        account = cursor.fetchall()
        # jika user login munculkan usernamenya
        return render_template('home.html', account=account)    
    # jika tidak arahkan ke login form
    return redirect(url_for('login'))

@app.route('/about')
def about():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts_accounting WHERE user_id = %s', ([session['id']]))
        account = cursor.fetchall()
        data_pengeluaran = []
        data_pendapatan = []
        for data in account:
            if data['jenis'] == 'pengeluaran':
                data_pengeluaran.append(int(data['rupiah']))
            else:
                data_pendapatan.append(int(data['rupiah']))
        pengeluaran = sum(data_pengeluaran)
        pendapatan = sum(data_pendapatan)
        count = (pendapatan- pengeluaran)
        return render_template('about.html', count=count) 
    return redirect(url_for('login'))
            

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE user_id = %s', ([session['id']]))
        account = cursor.fetchone()
        return render_template("profile.html", account = account)
    return redirect(url_for('login'))  

@app.route('/akuntan', methods =['GET', 'POST'])
def akuntan():
    from datetime import date
    if 'loggedin' in session:
        if request.method == 'POST' and 'rupiah' in request.form and 'jenis' in request.form:
            rupiah = request.form['rupiah']
            jenis = request.form['jenis']
            user_id = [session['id']]
            hari = date.today()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO accounts_accounting VALUES (NULL, %s, %s, %s, %s)', (hari,int(rupiah),jenis,user_id))
            mysql.connection.commit()
            flash("You have successfully registered!", "success")
        elif request.method == 'POST':
                # form tidak diisi maka feedbacknya seperti dibawah ini :
                flash("Please fill out the form!")
        return render_template('akuntanku.html')
    return redirect(url_for('login')) 

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/pendapatan')
def pendapatan():
    # check apakah user sudah login
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts_accounting WHERE user_id = %s AND jenis = "pendapatan"', ([session['id']]))
        account = cursor.fetchall()
        # jika user login munculkan usernamenya
        return render_template('pendapatan.html', account=account)    
    # jika tidak arahkan ke login form
    return redirect(url_for('login'))

@app.route('/pengeluaran')
def pengeluaran():
    # check apakah user sudah login
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts_accounting WHERE user_id = %s AND jenis = "pengeluaran"', ([session['id']]))
        account = cursor.fetchall()
        # jika user login munculkan usernamenya
        return render_template('pendapatan.html', account=account)    
    # jika tidak arahkan ke login form
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
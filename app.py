from flask import Flask, render_template, request, session, redirect, url_for

# for db
import sqlite3

DATABASE = r"C:\Users\jroberts\OneDrive - Trinity Anglican School\PyCharm\SCHOOL\DSO_U2_flask_sql\sports_orders.db"
app = Flask(__name__)

app.secret_key = "flaskLogin"
app.config['SESSION_TYPE'] = 'filesystem'

@app.before_first_request
def before_first_request_func():
    session['isLoggedIn'] = False

@app.route('/')
def home():  # put application's code here
    if session['isLoggedIn'] == True:
        #TODO: get name and details from session

        return render_template("home.html")
    else:
        return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    # only get here if POST form. -- Clicked login
    username = request.form['uname']
    password = request.form['pwd']

    # for debug
    print(f"Username: {username}")
    print(f"Pwd: {password}")

    # if username == "bob" and password == "123":
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    query = "SELECT username, password, role, userID FROM users WHERE username = ?" #sqlInjection attacks
    data = (username,)

    results = cur.execute(query, data).fetchone()

    if results:
        if username == results[0]:
            # user exists and is correct.
            session['isLoggedIn'] = True
            session['user'] = username
            session['role'] = results[2]
            if results[2] == "customer":
                query = "SELECT firstname, lastname FROM customers WHERE userID = ?"
                data = (results[3],)
                results = cur.execute(query, data).fetchone()
                session['user'] = f"{results[0]} {results[1]}"

            conn.close()
            return render_template("home.html")




    conn.close()
    return render_template("login.html", msg="Error Logging in.")

@app.route('/logout')
def logout():
    session.clear()

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()

from flask import current_app as app
from flask import render_template, redirect, request
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

from .routeutils import get_all_continents, get_partners_from_continent

mysql = MySQL(app)


@app.route("/", methods=["GET"])
def root():
    return redirect("/home")


@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html", continents=get_all_continents())


@app.route("/aj-kanat", methods=["GET"])
def aj_kanat():
    return render_template("kanat.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        login_details = request.form
        username = login_details['username']
        password = login_details['password']
        with mysql.connect().cursor() as cur:
            try:
                query = f"select stu_id,password from users where stu_id = {username}"
                cur.execute(query)
                result = cur.fetchall()
                if check_password_hash(result[0][1], password):
                    return render_template("login.html", error="Success") \
                        , {"Refresh": "3; url=/"}
                return render_template("login.html", error="Wrong password")
            except:
                return render_template("login.html", error="Student_ID doesn't not exist [1]")
    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        register_details = request.form
        username = int(register_details['username'])
        password = register_details['password']
        c_password = register_details['confirm_password']

        if password != c_password:
            return render_template('register.html', error='Password is different')

        hashed_pw = generate_password_hash(password)

        with mysql.connect().cursor() as cur:
            try:
                query = (
                    f"INSERT INTO "
                    f"users(stu_id,password) "
                    f"VALUES({username}, '{hashed_pw}')"
                )
                cur.execute(query)
                cur.connection.commit()
                return render_template('register.html', error='Register Succesful, Redirecting to Login Page') \
                    , {"Refresh": "3; url=/login"}
            except:
                return render_template('register.html', error='Kaboom')
    return render_template('register.html')


@app.route("/continent", methods=["GET"])
def continents():
    return render_template("continents.html", continents=get_all_continents())


@app.route("/continent/<continent_name>", methods=["GET"])
def continent(continent_name: str):
    full_cont_name, partners = get_partners_from_continent(continent_name)
    return render_template("continent.html", fcn=full_cont_name, partners=partners)

from flask import current_app as app
from flask import render_template, redirect, request
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

from .routeutils import NavbarLink, ContinentLink

mysql = MySQL(app)

links = [
    NavbarLink("Partner Universities", "/partners"),
    NavbarLink("Buddy Program", "/buddy"),
    NavbarLink("Apply", "/apply"),
    NavbarLink("Scholarships", "/scholarships"),
    NavbarLink("Course Equivalency", "/course-equiv"),
    NavbarLink("FAQ", "/faq"),
]


@app.route("/", methods=["GET"])
def root():
    return redirect("/home")


@app.route("/home", methods=["GET"])
def home():
    with mysql.connect().cursor() as cur:
        def generate_continent(continent: tuple[str]): return ContinentLink(continent)

        query = "select distinct continent from country;"
        cur.execute(query)
        continents = map(generate_continent, cur.fetchall())
        return render_template("home.html", links=links, continents=continents)


@app.route("/aj-kanat", methods=["GET"])
def aj_kanat():
    return render_template("kanat.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        loginDetails = request.form
        id = loginDetails['username']
        password = loginDetails['password']
        with mysql.connect().cursor() as cur:
            try:
                query = f"select stu_id,password from users where stu_id = {id}"
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
        cpassword = register_details['confirm_password']

        if password != cpassword:
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

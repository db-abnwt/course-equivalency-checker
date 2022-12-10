from flask import current_app as app
from flask import render_template, redirect, request
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

from .rutils import get_all_continents, get_partners_from_continent
from .rmodels import PartnerUniversity

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
        return render_template("auth/login.html")
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
                    return render_template("auth/login.html", error="Success") \
                        , {"Refresh": "3; url=/"}
                return render_template("auth/login.html", error="Wrong password")
            except:
                return render_template("auth/login.html", error="Student_ID doesn't not exist [1]")
    return render_template("auth/login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    if request.method == 'POST':
        register_details = request.form
        username = int(register_details['username'])
        password = register_details['password']
        c_password = register_details['confirm_password']

        if password != c_password:
            return render_template('auth/register.html', error='Password is different')

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
                return render_template('auth/register.html', error='Register Succesful, Redirecting to Login Page') \
                    , {"Refresh": "3; url=/login"}
            except:
                return render_template('auth/register.html', error='Kaboom')
    return render_template('auth/register.html')


@app.route("/continent", methods=["GET"])
def continents():
    all_continents = get_all_continents()
    return render_template("partners/continents.html", continents=all_continents)


@app.route("/continent/<continent_name>", methods=["GET"])
def continent(continent_name: str):
    full_continent_name, partners = get_partners_from_continent(continent_name)
    return render_template("partners/continent.html", fcn=full_continent_name, partners=partners)


@app.route("/partner/<int:uni_id>", methods=["GET"])
def partner_by_id(uni_id: int):
    with mysql.connect().cursor() as cur:
        columns = "uni_name, c.name, required_gpa, housing_type, est_cost_max, est_cost_min, map_link, " \
                  "incoming_stu_link, course_open_link "
        query = f"select {columns} " \
                f"from partner_university as p join country c on p.country_id = c.country_id " \
                f"where p.uni_id = {uni_id}"
        cur.execute(query)
        res = cur.fetchone()
        partner_uni = PartnerUniversity.generate(res)
    return render_template("partners/partner.html", u=partner_uni)


@app.route("/apply", methods=["GET"])
def apply():
    return render_template("apply.html")


@app.route("/buddy", methods=["GET"])
def buddy():
    return render_template("buddy.html")

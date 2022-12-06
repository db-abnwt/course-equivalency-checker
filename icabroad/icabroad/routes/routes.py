from flask import render_template, redirect
from flask import current_app as app
from flaskext.mysql import MySQL
from .routeutils import NavbarLink, ContinentLink

mysql = MySQL()

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

from flask import render_template
from flask import current_app as app
from .routeutils import NavbarLink


@app.route("/", methods=["GET"])
def home():
    links = [
        NavbarLink("Partner Universities", "/partners"),
        NavbarLink("Buddy Program", "/partners"),
        NavbarLink("Apply", "/apply"),
        NavbarLink("Scholarships", "/scholarships"),
        NavbarLink("Course Equivalency", "/course-equiv"),
        NavbarLink("FAQ", "/faq"),
    ]
    return render_template("base.html", links=links)


@app.route("/ajkanat", methods=["GET"])
def ajkanat():
    return render_template("kanat.html")

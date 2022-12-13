import pymysql
from flask import Blueprint
from flask import render_template, request
from werkzeug.security import generate_password_hash, check_password_hash

from .rmodels import PartnerUniversity, QuestionAndAnswer, EqualCoursePair, Link
from .rutils import *

mysql = MySQL(app)
routes = Blueprint("routes", __name__)


@app.route("/", methods=["GET"])
def root():
    return redirect("/home")


@app.route("/home", methods=["GET"])
def home():
    all_continents = get_all_continents()
    with mysql.connect().cursor() as cur:
        query = f"select url " \
                f"from links " \
                f"where link_name = 'exchange_info'"
        cur.execute(query)
        info_sesh_link, = cur.fetchone()
    return render_template("home.html", continents=all_continents, info_sesh_link=info_sesh_link)


@app.route("/aj-kanat", methods=["GET"])
def aj_kanat():
    return render_template("easter-egg.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        login_details = request.form
        username = login_details['username']
        password = login_details['password']
        with mysql.connect().cursor() as cur:
            try:
                query = f"select username, password from users where username = '{username}'"
                cur.execute(query)
                result = cur.fetchall()
                if check_password_hash(result[0][1], password):
                    session["logged_in"] = True
                    return render_template("auth/login.html", error="Success"), \
                        {"Refresh": "2; url=/admin"}
                return render_template("auth/login.html", error="Wrong username or password")
            except:
                return render_template("auth/login.html", error="Wrong username or password")

    return render_template("auth/login.html")


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("logged_in", None)
    return redirect("/home")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    if request.method == 'POST':
        register_details = request.form
        username = register_details['username']
        password = register_details['password']
        c_password = register_details['confirm_password']

        if password != c_password:
            return render_template('auth/register.html', error='Password is different')

        hashed_pw = generate_password_hash(password)

        with mysql.connect().cursor() as cur:
            try:
                query = (
                    f"INSERT INTO "
                    f"users(username, password) "
                    f"VALUES('{username}', '{hashed_pw}')"
                )
                cur.execute(query)
                cur.connection.commit()
                return render_template('auth/register.html', error='Register Successful, Redirecting to Login Page'), \
                    {"Refresh": "2; url=/login"}
            except pymysql.err.OperationalError:
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
    return render_template("tabs/apply.html")


@app.route("/admin", methods=["GET"])
@login_required
def admin():
    return render_template("admin/admin.html")


@app.route("/admin/<zone>", methods=["GET", "POST"])
@login_required
def admin_zone(zone: str):
    countries = get_all_countries()
    if request.method == 'GET':
        args = request.args.get('uni')
        if args:
            partner_info = get_partners_from_name(args)
            return render_template("admin/admin.html", zone=zone, countries=countries,
                                   universities=get_all_universities(),
                                   fill=partner_info[0])
        pn_courses, ic_courses = get_all_courses()
        return render_template("admin/admin.html", zone=zone, countries=countries, universities=get_all_universities(),
                               approved_courses=get_all_approved_courses(), pn_courses=pn_courses,
                               ic_courses=ic_courses)
    elif request.method == 'POST':
        uni_details = request.form
        none_list = tuple(int(i) if i.isdigit() else (i if i != "" else None) for i in list(uni_details.values())[1:])
        add_partners(none_list)
        return render_template("admin/admin.html", zone=zone, countries=countries)


@app.route("/admin/partner/edit", methods=["POST"])
@login_required
def edit_partner():
    uni_details = list(request.form.values())
    index = uni_details[0]
    none_list = tuple(int(i) if i.isdigit() else (i if i != "" else None) for i in uni_details[1:])
    edit_partners(none_list, index)
    return redirect('/admin/partner')


@app.route("/admin/partner/delete/<name>", methods=["GET"])
@login_required
def delete_partner(name: str):
    delete_partners(name)
    return redirect('/admin/partner')


@app.route("/admin/linker/<state>", methods=["POST"])
@login_required
def course_link(state):
    link_details = tuple(request.form.values())
    if state == 'link':
        link_courses(link_details)
    else:
        unlink_courses(link_details)
    return redirect('/admin/linker')


@app.route("/admin/course/<state>", methods=["POST"])
@login_required
def crud_course(state):
    course_details = tuple(request.form.values())
    none_list = tuple(int(i) if i.isdigit() else (i if i != "" else None) for i in course_details)
    match state:
        case 'add_pn':
            add_partner_course(none_list)
        case 'add_ic':
            add_ic_course(none_list)
        case 'del_pn':
            del_partner_course(none_list)
        case 'del_ic':
            del_ic_course(none_list)
        case 'edit_pn':
            edit_partner_course(none_list)
        case 'edit_ic':
            edit_ic_course(none_list)

    return redirect("/admin/course")


@app.route("/admin/links/", methods=["GET", "POST"])
def links():
    with mysql.connect().cursor() as cur:
        if request.method == "GET":
            query = f"select link_name, url " \
                    f"from links;"
            cur.execute(query)
            raw_links = cur.fetchall()
            all_links = list(map(Link.generate_link, raw_links))
            return render_template("admin/crud_links.html", links=all_links)
        new_url = request.form["url"]
        link_name = request.form["name"]
        query = f"update links " \
                f"set url = '{new_url}' " \
                f"where link_name = '{link_name}'"
        cur.execute(query)
        cur.connection.commit()
        return redirect("/admin/links/")


@app.route("/buddy", methods=["GET"])
def buddy():
    with mysql.connect().cursor() as cur:
        query = f"select url " \
                f"from links " \
                f"where link_name = 'buddy_register'"
        cur.execute(query)
        link, = cur.fetchone()
    return render_template("tabs/buddy.html", buddy_registration_link=link)


@app.route("/faq", methods=["GET"])
def faq():
    with mysql.connect().cursor() as cur:
        query = f"select question, answer " \
                f"from faq"
        cur.execute(query)
        raw_res = cur.fetchall()
        qas = list(map(QuestionAndAnswer.generate_qa, raw_res))
    return render_template("tabs/faq.html", qas=qas)


@app.route("/course-equiv", methods=["GET"])
def course_equiv():
    with mysql.connect().cursor() as cur:
        equiv_course_query = f"select pu.uni_name, pc.pn_cid, pc.pn_name, ic.ic_cid, ic.ic_name " \
                             f"from partner_course pc " \
                             f"join approved_course ac on pc.n_id = ac.n_id " \
                             f"join ic_course ic on ic.c_id = ac.c_id " \
                             f"join partner_university pu on pc.uni_id = pu.uni_id;"
        cur.execute(equiv_course_query)
        raw_pairings = cur.fetchall()
        equal_courses = map(EqualCoursePair.generate_pair, raw_pairings)

        link_query = f"select url " \
                     f"from links " \
                     f"where link_name = 'course_equiv'"
        cur.execute(link_query)
        raw_link = cur.fetchone()
        request_form, = raw_link
    return render_template("tabs/course-equiv.html", ecs=equal_courses, request_form=request_form)


@app.route("/course-equiv/search", methods=["GET"])
def course_equiv_search():
    params = request.args
    with mysql.connect().cursor() as cur:
        query = create_course_search_query(params)
        cur.execute(query)
        raw_pairings = cur.fetchall()
        equal_courses = map(EqualCoursePair.generate_pair, raw_pairings)
    return render_template("tabs/course-equiv.html", ecs=equal_courses)

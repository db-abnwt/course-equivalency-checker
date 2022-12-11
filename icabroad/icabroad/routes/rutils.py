from typing import Tuple, Any, Dict

from flaskext.mysql import MySQL
from flask import current_app as app
from .rmodels import ContinentLink, PartnerLink

mysql = MySQL(app)


def get_all_continents() -> list[ContinentLink]:
    with mysql.connect().cursor() as cur:
        query = "select distinct continent from country;"
        cur.execute(query)
        return list(map(ContinentLink.generate_continent, cur.fetchall()))


def get_partners_from_continent(continent_name: str) -> tuple[str, dict[list[PartnerLink]]]:
    with mysql.connect().cursor() as cur:
        all_countries_query = f"select country_id, name, continent " \
                              f"from country " \
                              f"where lower(replace(continent, ' ', '')) = '{continent_name}'"
        cur.execute(all_countries_query)
        all_countries = cur.fetchall()

        country2partners = {}
        for cid, country, _ in all_countries:
            partners_in_country_query = f"select uni_id, uni_name " \
                                        f"from partner_university " \
                                        f"where country_id = {cid}"
            cur.execute(partners_in_country_query)
            partners_in_country = cur.fetchall()
            country2partners[country] = list(map(PartnerLink.generate_partner_link, partners_in_country))

        return all_countries[0][2], country2partners


def get_all_countries() -> list[tuple[int, str]]:
    with mysql.connect().cursor() as cur:
        all_countries_query = f"select * " \
                              f"from country "
        cur.execute(all_countries_query)
        all_countries = cur.fetchall()

    # print(all_countries)
    return all_countries


def get_all_universities() -> tuple[Any, dict[Any, Any]]:
    with mysql.connect().cursor() as cur:
        all_universities_query = f"select * " \
                                 f"from partner_university "
        cur.execute(all_universities_query)
        all_universities = cur.fetchall()

    return all_universities


def get_partners_from_name(name: str) -> Any | None:
    with mysql.connect().cursor() as cur:
        find_uni_query = f"select * " \
                         f"from partner_university " \
                         f"where uni_name = '{name}';"
        cur.execute(find_uni_query)
        partner_info = cur.fetchall()

    return partner_info


def add_partners(res: tuple[Any, ...]):
    with mysql.connect().cursor() as cur:
        add_uni_query = "INSERT INTO " \
                        "partner_university(uni_name, country_id, required_gpa, housing_type, " \
                        "est_cost_max, est_cost_min, map_link, incoming_stu_link, course_open_link) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(add_uni_query, res)
        cur.connection.commit()
    return


def edit_partners(res: tuple[Any, ...], index):
    with mysql.connect().cursor() as cur:
        edit_uni_query = "UPDATE partner_university " \
                         "SET uni_name = %s, country_id = %s," \
                         "required_gpa = %s, housing_type = %s," \
                         "est_cost_max = %s, est_cost_min = %s," \
                         "map_link = %s, incoming_stu_link = %s," \
                         "course_open_link = %s " \
                         f"WHERE uni_id = {index};"
        cur.execute(edit_uni_query, res)
        cur.connection.commit()
    return


def delete_partners(name: str):
    with mysql.connect().cursor() as cur:
        delete_uni_query = "DELETE FROM partner_university   WHERE uni_name = %s"
        cur.execute(delete_uni_query, name)
        cur.connection.commit()
    return


def get_all_approved_courses():
    with mysql.connect().cursor() as cur:
        approved_courses_query = """select a.id, c.uni_name, b.pn_cid, b.pn_name, d.ic_cid, d.ic_name, a.n_id, a.c_id
                                    from approved_course as a
                                             left join partner_course as b on a.n_id = b.n_id
                                             left join partner_university as c on b.uni_id = c.uni_id
                                             left join ic_course as d on a.c_id = d.c_id; """
        cur.execute(approved_courses_query)
        approved_course_info = cur.fetchall()
    return approved_course_info


def get_all_courses():
    with mysql.connect().cursor() as cur:
        pn_course_query = """select a.uni_id, b.uni_name, a.pn_cid, a.pn_name, a.credits, a.major, a.n_id
                                    from partner_course as a 
                                        left join partner_university as b on a.uni_id = b.uni_id"""
        cur.execute(pn_course_query)
        all_pn_course = cur.fetchall()

        ic_course_query = """select * from ic_course"""
        cur.execute(ic_course_query)
        all_ic_course = cur.fetchall()
    return all_pn_course, all_ic_course


def link_courses(tup):
    with mysql.connect().cursor() as cur:
        link_course_query = "insert into approved_course(n_id, c_id) values(%s, %s)"
        cur.execute(link_course_query, tup)
        cur.connection.commit()
    return


def unlink_courses(tup):
    with mysql.connect().cursor() as cur:
        unlink_course_query = "delete from approved_course where n_id = %s and c_id = %s"
        cur.execute(unlink_course_query, tup)
        cur.connection.commit()
    return


def add_partner_course(tup):
    with mysql.connect().cursor() as cur:
        add_partner_query = "insert into partner_course(uni_id, pn_cid, major, credits, pn_name) values(%s, %s, %s, %s, %s)"
        cur.execute(add_partner_query, tup)
        cur.connection.commit()
    return


def add_ic_course(tup):
    with mysql.connect().cursor() as cur:
        add_partner_query = "insert into ic_course(ic_cid, major, credits, ic_name) values(%s, %s, %s, %s)"
        cur.execute(add_partner_query, tup[:4])
        cur.connection.commit()
    return


def del_partner_course(tup):
    with mysql.connect().cursor() as cur:
        del_partner_query = "delete from partner_course where n_id = %s"
        cur.execute(del_partner_query, tup[-1])
        cur.connection.commit()
    return


def del_ic_course(tup):
    with mysql.connect().cursor() as cur:
        del_ic_query = "delete from ic_course where c_id = %s"
        cur.execute(del_ic_query, tup[-1])
        cur.connection.commit()
    return


def edit_partner_course(tup):
    with mysql.connect().cursor() as cur:
        del_partner_query = "update partner_course set uni_id = %s, pn_cid = %s, " \
                            "major = %s, credits = %s, pn_name = %s " \
                            "where n_id = %s"
        cur.execute(del_partner_query, tup)
        cur.connection.commit()
    return


def edit_ic_course(tup):
    with mysql.connect().cursor() as cur:
        del_partner_query = "update ic_course set ic_cid = %s, major = %s, " \
                            "credits = %s, ic_name = %s " \
                            "where c_id = %s"
        cur.execute(del_partner_query, tup)
        cur.connection.commit()
    return


def create_course_search_query(rq_params: dict[str, str]):
    criteria = rq_params["criteria"].lower()
    search_term = rq_params["searchTerm"].lower()
    base_query = f"select pu.uni_name, pc.pn_cid, pc.pn_name, ic.ic_cid, ic.ic_name " \
                 f"from partner_course pc " \
                 f"join approved_course ac on pc.n_id = ac.n_id " \
                 f"join ic_course ic on ic.c_id = ac.c_id " \
                 f"join partner_university pu on pc.uni_id = pu.uni_id "
    extension = ""
    match criteria:
        case "country":
            extension = f"join country c on pu.country_id = c.country_id " \
                        f"where lower(c.name) = '{search_term}'"
        case "major":
            extension = f"where lower(ic.major) = '%{search_term}%'"
        case "host course name":
            extension = f"where lower(pc.pn_name) = '{search_term}' " \
                        f"or lower(pc.pn_cid) = '{search_term}'"
        case "muic course name":
            extension = f"where lower(ic.pn_name) = '{search_term}' " \
                        f"or lower(ic.pn_cid) = '{search_term}'"
        case "host university name":
            extension = f"where lower(pu.uni_name) like '%{search_term}%'"
    return base_query + extension

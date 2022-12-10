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


def add_partners(res: tuple[Any]):
    with mysql.connect().cursor() as cur:
        add_uni_query = "INSERT INTO " \
                        "partner_university(uni_name, country_id, required_gpa, housing_type, " \
                        "est_cost_max, est_cost_min, map_link, incoming_stu_link, course_open_link) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(add_uni_query, res)
        cur.connection.commit()
    return


def edit_partners(res: tuple[Any], index: int):
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
        approved_courses_query = """select a.id, c.uni_name, a.pn_cid, b.pn_name, a.ic_cid, d.ic_name 
                                    from approved_course as a 
                                        left join partner_course as b on a.pn_cid = b.pn_cid 
                                        left join partner_university as c on b.uni_id = c.uni_id 
                                        left join ic_course as d on a.ic_cid = d.ic_cid; """
        cur.execute(approved_courses_query)
        approved_course_info = cur.fetchall()
    return approved_course_info

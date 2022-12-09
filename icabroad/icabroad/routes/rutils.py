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

from flaskext.mysql import MySQL
from flask import current_app as app

mysql = MySQL(app)


class ContinentLink:
    def __init__(self, continent: tuple[str]):
        self.normal, = continent
        self.simple = self.normal.lower().replace(" ", "")

    @staticmethod
    def generate_continent(continent_tup: tuple[str]):
        return ContinentLink(continent_tup)


class PartnerLink:
    def __init__(self, partner: tuple):
        self.uni_id, self.uni_name = partner

    @staticmethod
    def generate_partner_link(partner_tup: tuple):
        return PartnerLink(partner_tup)


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

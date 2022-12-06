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


class PartnerUniversity:
    def __init__(self, partner: tuple):
        self.uni_name = partner[0]
        self.country = partner[1]
        self.required_gpa = partner[2]
        self.housing = partner[3]
        self.c_min = partner[4]
        self.c_max = partner[5]
        self.map = partner[6]
        self.incoming_student = partner[7]
        self.courses = partner[8]

    @staticmethod
    def generate_partner(partner_tup: tuple):
        return PartnerUniversity(partner_tup)


def get_all_continents() -> list[ContinentLink]:
    with mysql.connect().cursor() as cur:
        query = "select distinct continent from country;"
        cur.execute(query)
        return list(map(ContinentLink.generate_continent, cur.fetchall()))


def get_partners_from_continent(continent_name: str):
    with mysql.connect().cursor() as cur:
        query1 = "select uni_name, c.name as name, required_gpa, housing_type, est_cost_min, " \
                 "est_cost_max, map_link, incoming_stu_link, course_open_link " \
                 "from partner_university as p " \
                 "join country as c on p.country_id = c.country_id " \
                 f"where lower(replace(c.continent, ' ', '')) = '{continent_name}';"
        cur.execute(query1)
        partners = list(map(PartnerUniversity.generate_partner, cur.fetchall()))

        query2 = "select continent " \
                 "from country " \
                 f"where lower(replace(continent, ' ', '')) = '{continent_name}';"
        cur.execute(query2)
        full_continent_name = cur.fetchone()[0]

        return full_continent_name, partners

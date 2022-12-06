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


def get_all_continents() -> list[ContinentLink]:
    with mysql.connect().cursor() as cur:
        query = "select distinct continent from country;"
        cur.execute(query)
        return list(map(ContinentLink.generate_continent, cur.fetchall()))

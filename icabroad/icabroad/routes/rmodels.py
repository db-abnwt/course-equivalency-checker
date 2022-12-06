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

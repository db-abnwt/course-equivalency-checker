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


class PartnerUniversity:
    def __init__(self, uni_name, country_name, required_gpa, housing_type, est_cost_max, est_cost_min, map_link,
                 incoming_link, course_link):
        self.name = uni_name
        self.country = country_name
        self.gpa = required_gpa
        self.housing = housing_type
        self.max = est_cost_max
        self.min = est_cost_min
        self.map = map_link
        self.incoming = incoming_link
        self.course = course_link

    @staticmethod
    def generate(uni_response: tuple):
        return PartnerUniversity(
            uni_response[0],
            uni_response[1],
            uni_response[2],
            uni_response[3],
            uni_response[4],
            uni_response[5],
            uni_response[6],
            uni_response[7],
            uni_response[8]
        )


class QuestionAndAnswer:
    def __init__(self, qa_tup: tuple[str, str]):
        self.question, self.answer = qa_tup

    @staticmethod
    def generate_qa(qa_tup: tuple[str, str]):
        return QuestionAndAnswer(qa_tup)


class EqualCoursePair:
    def __init__(self, ce_tup):
        self.pn_uname = ce_tup[0]
        self.pn_cid = ce_tup[1]
        self.pn_cname = ce_tup[2]
        self.ic_cid = ce_tup[3]
        self.ic_cname = ce_tup[4]

    @staticmethod
    def generate_pair(ce_tup):
        return EqualCoursePair(ce_tup)


class Link:
    def __init__(self, tup: tuple[str, str]):
        self.db_name, self.url = tup
        self.pretty_name = self.db_name.replace('_', ' ').title()

    @staticmethod
    def generate_link(tup):
        return Link(tup)

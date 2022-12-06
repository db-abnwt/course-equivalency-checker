from dataclasses import dataclass


@dataclass
class NavbarLink:
    name: str
    url: str


class ContinentLink:
    def __init__(self, continent: tuple[str]):
        self.normal, = continent
        self.simple = self.normal.lower().replace(" ", "")

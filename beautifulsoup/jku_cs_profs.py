import json

import requests
from bs4 import BeautifulSoup

CS_PROFESSORS_URL = "http://informatik.jku.at/research/faculty.phtml"


class Professor:
    def __init__(self, name: str, position: str, phone: str, email: str, room: str, photo_url: str):
        self.name = name
        self.position = position
        self.phone = phone
        self.email = email
        self.room = room
        self.photoUrl = photo_url

    def __str__(self):
        return f"{self.name}, {self.position}, {self.phone}, {self.email}, {self.room}, {self.photoUrl}"


def scrape_jku_cs_profs() -> list[Professor]:
    print("Scraping JKU CS professors...")

    page = requests.get(CS_PROFESSORS_URL)
    soup = BeautifulSoup(page.content, "html.parser", from_encoding="utf-8")

    prof_result_set = soup.find_all("div", class_="team_employee")

    profs: list[Professor] = []

    for prof in prof_result_set:
        info_p = prof.find_next("p")

        x = list(filter(lambda a: len(a) != 0,
                        map(lambda a: a.strip(),
                            map(lambda a: a.text, info_p.contents))))

        profs.append(Professor(x[0], x[1], x[3 + len(x) - 5], x[4 + len(x) - 5], x[2 + len(x) - 5], ""))

    return profs


def main():
    profs = scrape_jku_cs_profs()

    json_dict_array = []
    print("Found %s professors" % len(profs))
    for prof in profs:
        print(prof)
        json_dict = {
            "name": prof.name,
            "position": prof.position,
            "phone": prof.phone,
            "email": prof.email,
            "room": prof.room,
            "photoUrl": prof.photoUrl
        }
        json_dict_array.append(json_dict)

    print(json.dumps(json_dict_array))


if __name__ == '__main__':
    main()

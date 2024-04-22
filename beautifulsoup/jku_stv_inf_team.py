import json

import requests
from bs4 import BeautifulSoup

STV_INF_URL = "https://new.oeh.jku.at/studium/tnf/informatik/team"


class StvTeamMember:
    def __init__(self, name: str, position: str):
        self.name = name
        self.position = position

    def __str__(self):
        return f"{self.name}, {self.position}"


def jku_stv_inf_team() -> list[StvTeamMember]:
    print("Scraping JKU Stv Informatik team members...")

    page = requests.get(STV_INF_URL)
    soup = BeautifulSoup(page.content, "html.parser", from_encoding="utf-8")

    potential_members = soup.find_all("div", class_="section section-separated")

    members: list[StvTeamMember] = []

    for pot_member in potential_members:
        position = pot_member.find_next("div", class_="h6 mb-_5")
        name = pot_member.find_next("h2")

        members.append(StvTeamMember(name.text.strip(), position.text.strip()))

    return members


def main():
    team_members = jku_stv_inf_team()

    json_dict_array = []
    print("Found %s stv team members" % len(team_members))
    for team_member in team_members:
        print(team_member)
        json_dict = {
            "name": team_member.name,
            "position": team_member.position,
        }
        json_dict_array.append(json_dict)

    print(json.dumps(json_dict_array))


if __name__ == '__main__':
    main()

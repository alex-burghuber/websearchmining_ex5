import json

import requests
from bs4 import BeautifulSoup

SIGIR_TEAM_MEMBERS_URL = "https://sigir.org/general-information/officers-and-volunteers/"


class SigirTeamMember:
    def __init__(self, name: str, position: str, email: str):
        self.name = name
        self.position = position
        self.email = email

    def __str__(self):
        return f"{self.name}, {self.position}, {self.email}"


def sigir_officers_volunteers() -> list[SigirTeamMember]:
    print("Scraping Sigir team members...")

    page = requests.get(SIGIR_TEAM_MEMBERS_URL)
    soup = BeautifulSoup(page.content, "html.parser", from_encoding="utf-8")

    member_p_list = soup.find_all("div", class_="entry-content")[0].find_all("p")

    members: list[SigirTeamMember] = []

    for member_p in member_p_list:
        name = member_p.find_next("a").text.strip()
        position = member_p.find_next("strong").text.strip()

        email = next((x for x in map(lambda a: a.text.strip(), member_p.contents) if '@' in x), "")
        members.append(SigirTeamMember(name, position, email))

    return members


def main():
    team_members = sigir_officers_volunteers()

    json_dict_array = []
    print("Found %s sigir team members" % len(team_members))
    for team_member in team_members:
        print(team_member)
        json_dict = {
            "name": team_member.name,
            "position": team_member.position,
            "email": (team_member.email if team_member.email != "" else None)
        }
        json_dict_array.append(json_dict)
    print(json.dumps(json_dict_array))


if __name__ == '__main__':
    main()

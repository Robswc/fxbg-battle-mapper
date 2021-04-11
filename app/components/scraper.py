import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.battles = []
        self.battle_urls = []

    def get_battle_urls(self):
        # get html from wiki page
        url = "https://en.wikipedia.org/wiki/Category:Battles_of_the_American_Civil_War_in_Virginia"
        r = requests.get(url)
        html_doc = r.text

        soup = BeautifulSoup(html_doc, "html.parser")

        # separate the div with all the battle links
        battle_list_div = soup.find("div", class_="mw-category")

        # get links for individual battles and put them into battle_urls
        for link in battle_list_div.find_all("a"):
            url_p1 = "en.wikipedia.org"
            url_p2 = link.get("href")
            full_url = url_p1 + url_p2

            self.battle_urls.append(full_url)

# test code
scraper = Scraper()
scraper.get_battle_urls()
print(scraper.battle_urls)
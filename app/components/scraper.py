import requests
import re
from bs4 import BeautifulSoup
from components.battle import Battle
from geopy.geocoders import Nominatim
import random

def convert_coord(coord):
    r = re.split('[°′″]', coord)
    if len(r) == 3:
        r.insert(2, '00')
    deg, minutes, seconds, direction = r
    return (float(deg) + float(minutes) / 60 + float(seconds) / (60 * 60)) * (-1 if direction in ['W', 'S'] else 1)


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
            url_p1 = "https://en.wikipedia.org"
            url_p2 = link.get("href")
            full_url = url_p1 + url_p2

            self.battle_urls.append(full_url)

        # remove anomoly links
        self.battle_urls.remove("https://en.wikipedia.org/wiki/List_of_American_Civil_War_battles_in_Northern_Virginia")
        self.battle_urls.remove("https://en.wikipedia.org/wiki/Manassas_campaign")
        self.battle_urls.remove("https://en.wikipedia.org/wiki/Battle_of_Clark%27s_House")
        self.battle_urls.remove("https://en.wikipedia.org/wiki/Battle_of_Smithfield")
        self.battle_urls.remove("https://en.wikipedia.org/wiki/Joint_Expedition_Against_Franklin")
        self.battle_urls.remove("https://en.wikipedia.org/wiki/Battle_of_Fairfax_Court_House_(June_1863)")

    def get_battles(self):
        self.battles = []
        self.battle_urls = []

        # get battle urls
        self.get_battle_urls()
        for idx, url in enumerate(self.battle_urls):
            print(url, end=" ")

            r = requests.get(url)  # get html
            print("done")
            html_doc = r.text

            soup = BeautifulSoup(html_doc, "html.parser")  # create bs

            # create battle object
            b = Battle()

            # seperate info table
            main_table = soup.find("table", class_="infobox vevent")
            main_table_rows = main_table.find_all("tr")

            b.wikilink = url

            # name
            first_header = main_table.find("th")  # find first table header, contains battle name
            b.name = first_header.text

            # get table and rows containing date/locations/result
            sub_table = main_table.find("table")
            sub_table_rows = sub_table.find_all("tr")

            # date - first row of sub table
            date = sub_table_rows[0].find("td").text
            b.date_range = date

            # locations - second row of sub table
            data = sub_table_rows[1].find("td")
            loc_div = data.find("div", class_="location")
            locs = loc_div.find_all("a")
            for loc in locs:
                b.locations.append(loc.string)

            # coords
            lat = soup.find_all('span', class_='latitude')
            lng = soup.find_all('span', class_='longitude')
            if lat and lng:
                lat = lat[0].string
                lng = lng[0].string
                lat = convert_coord(lat)
                lng = convert_coord(lng)
                b.coord = [lat, lng]

            # result
            try:
                b.result = sub_table_rows[2].find("td").text
            except:
                b.result = 'Unknown'

            # belligerents
            for i, row in enumerate(
                    main_table_rows):  # loop through rows - side note, im a bit upset i didn't know i could use enumerate() to get the index along with the item when in a for loop like this. this seems very useful
                th = row.find("th")  # get header
                if th is not None:  # check if header exists
                    if th.string == "Belligerents":
                        for idx, j in enumerate(main_table_rows[i + 1].find_all('td')):
                            try:
                                a = [l.string for l in j.find_all('a')]
                            except:
                                a = [l.string for l in j.find_all('p')]
                            if None in a:
                                a.remove(None)
                            try:
                                icon_link = j.find('img')['src']
                            except:
                                icon_link = ''
                            try:
                                b.belligerents.update({idx: {'name': ' '.join(a), 'icon': icon_link}})
                            except:
                                b.belligerents.update({idx: {'name': a[0], 'icon': icon_link}})

            # leaders
            for i, row in enumerate(main_table_rows):
                th = row.find("th")
                if th is not None:
                    if th.string == "Commanders and leaders":
                        for idx, j in enumerate(main_table_rows[i + 1].find_all('td')):
                            a = [l.string for l in j.find_all('a')]
                            a = list(filter(None, a))
                            if '†' in a:
                                a.remove('†')
                            if '' in a:
                                a.remove('')
                            b.leaders.update({idx: {'name': a}})

            # strength
            for i, row in enumerate(main_table_rows):
                th = row.find("th")
                if th is not None:
                    if th.string == "Strength":
                        for idx, j in enumerate(main_table_rows[i + 1].find_all('td')):
                            s = 'Unknown'
                            num = 0
                            try:
                                if j.string is not None:
                                    s = j.string
                                else:
                                    p = j.find_all('p')[0].getText()
                                    s = p
                                    num = re.findall(r'\b\d+\b', s.replace(',', ''))[0]
                            except:
                                pass

                            s = re.sub("[\(\[].*?[\)\]]", "", s)
                            s = s.strip()





                            b.strength.update({idx: {'strength': {'text': s, 'number': num}}})

            # casualties
            for i, row in enumerate(main_table_rows):
                th = row.find("th")
                if th is not None:
                    if th.string == "Casualties and losses":
                        for idx, j in enumerate(main_table_rows[i + 1].find_all('td')):
                            try:
                                a = [j.string.strip()]
                            except:
                                a = ['Unknown']
                            if None in a:
                                a.remove(None)
                            b.casualties.update({idx: {'casualties': ' '.join(a)}})

            self.battles.append(b)
            if 'fredericksburg' in url:
                break

        self.get_lat_long()

        return self.battles

    def get_lat_long(self):
        geolocator = Nominatim(user_agent="battle_mapper")

        for b in self.battles:
            if not b.coord:
                loc_string = ""
                if "Virginia" in b.locations[0]:  # check if location has virgina in it already, if not add it
                    loc_string = b.locations[0]
                else:
                    loc_string = b.locations[0] + ", Virginia"

                print(loc_string, end=" - ")
                location = geolocator.geocode(loc_string)
                lat = location.latitude + random.uniform(-.3, .3)
                b.coord.append(lat)
                lon = location.longitude + random.uniform(-.3, .3)
                b.coord.append(lon)
                print((lat, lon))

#
# def main():
#     print("not right")


# if __name__ == "__main__":
#     main()

# test code
# scraper = Scraper()
# scraper.get_battles()
#
# for b in scraper.battles:
#     b.print_battle()

import requests
from bs4 import BeautifulSoup
from battle import Battle

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
    
    def get_battles(self):
        # get html from wiki page
        url = "https://en.wikipedia.org/wiki/Battle_of_Fredericksburg"
        r = requests.get(url)
        html_doc = r.text

        soup = BeautifulSoup(html_doc, "html.parser")

        # create battle object
        b = Battle()

        # seperate info table
        main_table = soup.find("table", class_="infobox vevent")

        # name
        first_header = main_table.find("th") # find first table header, contains battle name
        b.name = first_header.string

        # get table and rows containing date/locations/result
        sub_table = main_table.find("table")
        sub_table_rows = sub_table.find_all("tr")

        # date - first row of sub table
        date = sub_table_rows[0].find("td").string
        b.date_range = date

        # locations - second row of sub table
        data = sub_table_rows[1].find("td")
        loc_div = data.find("div", class_="location")
        locs = loc_div.find_all("a")
        for loc in locs:
            b.locations.append(loc.string)
        
        # belligerents
        main_table_rows = main_table.find_all("tr")
        for i, row in enumerate(main_table_rows): # loop through rows - side note, im a bit upset i didn't know i could use enumerate() to get the index along with the item when in a for loop like this. this seems very useful
            th = row.find("th") # get header
            if th is not None: # check if header exists
                if th.string == "Belligerents":
                    bellig = main_table_rows[i + 1]

                    a_tags = bellig.find_all("a") # find all a tags and add their text to belligerents
                    for a in a_tags:
                        if a.string is not None:
                            b.belligerents.append(a.string)

                        
                        


        # print
        b.print_battle()




# test code
scraper = Scraper()
scraper.get_battles()
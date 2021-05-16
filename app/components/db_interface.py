import sqlite3
from components.scraper import Scraper
from components.battle import Battle
import json


def add_battles_to_db(battle_list):
    conn = sqlite3.connect('app/data/battles.db')

    c = conn.cursor()
    c.execute('''
    DROP TABLE IF EXISTS battle
    ''')
    c.execute('''
              CREATE TABLE battle (
              id INTEGER PRIMARY KEY ASC, 
              name TEXT NOT NULL, 
              data JSON
              )
              ''')

    idx = 0
    for b in battle_list:
        idx += 1

        # print(type(b.wikilink)) returns type str

        data = {
            'name': b.name,
            'dateRange': b.date_range,
            'locations': b.locations,
            'result': b.result,
            'coord': b.coord,
            'belligerents': b.belligerents,
            'leaders': b.leaders,
            'strength': b.strength,
            'casualties': b.casualties,
            'wikilink': b.wikilink
        }

        # print(type(data.get('link'))) return type str

        params = (idx, str(b.name), json.dumps(data))

        c.execute('''INSERT INTO battle VALUES(?,?,?)''', params)

    conn.commit()
    conn.close()


def get_battles_from_db():
    conn = sqlite3.connect('app/data/battles.db')
    c = conn.cursor()
    c.execute('SELECT * FROM battle')
    battle_list = []
    for i in c.fetchall():

        data = json.loads(i[2])
        b = Battle()
        b.name = data.get('name')
        b.date_range = data.get('dateRange')
        b.locations = data.get('locations')
        b.result = data.get('result')
        b.coord = data.get('coord')
        b.belligerents = data.get('belligerents')
        b.leaders = data.get('leaders')
        b.strength = data.get('strength')
        b.casualties = data.get('casualties')
        b.wikilink = data.get('wikilink') # NoneType when it gets here
        battle_list.append(b)

    for b in battle_list:
        print(b.wikilink)
        pass
    return battle_list


def update_db(update):
    if update:
        s = Scraper()
        add_battles_to_db(s.get_battles())
    # get_battles_from_db()

import json
from battle import Battle


# Function that loads sample json
def load_sample_json():
    with open('sample_battle.json') as j:
        return json.load(j)


class BattleFactory:
    """Factory class, responsible for creating battle objects from json data."""
    def __init__(self):
        self.battle_list = []

    def create_battles(self, json_data):
        """
        Creates Battle objects.
        :param json_data: json list of battle data.
        :return: list of Battle objects.
        """
        for battle_data in json_data:
            self.add_battle(self.create_battle(battle_data))

        return self.battle_list

    def create_battle(self, json_data):
        """
        Creates a battle object, given appropriate json data.
        :param json_data: formatted json data.
        :return: Battle
        """
        b = Battle()
        b.name = json_data.get('name')
        b.date_range = json_data.get('dateRange')
        b.location = json_data.get('loc')
        b.coord = json_data.get('coord')
        b.belligerents = json_data.get('belligerents')
        b.leaders = json_data.get('leaders')
        b.strength = json_data.get('strength')
        b.casualties = json_data.get('casualties')
        return b

    def add_battle(self, battle):
        """
        Setter, channel for adding Battle objs to main battle list.
        :param battle: Battle object.
        :return: void
        """
        print('{} added to battle list.'.format(battle.name))
        self.battle_list.append(battle)


# Testing that BattleFactory correctly creates a battle class.
bf = BattleFactory()
print(bf.create_battle(load_sample_json()).print_battle())

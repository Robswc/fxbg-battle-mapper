class Battle:
    def __init__(self):
        self.name = ""
        self.date_range = []
        self.location = ""
        self.coord = []
        self.belligerents = []
        self.leaders = []
        self.strength = []
        self.casualties = []
    
    def print_battle(self):
        txt = """Name: {n}
        Date Range: {dr}
        Location: {loc}
        Coords: {coord}
        Belligerents: {bel}
        Leaders: {lead}
        Strength: {stren}
        Casualties: {cas}"""

        txt = txt.format(n = self.name,
        dr = self.date_range,
        loc = self.location,
        coord = self.coord,
        bel = self.belligerents,
        lead = self.leaders,
        stren = self.strength,
        cas = self.casualties)

        print(txt)
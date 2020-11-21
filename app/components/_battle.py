

class Battle:
    def __init__(self):
        self.name = ''
        self.date_range = []
        self.loc = ''
        self.coord = []
        self.belligerents = []
        self.leaders = []
        self.strength = []
        self.casualties = []

    def __str__(self):
        return '{}:\n {} | {}'.format(self.name, self.belligerents[0], self.belligerents[1])


    def update(self):
        pass
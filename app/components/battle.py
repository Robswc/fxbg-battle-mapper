import dash_html_components as html

class Battle:
    def __init__(self):
        self.name = ""
        self.date_range = []
        self.locations = []
        self.coord = []
        self.belligerents = []
        self.leaders = []
        self.strength = []
        self.casualties = []
    
    def print_battle(self):
        txt = """Name: {n}
        Date Range: {dr}
        Location: {locs}
        Coords: {coord}
        Belligerents: {bel}
        Leaders: {lead}
        Strength: {stren}
        Casualties: {cas}"""

        txt = txt.format(n = self.name,
        dr = self.date_range,
        locs = self.locations,
        coord = self.coord,
        bel = self.belligerents,
        lead = self.leaders,
        stren = self.strength,
        cas = self.casualties)

        print(txt)

    def render(self):
        """
        to be filled in
        :return: html.Div()
        """

        # Create list for information, based on class attributes.
        info_list = [self.date_range,
                     self.locations,
                     self.coord,
                     self.belligerents,
                     self.leaders,
                     self.strength,
                     self.casualties]

        info_list_html = []
        for item in info_list:
            info_list_html.append(html.Li(item))


        grid = html.Div(
            children=[

                html.H1(self.name, className='battle-header'),
                html.Ul(children=info_list_html)
            ], className='battle-container')

        return grid
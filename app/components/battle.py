import dash_html_components as html


class Battle:
    def __init__(self):
        self.name = ""
        self.date_range = []
        self.locations = []
        self.result = ''
        self.coord = []
        self.belligerents = {}
        self.flags = {}
        self.leaders = {}
        self.strength = {}
        self.casualties = {}
        self.wikilink = ""

    def print_battle(self):
        print(self.name, '\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t'.format(self.date_range,
                                                                           self.locations,
                                                                           self.result,
                                                                           self.leaders,
                                                                           self.belligerents,
                                                                           self.strength,
                                                                           self.wikilink
                                                                           )
              )

    def generate_details(self, info):
        """
        Generates html details and puts them into a dict to be used by renderer.
        :param info:
        :return: dict of html.details
        """
        try:
            date_info = info.get('date').split('-')[0]
        except:
            date_info = info.get('date')

        flags = [
            html.Img(src=info.get('belligerents').get('0').get('icon'), className='flag-icon'),
            html.Img(src=info.get('belligerents').get('1').get('icon'), className='flag-icon')
        ]


        refined = {
            'Date': html.Details(
                children=[
                    html.Summary(date_info, className='flex-col'),

                ]
            ),
            'Locations': html.Details(
                children=[
                    html.Summary(', '.join(info.get('locations')), className='flex-col'),
                    html.Div([
                        html.Div('Latitude: {}'.format(info.get('coordinates')[0])),
                        html.Div('Longitude: {}'.format(info.get('coordinates')[1])),
                    ], className='text-muted')
                ]
            ),
            'Belligerents': html.Details(
                children=[
                    html.Summary(
                        children=[
                            html.Div([flags[0], info.get('belligerents').get('0').get('name')]),
                            html.Div([flags[1], info.get('belligerents').get('1').get('name')]),
                        ], className='flex-col'),
                ]
            ),
            'Leaders': html.Details(
                children=[
                    html.Summary(
                        children=[
                            html.Div([html.Div([flags[0], i]) for i in info.get('leaders').get('0').get('name')]),
                            html.Div([html.Div([flags[1], i]) for i in info.get('leaders').get('1').get('name')]),
                        ], className='flex-col'),
                    html.Div('more details here I guess')
                ]
            ),
            'Strength': html.Details(
                children=[
                    html.Summary(
                        children=[
                            html.Div([flags[0], info.get('strength').get('0').get('strength').get('text')]),
                            html.Div([flags[1], info.get('strength').get('1').get('strength').get('text')]),
                        ], className='flex-col'),
                ]
            ),
            'Casualties': html.Details(
                children=[
                    html.Summary(
                        children=[
                            html.Div([flags[0], info.get('casualties').get('0').get('casualties')]),
                            html.Div([flags[1], info.get('casualties').get('1').get('casualties')]),
                        ], className='flex-col'),
                ]
            ),
            'Link': html.Details(
                children=[
                    html.A(info.get('name'), href=str(info.get('link')), className='flex-col'),
                ]
            )
        }
        return refined

    def render(self):
        """
        to be filled in
        :return: html.Div()
        """

        # Create list for information, based on class attributes.
        info = {
            'name': self.name,
            'date': self.date_range,
            'locations': self.locations,
            'coordinates': self.coord,
            'belligerents': self.belligerents,
            'leaders': self.leaders,
            'strength': self.strength,
            'casualties': self.casualties,
            'link': self.wikilink,
        }

        details = self.generate_details(info)

        info_list_html = []
        for k, v in details.items():
            info_list_html.append(html.Div(
                children=[
                    html.Div(k, className='flex-item-key'),
                    html.Div(v, className='flex-item-value')
                ], className='flex-row'))
            # info_list_html.append(html.Li(item))

        grid = html.Div(
            children=[

                html.Div(
                    children=[
                        html.Div(self.name),
                        html.Span(self.date_range, className='text-muted')
                    ],
                    className='battle-header'),
                html.Hr(),
                html.Div(children=info_list_html, className='flex-col')
            ], className='battle-container')

        return grid

    def __str__(self):
        return str(self.name)

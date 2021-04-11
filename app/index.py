# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup

# Import Controls
from components import controls

# Import App
from app import app

from components.battle import Battle
from components.battle_factory import BattleFactory
from components.scraper import Scraper


# Function that loads sample json
def load_sample_json():
    with open('components/sample_battle.json') as j:
        return json.load(j)


bf = BattleFactory()
bf.add_battle(bf.create_battle(load_sample_json()))
# Creates header, description, and renders map html.

# These lists chould probably start empty and have locations added from the web scraper but
# Richmond is here as a placeholder
latList = [37.5407]
longList = [-77.4360]
textList = ['Richmond']

mapbox_figure = go.Figure(go.Scattermapbox(lat=latList, lon=longList, text=textList,
    marker=go.scattermapbox.Marker(size=9)))
mapbox_figure.update_layout(mapbox_style='carto-darkmatter')
mapbox_figure.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
mapbox_figure.update_layout(height=720)
mapbox_figure.update_layout(mapbox=dict(center=dict(lat=37.4316, lon=-78.6569), zoom=6))

app.layout = html.Div(children=[
    dcc.Loading(
        fullscreen=False,
        type='cube',
        color='#009245',
        children=[
            html.Div(children=[
                # Bootstrap grid
                html.Div(children=[
                    html.Div(children=[
                        html.Div(children=[
                            html.Div(children=[
                                dcc.Graph(figure=mapbox_figure)
                            ], className='card')
                        ], className='col-lg-8'),
                        html.Div(children=[
                            html.Div(children=[
                                controls.help_section,
                                # Battle info render
                                html.Div(bf.battle_list[0].render()),
                                # Footer
                                controls.footer
                            ], className='card', style={'height': '100%'})
                        ], className='col-lg-4')
                    ], className='row'),
                ], className='container', style={'height': '100%;'}),
            ], className='main-container')
        ])
])

if __name__ == '__main__':
    app.run_server(debug=True)

# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import json

from components.battle import Battle
from components.battle_factory import BattleFactory

app = dash.Dash(__name__)


# Function that loads sample json
def load_sample_json():
    with open('components/sample_battle.json') as j:
        return json.load(j)


bf = BattleFactory()
bf.add_battle(bf.create_battle(load_sample_json()))
# Creates header, description, and renders map html.
app.layout = html.Div(children=[
    # Creates header html.
    html.H1(children='Welcome to FXBG-BATTLE-MAPPER'),

    html.Div(children='''
        Plots historical battles on a map.
    '''),

    html.Div(bf.battle_list[0].render()),

    html.Footer(children=[
        html.Div(children=[
            html.A(children='GitHub', href='https://github.com/robswc/fxbg-battle-mapper')
        ], className='footer-element'),

        html.Div(children=[
            html.A(children='About', href='')
        ], className='footer-element'),

        html.Div(children=[
            html.A(children='Contact', href='')
        ], className='footer-element')
    ], className='footer')
])

if __name__ == '__main__':
    app.run_server(debug=True)
# -*- coding: utf-8 -*-

# Run this app with `python index.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import math

# Import Controls
from components import controls

# Import App
from app import app

from components.battle import Battle
from components.scraper import Scraper

# These lists chould probably start empty and have locations added from the web scraper but
# Richmond is here as a placeholder
latList = []
longList = []
textList = []
battleIndex = []
color_list = []
size_list = []

# scrape battles and fill in marker data
# s = Scraper()
# s.get_battles()

# load data from database
from components import db_interface

battles = db_interface.get_battles_from_db()
# print(battles)
for i, b in enumerate(battles):
    latList.append(str(b.coord[0]))
    longList.append(str(b.coord[1]))
    textList.append(str(b.name))
    color = 'gray'
    if 'union' or 'united' in str(b.result).lower():
        color = 'blue'
    if 'confederate' in str(b.result).lower():
        color = 'red'
    if 'inconclusive' in str(b.result).lower():
        color = 'gray'
    color_list.append(color)

    # print('ssssss', b.strength)
    size = 0
    try:
        size += int(b.strength.get('0').get('strength').get('number'))
        size += int(b.strength.get('1').get('strength').get('number'))
        size_list.append(10 * math.log(size, 10))
        print(size)
    except:
        size_list.append(10)

    battleIndex.append(i)

# Creates header, description, and renders map html.
mapbox_figure = go.Figure()
mapbox_figure.add_trace(go.Scattermapbox(lat=latList, lon=longList, text=textList, mode='markers',
                                         marker=go.scattermapbox.Marker(size=size_list, color=color_list),
                                         customdata=battleIndex))
mapbox_figure.update_layout(mapbox_style='carto-darkmatter')
mapbox_figure.update_layout(clickmode="event+select")
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
                                dcc.Graph(id="battle-map", figure=mapbox_figure)
                            ], className='card')
                        ], className='col-lg-8'),
                        html.Div(children=[
                            html.Div(children=[
                                controls.help_section,
                                # Battle info render
                                html.Div(id="battle-output", children=[]),
                                # Footer
                                controls.footer
                            ], className='card', style={'height': '100%'})
                        ], className='col-lg-4')
                    ], className='row'),
                ], className='container', style={'height': '100%;'}),
            ], className='main-container')
        ])
])

# for b in battles:
#     print(b.print_battle())

# update html to show battle info
@app.callback(
    Output("battle-output", "children"),
    Input("battle-map", "clickData"))
def show_battle_info(clickData):
    if clickData is not None:
        print(battles[clickData["points"][0]["customdata"]].print_battle())
        return battles[clickData["points"][0]["customdata"]].render()
    else:
        return html.Div()


if __name__ == '__main__':
    db_interface.update_db(False) # make false to not run scraper
    app.run_server(debug=True)

# debug=True causes scraper code to run twice before the app loads, just the way the debugger works
# turned it off to waste time

# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

# Import Controls
from components import controls

# Import App
from app import app

from components.battle import Battle
from components.scraper import Scraper

# Creates header, description, and renders map html.


# These lists chould probably start empty and have locations added from the web scraper but
# Richmond is here as a placeholder
latList = []
longList = []
textList = []
battleIndex = []

# scrape battles and fill in marker data
s = Scraper()
s.get_battles()

for i, b in enumerate(s.battles):
    latList.append(str(b.coord[0]))
    longList.append(str(b.coord[1]))
    textList.append(str(b.name))
    battleIndex.append(i)

mapbox_figure = go.Figure(go.Scattermapbox(lat=latList, lon=longList, text=textList, mode='markers',
    marker=go.scattermapbox.Marker(size=9), customdata=battleIndex))
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

@app.callback(
    Output("battle-output", "children"),
    Input("battle-map", "clickData"))
def show_battle_info(clickData):
    if clickData is not None:
        return s.battles[clickData["points"][0]["customdata"]].render()
    else:
        return html.Div()

if __name__ == '__main__':
    app.run_server(debug=True)

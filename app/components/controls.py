import dash
import time
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
import base64

logo = base64.b64encode(open('app/assets/img/brand_logo.png', 'rb').read())

footer = html.Footer(children=[
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

help_section = html.Div(
    children=[
        html.Img(src=app.get_asset_url('img/brand_logo.png')),
        html.H1('FXBG-BATTLE-MAPPER'),
        html.P('Explore historical battles that took place in Virginia!'),
        html.P('Click the markers on the map to learn more about each battle.'),
        html.P('Click get started when ready. You can also check out the project on Github!'),
        html.Button('GET STARTED!', id='get-started')
    ],
    className='help-container', id='help-container')


@app.callback(Output('help-container', 'style'),
              Input('get-started', 'n_clicks'))
def get_started_click(n_clicks):
    if n_clicks is None:
        time.sleep(1)
    else:
        time.sleep(0.25)
    try:
        if int(n_clicks) > 0:
            return {'display': 'none'}
    except:
        return {'display': ''}


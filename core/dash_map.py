import random
import json
import dash
import dash_leaflet as dl
from django_plotly_dash import DjangoDash
import dash_leaflet.express as dlx
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import dash_core_components as dcc


app = DjangoDash("MapApp", prevent_initial_callbacks=True)
 
app.layout = html.Div([
    dl.Map([dl.TileLayer(), dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}})],
           id="map", style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
    html.Div(id="text")
])


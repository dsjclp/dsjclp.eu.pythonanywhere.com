import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table as dct
import dash_html_components as html
import pandas as pd

from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output, State
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format

import datetime
from collections import OrderedDict
from dash_table.Format import Sign


from dash_table.Format import Format, Group, Scheme, Symbol

import json




app = DjangoDash("QuoteApp")

app.layout = html.Div(
    [

        html.Div(className='d-sm-flex align-items-center justify-content-between mb-4',
            children=[
                html.Div('Lease quote', className='h3 mb-0 text-gray-800'),
                dbc.Button("Add manual rents", id="manual-rents-button", className="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm")
            ]
        ),


        dbc.CardDeck(
            [
                dbc.Col(className='col-lg-8 col-sm-12',
                    children=[
                        html.Div(className='card border-left-secondary shadow mb-4',
                            children=[
                                html.Div(className='card-body',
                                    children=[
                                        html.Div('Financed amount', className='mb-2 font-weight-bold text-gray-800'),
                                        html.Div(className='input-group mb-3',
                                            children=[
                                                html.Div(className='input-group-prepend',
                                                    children=[
                                                        html.Div('€', className='input-group-text'),
                                                    ]
                                                ),
                                                dcc.Input(id="resultamount", type="text", min=10000, max=100000, step=1000,value=10000, debounce=True, className='form-control'),

                                            ]
                                        ),
                                         dcc.Slider(id='amount-slider',min=10000,max=100000,value=10000,step=1000, updatemode='drag',
                                                    marks={
                                                        10000: {'label': '10K'},
                                                        20000: {'label': '20K'},
                                                        40000: {'label': '40K'},
                                                        50000: {'label': '50K'},
                                                        60000: {'label': '60K'},
                                                        80000: {'label': '80K'},
                                                        100000: {'label': '100K'}
                                                    },
                                                    className='px-1'
                                        ),
                                        html.Div('Residual Value amount', className='mb-2 font-weight-bold text-gray-800'),
                                        html.Div(className='input-group mb-3',
                                            children=[
                                                html.Div(className='input-group-prepend',
                                                    children=[
                                                        html.Div('€', className='input-group-text'),
                                                    ]
                                                ),
                                                dcc.Input(id="resultrv", type="text", min=0, max=300000, step=1000,value=0, debounce=True, className='form-control'),

                                            ]
                                        ),
                                        dcc.Slider(id='rv-slider',min=0,max=30000,value=0,step=5000,updatemode='drag',
                                            marks={
                                                00000: {'label': '0K'},
                                                10000: {'label': '10K'},
                                                20000: {'label': '20K'},
                                                30000: {'label': '30K'}
                                            },
                                            className='px-1'
                                        ), 


                                        html.Div('Duration', className='mb-2 font-weight-bold text-gray-800'),
                                        html.Div(id='wrapper_div',
                                            children=[
                                                html.Div(className='input-group-prepend',
                                                    children=[
                                                        html.Div('€', className='input-group-text'),
                                                           dcc.Input(id="durationInput", type="text", min=12, max=60, step=1,value=24, debounce=True, className='form-control'),
                                               
                                                    ]
                                                ),
                                              dcc.Slider(id='durationSlider',min=12,max=60,value=24,step=1,updatemode='drag',
                                                    marks={
                                                        12: {'label': '12'},
                                                        24: {'label': '24'},
                                                        36: {'label': '36'},
                                                        48: {'label': '48'},
                                                        60: {'label': '60'}
                                                    },
                                                    className='px-1'
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
    ]
)



@app.callback(
    Output('wrapper_div', 'children'),
    [Input('durationInput', 'value'), Input('durationSlider', "value")]
)
def input_update(valueInput, valueSlider):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_id = "durationSlider.value"
    else:
        trigger_id = ctx.triggered[0]['prop_id']

    if trigger_id == "durationSlider.value":
        return [
            # Fill the dots with whatever arguments are in your layout
                                                           html.Div(className='input-group-prepend',
                                                    children=[
                                                        html.Div('€', className='input-group-text'),
                                                            dcc.Input(id="durationInput", type="text", min=12, max=60, step=1,value=valueSlider, debounce=True, className='form-control'),
            
                                                    ]
                                                ),
        dcc.Slider(id='durationSlider',min=12,max=60,value=valueSlider,step=1,updatemode='drag',
                                            marks={
                                                12: {'label': '12'},
                                                24: {'label': '24'},
                                                36: {'label': '36'},
                                                48: {'label': '48'},
                                                60: {'label': '60'}
                                            },
                                            className='px-1',
                                        ),
       ]
    
    if trigger_id == "durationInput.value":
        return [
            # Fill the dots with whatever arguments are in your layout
                                                            html.Div(className='input-group-prepend',
                                                    children=[
                                                        html.Div('€', className='input-group-text'),
                                                            dcc.Input(id="durationInput", type="text", min=12, max=60, step=1,value=valueInput, debounce=True, className='form-control'),
          
                                                    ]
                                                ),
          dcc.Slider(id='durationSlider',min=12,max=60,value=valueInput,step=1,updatemode='drag',
                                            marks={
                                                12: {'label': '12'},
                                                24: {'label': '24'},
                                                36: {'label': '36'},
                                                48: {'label': '48'},
                                                60: {'label': '60'}
                                            },
                                            className='px-1',
                                        ),
        ]
    
    return dash.no_update
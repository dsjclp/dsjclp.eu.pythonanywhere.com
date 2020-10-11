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
                                html.Div(className='card-body',id='wrapper_amount',
                                    children=[
                                        html.Div('Financed amount', className='mb-2 font-weight-bold text-gray-800'),
                                        html.Div(className='input-group mb-3',
                                            children=[
                                                html.Div(className='input-group-prepend',
                                                    children=[
                                                        html.Div('€', className='input-group-text'),
                                                    ]
                                                ),
                                                dcc.Input(id="amountInput", type="text", min=10000, max=100000, step=1000,value=10000, debounce=True, className='form-control'),    
                                            ]
                                        ),
                                        dcc.Slider(id='amountSlider',min=10000,max=100000,value=10000,step=1000,updatemode='drag',
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
                                    ]
                                ),
                                html.Div(className='card-body',id='wrapper_rv',
                                    children=[
                                        html.Div('Residual value', className='mb-2 font-weight-bold text-gray-800'),
                                        html.Div(className='input-group mb-3',
                                            children=[
                                                html.Div(className='input-group-prepend',
                                                    children=[
                                                        html.Div('€', className='input-group-text'),
                                                    ]
                                                ),
                                                dcc.Input(id="rvInput", type="text", min=0, max=30000, step=1000,value=0, debounce=True, className='form-control'),    
                                            ]
                                        ),
                                        dcc.Slider(id='rvSlider',min=0,max=30000,value=0,step=1000,updatemode='drag',
                                            marks={
                                                00000: {'label': '0K'},
                                                10000: {'label': '10K'},
                                                20000: {'label': '20K'},
                                                30000: {'label': '30K'}
                                            },
                                            className='px-1'
                                        ),
                                    ]
                                ),
                                html.Div(className='card-body',id='wrapper_duration',
                                    children=[
                                        html.Div('Duration', className='mb-2 font-weight-bold text-gray-800'),
                                        html.Div(className='input-group mb-3',
                                            children=[
                                                html.Div(className='input-group-prepend',
                                                    children=[
                                                        html.Div('Months', className='input-group-text'),
                                                    ]
                                                ),
                                                dcc.Input(id="durationInput", type="text", min=12, max=84, step=1,value=24, debounce=True, className='form-control'),    
                                            ]
                                        ),
                                        dcc.Slider(id='durationSlider',min=12,max=84,value=24,step=1,updatemode='drag',
                                            marks={
                                                12: {'label': '12M'},
                                                24: {'label': '24M'},
                                                36: {'label': '36M'},
                                                48: {'label': '48M'},
                                                60: {'label': '60M'},
                                                72: {'label': '72M'},
                                                84: {'label': '84M'}
                                            },
                                            className='px-1'
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
                dbc.Col(className='col-lg-4 col-sm-12',
                    children=[
                        html.Div(className='card border-left-success shadow mb-4',
                            children=[
                                html.Div(className='card-header py-3 d-flex flex-row align-items-center justify-content-between',
                                    children=[
                                        html.Div('Your monthly rent', className='m-0 font-weight-bold text-primary'),
                                    ]
                                ),
                                html.Div(className='card-body',
                                    children=[
                                        html.Div(className='row no-gutters align-items-center',
                                            children=[
                                                html.H2(id='result', className='mb-2 font-weight-bold text-gray-800'),
                                            ]
                                        ),
                                        dcc.RadioItems(id='mode',
                                            options=[
                                                {'label': 'Advanced mode', 'value': '01'},
                                                {'label': 'Arrear mode', 'value': '02'}
                                            ],
                                            value='01',
                                            style={"padding": "auto", "max-width": "800px", "margin": "auto"},
                                            labelStyle={'display': 'block'}
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        html.Div(className='card-body',
                            children=[ 
                                html.Img(src="../staticfiles/img/undraw_posting_photo.svg", className='img-fluid px-3 px-sm-4 mt-3 mb-4')
                            ]
                        )
                    ]
                ),
            ],
        ),

                                           
    dbc.CardGroup(
        [

            dbc.Col(className='mb-4',
            children=[
                html.Div(className='card border-bottom-secondary shadow mb-4',
                    children=[
                        html.Div(className='card-header py-3 d-flex flex-row align-items-center justify-content-between',
                            children=[
                                html.Div('Your manual rents', className='m-0 font-weight-bold text-primary'),
                            ]
                        ),
                        html.Div(className='card-body', 
                            children=[
                                html.Div(
                                    children=[
                                        dct.DataTable(
                                        id='table',
                                        columns=[
                                            {"name": ['Year'], "id": "year"},
                                            {"name": [datetime.datetime.now().strftime('%b')], "id": "01", 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=0,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=30)).strftime('%b')], "id": "02",'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=0,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=61)).strftime('%b')], "id": "03",'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=0,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=91)).strftime('%b')], "id": "04",'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=0,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=122)).strftime('%b')], "id": "05",'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=0,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=152)).strftime('%b')], "id": "06", 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=0,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=183)).strftime('%b')], "id": "07", 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=0,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=213)).strftime('%b')], "id": "08", 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=0,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=244)).strftime('%b')], "id": "09", 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=0,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=274)).strftime('%b')], "id": "10", 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=0,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=305)).strftime('%b')], "id": "11", 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=0,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=335)).strftime('%b')], "id": "12", 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=0,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                        ],
                                        data=[],
                                        editable= True,
                                        style_data_conditional=[
                                            {
                                                'if': {'row_index': 'odd'},
                                                'backgroundColor': 'rgb(248, 248, 248)'
                                            },
                                        ],
                                        style_header={
                                            'backgroundColor': 'rgb(230, 230, 230)',
                                            'fontWeight': 'bold'
                                        }
                                        ),
                                        ],
                                    ),
                            ]
                        )
                    ]
                )
            ]
        ),
    ],
    id='table-container',),

        
        dbc.CardGroup(
            [
                 dbc.Col(className='col-sm-12',
                    children=[
                        html.Div(className='card border-left-warning shadow mb-4',
                            children=[
                                html.Div(className='card-header py-3 d-flex flex-row align-items-center justify-content-between',
                                    children=[
                                        html.Div('Your graph', className='m-0 font-weight-bold text-primary'),
                                    ]
                                ),
                                html.Div(className='card-body',
                                    children=[
                                        html.Div(
                                            children=[
                                                        dcc.Graph(id='graph',style={'color': 'rgb(230, 230, 230)'})
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                dbc.Col(className='col-sm-12',
                    children=[
                        html.Div(className='card border-left-primary shadow mb-4',
                            children=[
                                html.Div(className='card-header py-3 d-flex flex-row align-items-center justify-content-between',
                                    children=[
                                        html.Div('Your schedule', className='m-0 font-weight-bold text-primary'),
                                    ]
                                ),
                                html.Div(className='card-body',
                                    children=[
                                        html.Div(
                                            children=[
                                                dct.DataTable(id='schedule',
                                                    data=[],
                                                    columns=[
                                                            {'id': 'date', 'name': 'Date', 'type': 'datetime'},
                                                            {'id': 'rent', 'name': 'Rent', 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=1,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                                            {'id': 'balance',  'name': 'Balance', 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=1,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                                        ],
                                                    page_size=12,
                                                    export_format="csv",
                                                    style_data_conditional=[
                                                        {
                                                            'if': {'row_index': 'odd'},
                                                            'backgroundColor': 'rgb(248, 248, 248)'
                                                        },
                                                    ],
                                                    style_header={
                                                        'backgroundColor': 'rgb(230, 230, 230)',
                                                        'fontWeight': 'bold'
                                                    },
                                                    style_table={
                                                        'font-size': '1.2rem'
                                                    }
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
    ]
)


#callback de mise à jour de la durée
@app.callback(
    Output('wrapper_duration', 'children'),
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
            html.Div('Duration', className='mb-2 font-weight-bold text-gray-800'),
            html.Div(className='input-group mb-3',
                children=[
                    html.Div(className='input-group-prepend',
                        children=[
                            html.Div('Months', className='input-group-text'),
                        ]
                    ),
                    dcc.Input(id="durationInput", type="text", min=12, max=84, step=1,value=valueSlider, debounce=True, className='form-control'),
                ]
            ),
            dcc.Slider(id='durationSlider',min=12,max=84,value=valueSlider,step=1,updatemode='drag',
                marks={
                    12: {'label': '12M'},
                    24: {'label': '24M'},
                    36: {'label': '36M'},
                    48: {'label': '48M'},
                    60: {'label': '60M'},
                    72: {'label': '72M'},
                    84: {'label': '84M'}
    },
                className='px-1'
            ),
        ]
    
    if trigger_id == "durationInput.value":
        return [
            html.Div('Duration', className='mb-2 font-weight-bold text-gray-800'),
            html.Div(className='input-group mb-3',
                children=[
                    html.Div(className='input-group-prepend',
                        children=[
                            html.Div('Months', className='input-group-text'),
                        ]
                    ),
                    dcc.Input(id="durationInput", type="text", min=12, max=84, step=1,value=valueInput, debounce=True, className='form-control'),                         
                    ]
            ),
            dcc.Slider(id='durationSlider',min=12,max=84,value=valueInput,step=1,updatemode='drag',
                marks={
                    12: {'label': '12M'},
                    24: {'label': '24M'},
                    36: {'label': '36M'},
                    48: {'label': '48M'},
                    60: {'label': '60M'},
                    72: {'label': '72M'},
                    84: {'label': '84M'}
                },
                className='px-1'
            ),
        ]
    
    return dash.no_update


#callback de mise à jour de la VR
@app.callback(
    Output('wrapper_rv', 'children'),
    [Input('rvInput', 'value'), Input('rvSlider', "value")]
)
def input_update(valueInput, valueSlider):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_id = "rvSlider.value"
    else:
        trigger_id = ctx.triggered[0]['prop_id']

    if trigger_id == "rvSlider.value":
        return [
            html.Div('Residual value', className='mb-2 font-weight-bold text-gray-800'),
            html.Div(className='input-group mb-3',
                children=[
                    html.Div(className='input-group-prepend',
                        children=[
                            html.Div('€', className='input-group-text'),
                        ]
                    ),
                    dcc.Input(id="rvInput", type="text", min=0, max=30000, step=1000,value="{:0,.2f}".format(valueSlider), debounce=True, className='form-control'),    
                ]
            ),
            dcc.Slider(id='rvSlider',min=0,max=30000,value=valueSlider,step=1000,updatemode='drag',
                marks={
                    00000: {'label': '0K'},
                    10000: {'label': '10K'},
                    20000: {'label': '20K'},
                    30000: {'label': '30K'}
                },
                className='px-1'
            ),
        ]
    
    if trigger_id == "rvInput.value":
        return [
            html.Div('Residual value', className='mb-2 font-weight-bold text-gray-800'),
            html.Div(className='input-group mb-3',
                children=[
                    html.Div(className='input-group-prepend',
                        children=[
                            html.Div('€', className='input-group-text'),
                        ]
                    ),
                    dcc.Input(id="rvInput", type="text", min=0, max=30000, step=1000,value="{:0,.2f}".format(int(valueInput)), debounce=True, className='form-control'),    
                ]
            ),
            dcc.Slider(id='rvSlider',min=0,max=30000,value=int(valueInput),step=1000,updatemode='drag',
                marks={
                    00000: {'label': '0K'},
                    10000: {'label': '10K'},
                    20000: {'label': '20K'},
                    30000: {'label': '30K'}
                },
                className='px-1'
            ),
        ]
    
    return dash.no_update

#callback de mise à jour du montant
@app.callback(
    Output('wrapper_amount', 'children'),
    [Input('amountInput', 'value'), Input('amountSlider', "value")]
)
def input_update(valueInput, valueSlider):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_id = "amountSlider.value"
    else:
        trigger_id = ctx.triggered[0]['prop_id']

    if trigger_id == "amountSlider.value":
        return [
            html.Div('Financed amount', className='mb-2 font-weight-bold text-gray-800'),
            html.Div(className='input-group mb-3',
                children=[
                    html.Div(className='input-group-prepend',
                        children=[
                            html.Div('€', className='input-group-text'),
                        ]
                    ),
                    dcc.Input(id="amountInput", type="text", min=10000, max=100000, step=1000,value="{:0,.2f}".format(valueSlider), debounce=True, className='form-control'),    
                ]
            ),
            dcc.Slider(id='amountSlider',min=10000,max=100000,value=valueSlider,step=1000,updatemode='drag',
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
        ]
    
    if trigger_id == "amountInput.value":
        return [
            html.Div('Financed amount', className='mb-2 font-weight-bold text-gray-800'),
            html.Div(className='input-group mb-3',
                children=[
                    html.Div(className='input-group-prepend',
                        children=[
                            html.Div('€', className='input-group-text'),
                        ]
                    ),
                    dcc.Input(id="amountInput", type="text", min=10000, max=100000, step=1000,value="{:0,.2f}".format(int(valueInput)), debounce=True, className='form-control'),    
                ]
            ),
            dcc.Slider(id='amountSlider',min=10000,max=100000,value=int(valueInput),step=1000,updatemode='drag',
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
        ]
    
    return dash.no_update

# Masquage de la table des loyers manuels
@app.callback(
    Output('table-container', 'style'),
    [Input('manual-rents-button', 'n_clicks')])
def on_button_click(n):
    if n is None:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


# Remplissage de la Table des loyers manuels
@app.callback(
    Output('table', 'data'),
    [Input('durationSlider', 'value'),],
    [State('table', 'data')]
    )
def create_data(durationValue, rows):
    yearref = datetime.datetime.now().year
    durationvalue = int(durationValue)
    # Calcul du nombre de lignes de la table des loyers fixes (1 par tranche de 12 mois de la durée choisie ... +1)
    nblig = int(durationvalue/12)
    # Remplissage
    d = []
    year = yearref
    for p in range(nblig):
        d.append([year,None, None, None, None, None, None, None, None, None, None, None, None])
        year=year+1
    if nblig != durationvalue/12:
        dec = durationvalue - nblig*12
        if dec ==1:
            d.append([year, None, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==2:
            d.append([year,None, None, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==3:
            d.append([year,None, None, None, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==4:
            d.append([year,None, None, None, None, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==5:
            d.append([year,None, None, None, None, None, 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==6:
            d.append([year,None, None, None, None, None, None, 'N/A','N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==7:
            d.append([year,None, None, None, None, None, None, None, 'N/A','N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==8:
            d.append([year,None, None, None, None, None, None, None, None, 'N/A','N/A', 'N/A', 'N/A'])
        elif dec ==9:
            d.append([year,None, None, None, None, None, None, None, None, None, 'N/A','N/A', 'N/A'])
        elif dec ==10:
            d.append([year,None, None, None, None, None, None, None, None, None, None, 'N/A','N/A'])
        elif dec ==11:
            d.append([year,None, None, None, None, None, None, None, None, None, None, None, None])
        else :
            d.append(['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
    df= pd.DataFrame(d, columns=['year',"01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
    return df.to_dict('rows')


# Calcul du loyer inconnu et création du calendrier de loyers
@app.callback(
    Output('schedule', 'data'),
    [
        Input('durationSlider', 'value'),
        Input('amountSlider', 'value'),
        Input('rvSlider', 'value'),
        Input('table', 'data'),
        Input('mode', 'value'),
    ]
    )
def clean_data(durationValue, amountValue, rvValue, rows, modeValue):
    #initialisation de la table schedule  du calendrier des loyers
    rent = []
    i=1
    j=1
    amountvalue = int(amountValue)
    rvvalue = int(rvValue)
    durationValue = int(durationValue)
    for row in rows:
        if(j<= durationValue): 
            rent.append(row['01'])
        j=j+1
        if(j<= durationValue):  
            rent.append(row['02'])
        j=j+1
        if(j<= durationValue):  
            rent.append(row['03'])
        j=j+1
        if(j<= durationValue): 
            rent.append(row['04'])
        j=j+1
        if(j<= durationValue):
            rent.append(row['05'])
        j=j+1
        if(j<= durationValue):
            rent.append(row['06'])
        j=j+1
        if(j<= durationValue):
            rent.append(row['07'])
        j=j+1
        if(j<= durationValue):
            rent.append(row['08'])
        j=j+1
        if(j<= durationValue):
            rent.append(row['09'])
        j=j+1
        if(j<= durationValue):
            rent.append(row['10'])
        j=j+1
        if(j<= durationValue):
            rent.append(row['11'])
        j=j+1
        if(j<= durationValue):
            rent.append(row['12'])
        j=j+1
        i=i+1

    
    #calcul des valeurs actuelles des loyers fixes et des coefficients
    rate = 0.05 /12
    npvvalue = 0
    npvcoeff = 0
    d = []
    k=0

    if modeValue=='01':
        for p in rent:
            #actualisation des values
            val = 0
            if (rent[k] != None) and str(rent[k]).isnumeric():
                val = (int(rent[k]) / pow((1+rate),k))
            #actualisation des coeffts
            coeff = 0
            if (rent[k] == None) or not str(rent[k]).isnumeric():
                coeff = 1 / pow((1+rate),k)
            #cumul des valeurs actualisées
            npvvalue = npvvalue + val
            npvcoeff = npvcoeff + coeff
            k=k+1
        #calcul de la valeur actuelle de la vr
        npvrv = rvvalue / pow((1+rate),durationValue)
        #calcul du montant des loyers en coefficient
        npvfin = amountvalue - npvvalue - npvrv
        #affichage du loyer principal
        if (npvcoeff != 0) :
            npvfin = npvfin / npvcoeff
            npvfin = float(npvfin)
        if (npvfin):
            rentc = float(npvfin)
        #remplissage du calendrier de loyers en mémoire
        rento = []
        crdo= []
        crd = amountvalue
        j=0
        for q in rent:
            rentschedule = rentc
            if rent[j] != None:
                rentschedule = float(rent[j])
            crd = crd - rentschedule
            crd = crd *(1+rate)
            rento.append(rentschedule)
            crdo.append(crd)
            j=j+1

    else:
        for p in rent:
            #actualisation des values
            val = 0
            if (rent[k] != None) and str(rent[k]).isnumeric():
                val = (int(rent[k]) / pow((1+rate),k+1))
            #actualisation des coeffts
            coeff = 0
            if (rent[k] == None) or not str(rent[k]).isnumeric():
                coeff = 1 / pow((1+rate),k+1)
            #cumul des valeurs actualisées
            npvvalue = npvvalue + val
            npvcoeff = npvcoeff + coeff
            k=k+1
        #calcul de la valeur actuelle de la vr
        npvrv = rvvalue / pow((1+rate),durationValue+1)
        #calcul du montant des loyers en coefficient
        npvfin = amountvalue - npvvalue - npvrv
        #affichage du loyer principal
        if (npvcoeff != 0) :
            npvfin = npvfin / npvcoeff
            npvfin = float(npvfin)
        if (npvfin):
            rentc = float(npvfin)
        #remplissage du calendrier de loyers en mémoire
        rento = []
        crdo= []
        crd = amountvalue
        j=0
        for q in rent:
            rentschedule = rentc
            if rent[j] != None:
                rentschedule = float(rent[j])
            crd = crd *(1+rate) - rentschedule
            rento.append(rentschedule)
            crdo.append(crd)
            j=j+1
    #bascule du calendrier de loyers dans la table schedule
    i=0
    j=0
    for p in rent:
        d.append([(datetime.datetime.now()+ datetime.timedelta(days=j)).strftime('%b %Y'), rento[i], crdo[i]])
        i=i+1
        j=j+30
    df= pd.DataFrame(d, columns=["date", "rent", "balance"])
    return df.to_dict('rows')

# Alimentation de la zone résultat
@app.callback(
    Output('result', 'children'),
    [Input('schedule', 'data'),
    Input('table', 'data')])
def result(scheduleRows, manuals):
    a=0
    i=1
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    # calcul du total des loyers manuels
    manualSum = 0
    manualNb = 0
    for manual in manuals:
        for k in months:
            if (manual[k] != None) and str(manual[k]).isnumeric():
                manualSum = manualSum + manual[k]
                manualNb = manualNb + 1
    # calcul du total de tous les loyers
    globalSum = 0
    globalNb = 0
    for scheduleRow in scheduleRows:
        globalSum = globalSum + float(scheduleRow['rent'])
        globalNb = globalNb + 1
    
    # calcul du total des loyers non manuels
    calcSum = globalSum - manualSum
    calclNb = globalNb - manualNb
    # calcul et affichage du loyer non manuel
    return "€ {:0,.1f}".format(float(calcSum/calclNb))

# Production des histogrammes
@app.callback(
    Output('graph', 'figure'),
    [Input('schedule', 'data')])
def update_graph(rows):
    i=0
    rentx = []
    renty = []
    crdx = []
    crdy = []
    for row in rows:
        rentx.append(i)
        renty.append(row['rent'])
        crdx.append(i)
        crdy.append(row['balance'])
        i=i+1
    return {
                'data': [
                {'x': rentx, 'y': renty, 'type': 'bar', 'name': 'rent', 'marker' : { "color" : "#4e73df"}},
                {'x': crdx, 'y': crdy, 'type': 'bar', 'name': 'balance', 'marker' : { "color" : "#f6c23e"}}
            ],
    }
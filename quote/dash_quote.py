import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table as dct
import dash_html_components as html
import pandas as pd

from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output, State
import dash_table.FormatTemplate as FormatTemplate

import datetime


app = DjangoDash("QuoteApp")

card_content_3 = [
    dbc.CardImg(src="../../../core/staticfiles/img/carousel1.jpg", top=True),
    dbc.CardBody(
        [
            html.H5("Card with image", className="card-title"),
            html.P(
                "This card has an image on top, and a button below",
                className="card-text text-xs",
            ),
            dbc.Button("Click me!", color="primary"),
        ]
    ),
]


app.layout = html.Div(
    [
        html.Div(className='d-sm-flex align-items-center justify-content-between mb-4',
            children=[
                html.H3('Lease quote', className='h3 mb-0 text-gray-800'),
                dbc.Button("Add manual rents", id="manual-rents-button", outline=True, color="primary"),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(className='col-xl-3 col-md-12 mb-4',
                    children=[
                        html.Div(className='card border-left-primary shadow h-100 py-2',
                            children=[
                                html.Div(className='card-body',
                                    children=[
                                        html.Div(className='row no-gutters align-items-center',
                                            children=[
                                                html.Div(className='col mr-2',
                                                    children=[
                                                        html.Div("Financed amount", className='font-weight-bold text-primary text-uppercase mb-4'),
                                                        dcc.Slider(id='amount-slider',min=0,max=1500000,value=100000,step=10000,tooltip='always_visible',className='mb-0 style',     marks={
                                                            0: {'label': '0', 'style': {'color': '#77b0b1'}},
                                                            500000: {'label': '500'},
                                                            1000000: {'label': '1000'}
                                                        },),
                                                        html.Div(id='resultamount', className='h4 mt-3 mb-0 font-weight-bold text-gray-600'),
                                                    ]
                                                ),
                                                html.Div(className='col-auto',
                                                    children=[
                                                        html.Div(className='fas fa-poll fa-2x text-gray-300'),
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

                dbc.Col(className='col-xl-3 col-md-12 mb-4',
                    children=[
                        html.Div(className='card border-left-primary shadow h-100 py-2',
                            children=[
                                html.Div(className='card-body',
                                    children=[
                                        html.Div(className='row no-gutters align-items-center',
                                            children=[
                                                html.Div(className='col mr-2',
                                                    children=[
                                                        html.Div("Residual value", className='font-weight-bold text-primary text-uppercase mb-4'),
                                                        dcc.Slider(id='rv-slider',min=0,max=30000,value=0,step=5000,tooltip='always_visible',className='mb-0'),
                                                        html.Div(id='resultrv', className='h4 mt-3 mb-0 font-weight-bold text-gray-600'),
                                                    ]
                                                ),
                                                html.Div(className='col-auto',
                                                    children=[
                                                        html.Div(className='fas fa-poll fa-2x text-gray-300'),
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

                dbc.Col(className='col-xl-3 col-md-12 mb-4',
                    children=[
                        html.Div(className='card border-left-warning shadow h-100 py-2',
                            children=[
                                html.Div(className='card-body',
                                    children=[
                                        html.Div(className='row no-gutters align-items-center',
                                            children=[
                                                html.Div(className='col mr-2',
                                                    children=[
                                                        html.Div("Duration", className='font-weight-bold text-warning text-uppercase mb-4'),
                                                        dcc.Slider(id='duration-slider',min=0,max=84,value=12,step=1,tooltip='always_visible',className='mb-0'),
                                                        html.Div(id='resultduration', className='h4 mt-3 mb-0 font-weight-bold text-gray-600'),
                                                    ]
                                                ),
                                                html.Div(className='col-auto',
                                                    children=[
                                                        html.Div(className='fas fa-clock fa-2x text-gray-300'),
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
        
                dbc.Col(className='col-xl-3 col-md-12 mb-4',
                    children=[
                        html.Div(className='card border-left-success shadow h-100 py-2',
                            children=[
                                html.Div(className='card-body',
                                    children=[
                                        html.Div(className='row no-gutters align-items-center',
                                            children=[
                                                html.Div(className='col mr-2',
                                                    children=[
                                                        html.Div("Monthly rent", className='font-weight-bold text-success text-uppercase mb-4'),
                                                        dcc.Slider(min=0,max=0,className='mb-0 invisible'),
                                                        html.Div(id='result', className='h4 mt-3 mb-0 font-weight-bold text-success'),
                                                    ]
                                                ),
                                                html.Div(className='col-auto',
                                                    children=[
                                                        html.Div(className='fas fa-calculator fa-2x text-gray-300'),
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
        ),

                
    dbc.Row(
        [

            dbc.Col(className='col-md-12',
            children=[
                html.Div(className='card shadow mb-4',
                    children=[
                        html.Div(className='card-header py-3 d-flex flex-row align-items-center justify-content-between',
                            children=[
                                html.H6('Your manual rents', className='m-0 font-weight-bold text-primary'),
                            ]
                        ),
                        html.Div(className='card-body', 
                            children=[
                                html.Div(
                                    children=[
                                        dct.DataTable(
                                        id='table',
                                        css='card border-left-primary shadow h-100 py-2',
                                        columns=[
                                            {"name": ['Year'], "id": "year"},
                                            {"name": [datetime.datetime.now().strftime('%b')], "id": "01"},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=30)).strftime('%b')], "id": "02"},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=61)).strftime('%b')], "id": "03"},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=91)).strftime('%b')], "id": "04"},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=122)).strftime('%b')], "id": "05"},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=152)).strftime('%b')], "id": "06"},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=183)).strftime('%b')], "id": "07"},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=213)).strftime('%b')], "id": "08"},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=244)).strftime('%b')], "id": "09"},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=274)).strftime('%b')], "id": "10"},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=305)).strftime('%b')], "id": "11"},
                                            {"name": [(datetime.datetime.now()+ datetime.timedelta(days=335)).strftime('%b')], "id": "12"},
                                        ],
                                        data=[],
                                        editable= True,
                                        style_data_conditional=[
                                            {
                                                'if': {
                                                    'filter_query': '{12} = "N/A"',
                                                },
                                                'color': 'red',
                                            },
                                            {
                                                'if': {'row_index': 'odd'},
                                                'backgroundColor': 'rgb(248, 248, 248)'
                                            },
                                        ],
                                        style_header={
                                            'backgroundColor': 'rgb(230, 230, 230)',
                                            'fontWeight': 'bold'
                                        }),
                                        ]
                                    ),
                            ]
                        )
                    ]
                )
            ]
        ),
    ],
    id='table-container',),

        
        dbc.Row(
            [
                 dbc.Col(className='col-xl-8 col-md-12',
                    children=[
                        html.Div(className='card shadow mb-4',
                            children=[
                                html.Div(className='card-header py-3 d-flex flex-row align-items-center justify-content-between',
                                    children=[
                                        html.H6('Your monthly rents', className='m-0 font-weight-bold text-primary'),
                                    ]
                                ),
                                html.Div(className='card-body',
                                    children=[
                                        html.Div(
                                            children=[
                                                        dcc.Graph(id='graph',)
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                dbc.Col(className='col-xl-4 col-md-12',
                    children=[
                        html.Div(className='card shadow mb-4',
                            children=[
                                html.Div(className='card-header py-3 d-flex flex-row align-items-center justify-content-between',
                                    children=[
                                        html.H6('Your schedule', className='m-0 font-weight-bold text-primary'),
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
                                                            {'id': 'rent', 'name': 'Your rent', 'type': 'numeric','format': FormatTemplate.money(0)},
                                                            {'id': 'crd', 'name': 'Outstanding', 'type': 'numeric'},
                                                        ],
                                                    page_size=12,
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
    [Input('duration-slider', 'value'),],
    [State('table', 'data')]
    )
def create_data(durationvalue, rows):
    yearref = datetime.datetime.now().year
    # Calcul du nombre de lignes de la table des loyers fixes (1 par tranche de 12 mois de la durée choisie ... +1)
    nblig = int(durationvalue/12)
    # Remplissage
    d = []
    year = yearref
    for p in range(nblig):
        d.append([year,'', '', '', '', '', '', '', '', '', '', '', ''])
        year=year+1
    if nblig != durationvalue/12:
        dec = durationvalue - nblig*12
        if dec ==1:
            d.append([year, '', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==2:
            d.append([year,'', '', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==3:
            d.append([year,'', '', '', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==4:
            d.append([year,'', '', '', '', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==5:
            d.append([year,'', '', '', '', '', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==6:
            d.append([year,'', '', '', '', '', '', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==7:
            d.append([year,'', '', '', '', '', '', '', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==8:
            d.append([year,'', '', '', '', '', '', '', '', 'N/A', 'N/A', 'N/A', 'N/A'])
        elif dec ==9:
            d.append([year,'', '', '', '', '', '', '', '', '', 'N/A', 'N/A', 'N/A'])
        elif dec ==10:
            d.append([year,'', '', '', '', '', '', '', '', '', '', 'N/A', 'N/A'])
        elif dec ==11:
            d.append([year,'', '', '', '', '', '', '', '', '', '', '', 'N/A'])
        else :
            d.append(['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
    df= pd.DataFrame(d, columns=['year',"01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
    return df.to_dict('rows')


# Calcul du loyer inconnu et création du calendrier de loyers
@app.callback(
    Output('schedule', 'data'),
    [
        Input('duration-slider', 'value'),
        Input('amount-slider', 'value'),
        Input('rv-slider', 'value'),
        Input('table', 'data'),
    ]
    )
def clean_data(durationvalue, amountvalue, rvvalue, rows):
    #initialisation de la table schedule  du calendrier des loyers
    rent = []
    i=1
    j=1
    for row in rows:
        if(j<= durationvalue): 
            rent.append(row['01'])
        j=j+1
        if(j<= durationvalue):  
            rent.append(row['02'])
        j=j+1
        if(j<= durationvalue):  
            rent.append(row['03'])
        j=j+1
        if(j<= durationvalue): 
            rent.append(row['04'])
        j=j+1
        if(j<= durationvalue):
            rent.append(row['05'])
        j=j+1
        if(j<= durationvalue):
            rent.append(row['06'])
        j=j+1
        if(j<= durationvalue):
            rent.append(row['07'])
        j=j+1
        if(j<= durationvalue):
            rent.append(row['08'])
        j=j+1
        if(j<= durationvalue):
            rent.append(row['09'])
        j=j+1
        if(j<= durationvalue):
            rent.append(row['10'])
        j=j+1
        if(j<= durationvalue):
            rent.append(row['11'])
        j=j+1
        if(j<= durationvalue):
            rent.append(row['12'])
        j=j+1
        i=i+1
    
    #calcul des valeurs actuelles des loyers fixes et des coefficients
    rate = 0.05 /12
    npvvalue = 0
    npvcoeff = 0
    d = []
    k=0
    for p in rent:
        #actualisation des values
        val = 0
        if (rent[k] != ''):
            val = (float)(float(rent[k]) / pow((1+rate),i))
        #actualisation des coeffts
        coeff = 0
        if (rent[k] == ''):
            coeff = 1 / pow((1+rate),i)
        #cumul des valeurs actualisées
        npvvalue = npvvalue + val
        npvcoeff = npvcoeff + coeff
        k=k+1
    #calcul de la valeur actuelle de la vr
    npvrv = rvvalue / pow((1+rate),durationvalue)
    #calcul du montant des loyers en coefficient
    npvfin = amountvalue - npvvalue - npvrv
    #affichage du loyer principal
    if (npvcoeff != 0) :
        npvfin = npvfin / npvcoeff
        npvfin = int(npvfin)
    if (npvfin):
        rentc = str(npvfin)
    #remplissage du calendrier de loyers en mémoire
    rento = []
    crdo= []
    crd = int(amountvalue)
    j=0
    for q in rent:
        toto = rentc
        if (rent[j] != ''):
            toto = rent[j]
        crd = crd *(1+rate)
        crdfin = int(crd - int(toto))
        crd = crdfin
        rento.append(toto)
        crdo.append(crd)
        j=j+1
    #bascule du calendrier de loyers dans la table schedule
    i=0
    j=0
    for p in rent:
        d.append([(datetime.datetime.now()+ datetime.timedelta(days=j)).strftime('%b %Y'), rento[i], crdo[i]])
        i=i+1
        j=j+30
    df= pd.DataFrame(d, columns=["date", "rent", "crd"])
    return df.to_dict('rows')

# Alimentation de la zone résultat
@app.callback(
    Output('result', 'children'),
    [Input('schedule', 'data')])
def result(rows):
    a=0
    for row in rows:
        a=row['rent']
    return "€ %s" % a

@app.callback(
    Output(component_id='resultamount', component_property='children'),
    [Input(component_id='amount-slider', component_property='value')]
)
def update_output_amount(amount_value):
    return '€ {:,.0f}'.format(amount_value)

@app.callback(
    Output(component_id='resultrv', component_property='children'),
    [Input(component_id='rv-slider', component_property='value')]
)
def update_output_rv(rv_value):
    return '€ {:,.0f}'.format(rv_value)

@app.callback(
    Output(component_id='resultduration', component_property='children'),
    [Input(component_id='duration-slider', component_property='value')]
)
def update_output_duration(input_value):
    return 'Months {}'.format(input_value)

# Production des histogrammes
@app.callback(
    Output('graph', 'figure'),
    [Input('schedule', 'data')])
def update_graph(rows):
    i=0
    x = []
    y = []
    for row in rows:
        x.append(i)
        y.append(row['rent'])
        i=i+1
    return {
     'data': [{
          'x': x,
          'y': y,
          'type': 'bar',
    }],
 }
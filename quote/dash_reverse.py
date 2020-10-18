import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table as dct
import dash_html_components as html
import pandas as pd
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output, State
from dash_table.Format import Format, Group, Scheme, Symbol

import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from core.models import Contract
from core.models import Schedule
from core.models import Step


startdate = datetime.datetime.now()

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

app = DjangoDash("ReverseApp")

app.layout = html.Div(
    [      
        html.Div(id="output-one", className='d-sm-flex align-items-center justify-content-between mb-4',
            children=[
                html.Div('Lease quote', className='h3 mb-0 text-gray-800'),
                dbc.Button("Save quote", id="save_quote_button", className="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm"),
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
                                        html.Div('Rent amount', className='mb-2 font-weight-bold text-gray-800'),
                                        html.Div(className='input-group mb-3',
                                            children=[
                                                html.Div(className='input-group-prepend',
                                                    children=[
                                                        html.Div('€', className='input-group-text'),
                                                    ]
                                                ),
                                                dcc.Input(id="amountInput", type="text", min=100, max=10000, step=100,value=10000, debounce=True, className='form-control'),    
                                            ]
                                        ),
                                        dcc.Slider(id='amountSlider',min=100,max=10000,value=2000,step=100,updatemode='drag',
                                            marks={100: {'label': '100€'},2000: {'label': '2000€'},5000: {'label': '5000€'},10000: {'label': '10000€'},
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
                                                00000: {'label': '0K'},10000: {'label': '10K'},20000: {'label': '20K'},30000: {'label': '30K'}
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
                                                12: {'label': '12M'},24: {'label': '24M'},36: {'label': '36M'},48: {'label': '48M'},60: {'label': '60M'},72: {'label': '72M'},84: {'label': '84M'}
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
                                        html.Div('Your financed amount', className='m-0 font-weight-bold text-primary'),
                                    ]
                                ),
                                html.Div(className='card-body',
                                    children=[
                                        html.Div('Annual rate', className='font-weight-bold text-primary'),
                                        dcc.Slider(id='rateSlider',min=0,max=500,value=500,step=10,updatemode='drag',
                                            marks={
                                                0: {'label': '0%'},100: {'label': '1%'},200: {'label': '2%'},300: {'label': '3%'}, 400: {'label': '4%'}, 500: {'label': '5%'}
                                            },
                                            tooltip = 'always_visible',
                                            className='px-1 mb-2'
                                        ),
                                        html.Div(className='row no-gutters align-items-center',
                                            children=[
                                                html.H4(id='result', className='font-weight-bold text-gray-800'),
                                            ]
                                        ),
                                        dbc.RadioItems(id='mode', className = 'mb-2 radioitems',
                                            options=[
                                                {'label': 'Advanced mode', 'value': '01'},
                                                {'label': 'Arrear mode', 'value': '03'}
                                            ],
                                            value='01',
                                            inline=True,
                                        ),
                                        dbc.RadioItems(id='manual',
                                            options=[
                                                {'label': 'No manual rent', 'value': '02'},
                                                {'label': 'W/ manual rent', 'value': '01'}
                                            ],
                                            value='02',
                                            inline=True,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        html.Div(className='card-body',
                            children=[ 
                                html.Img(src="../staticfiles/img/undraw_posting_photo.svg", alt='devices', className='img-fluid px-3 px-sm-4 mt-3 mb-4')
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
                                                    id='manual_rents',
                                                    columns=(
                                                        [{'name': ['Starting'], 'id': 'year'}] +
                                                        [{'name': [(startdate + relativedelta(months=i)).strftime('%b')], 'id': str(i+1), 'type': 'numeric',
                                                            'format': Format(scheme=Scheme.fixed, precision=0,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')}
                                                            for i in range (12)
                                                        ]
                                                    ),
                                                    data=[],
                                                    editable= True,
                                                    style_data_conditional=[
                                                        {'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'}
                                                    ],
                                                    style_header={
                                                        'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'
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
            id='table-container',
        ),

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
                                                dcc.Graph(id='graph',style={'color': 'rgb(230, 230, 230)'},
                                                    figure={
                                                    'layout': {
                                                        'title': f'Trend by Date',
                                                        'showlegend': True,
                                                        'legend': {'x': 0,
                                                                    'y': 1,

                                                                    'traceorder': 'normal',
                                                                    'bgcolor': 'rgba(200, 200, 200, 0.4)'
                                                                    },
                                                        'xaxis': {'title': 'Date',
                                                                    'showline': True},
                                                        'yaxis': {'title': 'trend1',
                                                                    'side': 'left',
                                                                    'showline': True},
                                                        'yaxis2': {'title': 'trend2',
                                                                    'tickformat': '%d %B (%a)<br>%Y',
                                                                    'side': 'right',
                                                                    'showline': True}
                                                        },
                                                    },
                                                )
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
                                                    style_table={'font-size': '1.2rem'}
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

# Mise à jour alignée des zones input et slider pour amount
@app.expanded_callback(
    Output('wrapper_amount', 'children'),
    [Input('amountInput', 'value'), Input('amountSlider', "value")]
)
def amount_update(valueInput, valueSlider, **kwargs):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_id = "amountSlider.value"
    else:
        trigger_id = ctx.triggered[0]['prop_id']
    
    if trigger_id == "amountSlider.value":
        valueForinput = valueSlider
        valueForslider = valueSlider
    
    if trigger_id == "amountInput.value":
        valueForinput = int(valueInput)
        valueForslider = int(valueInput)

    return [
        html.Div('Rent amount', className='mb-2 font-weight-bold text-gray-800'),
        html.Div(className='input-group mb-3',
            children=[
                html.Div(className='input-group-prepend',
                    children=[
                        html.Div('€', className='input-group-text'),
                    ]
                ),
                dcc.Input(id="amountInput", type="text", min=100, max=10000, step=100,value="{:0,.2f}".format(valueForinput), debounce=True, className='form-control'),    
            ]
        ),
        dcc.Slider(id='amountSlider',min=100,max=10000,value=valueForslider,step=100,updatemode='drag',
            marks={100: {'label': '100€'},2000: {'label': '2000€'},5000: {'label': '5000€'},10000: {'label': '10000€'},
            },
            className='px-1'
        ),
    ]
    
    return dash.no_update

# Mise à jour alignée des zones input et slider pour RV
@app.expanded_callback(
    Output('wrapper_rv', 'children'),
    [Input('rvInput', 'value'), Input('rvSlider', "value")]
)
def rv_update(valueInput, valueSlider, **kwargs):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_id = "rvSlider.value"
    else:
        trigger_id = ctx.triggered[0]['prop_id']
    
    if trigger_id == "rvSlider.value":
        valueForinput = valueSlider
        valueForslider = valueSlider
    
    if trigger_id == "rvInput.value":
        valueForinput = int(valueInput)
        valueForslider = int(valueInput)

    return [
        html.Div('Residual value', className='mb-2 font-weight-bold text-gray-800'),
        html.Div(className='input-group mb-3',
            children=[
                html.Div(className='input-group-prepend',
                    children=[
                        html.Div('€', className='input-group-text'),
                    ]
                ),
                dcc.Input(id="rvInput", type="text", min=0, max=30000, step=1000,value="{:0,.2f}".format(valueForinput), debounce=True, className='form-control'),    
            ]
        ),
        dcc.Slider(id='rvSlider',min=0,max=30000,value=valueForslider,step=1000,updatemode='drag',
            marks={
                00000: {'label': '0K'},10000: {'label': '10K'},20000: {'label': '20K'},30000: {'label': '30K'}
            },
            className='px-1'
        ),
    ]
    
    return dash.no_update

# Mise à jour alignée des zones input et slider pour duration
@app.expanded_callback(
    Output('wrapper_duration', 'children'),
    [Input('durationInput', 'value'), Input('durationSlider', "value")]
)
def duration_update(valueInput, valueSlider, **kwargs):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_id = "durationSlider.value"
    else:
        trigger_id = ctx.triggered[0]['prop_id']

    if trigger_id == "durationSlider.value":
        valueForinput = valueSlider
        valueForslider = valueSlider
    
    if trigger_id == "durationInput.value":
        valueForinput = valueInput
        valueForslider = valueInput

    return [
        html.Div('Duration', className='mb-2 font-weight-bold text-gray-800'),
        html.Div(className='input-group mb-3',
            children=[
                html.Div(className='input-group-prepend',
                    children=[
                        html.Div('Months', className='input-group-text'),
                    ]
                ),
                dcc.Input(id="durationInput", type="text", min=12, max=84, step=1,value=valueForinput, debounce=True, className='form-control'),
            ]
        ),
        dcc.Slider(id='durationSlider',min=12,max=84,value=valueForslider,step=1,updatemode='drag',
            marks={
                12: {'label': '12M'},24: {'label': '24M'},36: {'label': '36M'},48: {'label': '48M'},60: {'label': '60M'},72: {'label': '72M'},84: {'label': '84M'}
            },
            className='px-1'
        ),
    ]
    
    return dash.no_update


# Démasquage des loyers manuels
@app.expanded_callback(
    Output('table-container', 'style'),
    [Input('manual', 'value')])
def show_manual(manualValue, **kwargs):
    if manualValue !='01':
        return {'display': 'none'}
    else:
        return {'display': 'block'}


# Alimentation des loyers manuels en fonction de la durée choisie
@app.expanded_callback(
    Output('manual_rents', 'data'),
    [Input('durationSlider', 'value'),
    Input('manual', 'value')],
    [State('manual_rents', 'data')]
    )
def create_manual(durationValue, manualValue, rows, **kwargs):
    yearref = datetime.datetime.now().year
    durationvalue = int(durationValue)
    # Calcul du nombre de lignes de la table des loyers manuels : 1 par tranche de 12 mois de la durée choisie ... +1
    nblig = int(durationvalue/12)
    d = []
    year = yearref
    for p in range(nblig):
        d.append([year,None, None, None, None, None, None, None, None, None, None, None, None])
        year=year+1
    if nblig != durationvalue/12:
        dec = durationvalue - nblig*12
        d.append([year,None, None, None, None, None, None, None, None, None, None, None, None])  
    df= pd.DataFrame(d, columns=['year',"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
    #blocage des saisies au delà de la durée
    if nblig != durationvalue/12:
        dec = durationvalue - nblig*12
        for y in range(nblig+1):
            if y==nblig:
                for x in range(12, dec, -1):
                    df[str(x)][y]= 'N/A'
            y=y+1

    return df.to_dict('rows')


# Calcul du montant financé et création du calendrier de loyers
@app.expanded_callback(
    Output('schedule', 'data'),
        [
            Input('durationSlider', 'value'),
            Input('amountSlider', 'value'),
            Input('rvSlider', 'value'),
            Input('manual_rents', 'data'),
            Input('mode', 'value'),
            Input('rateSlider', 'value'),
        ]
    )
def compute_schedule(durationValue, amountValue, rvValue, rows, modeValue, rateValue, **kwargs):
    rent = []
    j=1
    amountvalue = int(amountValue)
    rvvalue = int(rvValue)
    durationValue = int(durationValue)
    for row in rows:
        for k in range(1,13):
            if(j<= durationValue): 
                rent.append(row[str(k)])
            j=j+1

    #calcul des valeurs actuelles des loyers fixes et des coefficients
    rate = rateValue/120000
    npvvalue = 0
    npvcoeff = 0
    d = []
    k=0
    # en mode advance
    if modeValue=='01':
        for p in rent:
            #actualisation
            val = 0
            coeff = 0
            if rent[k] != None and str(rent[k]).isnumeric():
                val = (int(rent[k]) / pow((1+rate),k))
            else:
                coeff = amountValue / pow((1+rate),k)
            #cumul des valeurs actualisées
            npvvalue = npvvalue + val
            npvcoeff = npvcoeff + coeff
            k=k+1
        #calcul de la valeur actuelle de la vr
        npvrv = rvvalue / pow((1+rate),durationValue)
        #calcul du montant total actualisé
        financedValue = npvvalue + npvcoeff + npvrv
        #remplissage du calendrier de loyers en mémoire
        rento = []
        crdo= []
        crd = financedValue
        j=0
        for q in rent:
            rentschedule = amountValue
            if rent[j] != None and str(rent[j]).isnumeric():
                rentschedule = rent[j]
            crd = crd - rentschedule
            crd = crd *(1+rate)
            rento.append(rentschedule)
            crdo.append(crd)
            j=j+1
    # en mode arrear
    else:
        for p in rent:
            #actualisation
            val = 0
            coeff = 0
            if (rent[k] != None) and str(rent[k]).isnumeric():
                val = (int(rent[k]) / pow((1+rate),k+1))
            else:
                coeff = amountValue / pow((1+rate),k+1)
            #cumul des valeurs actualisées
            npvvalue = npvvalue + val
            npvcoeff = npvcoeff + coeff
            k=k+1
        #calcul de la valeur actuelle de la vr
        npvrv = rvvalue / pow((1+rate),durationValue)
        #calcul du montant total actualisé
        financedValue = npvvalue + npvcoeff + npvrv
        #remplissage du calendrier de loyers en mémoire
        rento = []
        crdo= []
        crd = financedValue
        j=0
        for q in rent:
            rentschedule = amountValue
            if rent[j] != None and str(rent[j]).isnumeric():
                rentschedule = rent[j]
            crd = crd *(1+rate) - rentschedule  
            rento.append(rentschedule)
            crdo.append(crd)
            j=j+1

# Alimentation de la table schedule
    i=0
    if (modeValue=='01') :
        for p in rent:
            d.append([(startdate + relativedelta(months=i)).strftime('%b %Y'), rento[i], crdo[i]])
            i=i+1
    if (modeValue!='01') :
        for p in rent:
            d.append([(startdate + relativedelta(months=i+1)).strftime('%b %Y'), rento[i], crdo[i]])
            i=i+1

    df= pd.DataFrame(d, columns=["date", "rent", "balance"])
    return df.to_dict('rows')


# Alimentation de la zone résultat
@app.expanded_callback(
    Output('result', 'children'),
        [
        Input('schedule', 'data'),
        Input('mode', 'value'),
        Input('rvSlider', 'value'),
        Input('rateSlider', 'value'),
        ]
    )
def result(scheduleRows, modeValue, rvValue, rateValue, **kwargs):
    val = 0
    k = 0
    rate = rateValue/120000
    if modeValue=='01':
        for scheduleRow in scheduleRows:
            val = val + (float(scheduleRow['rent'] / pow((1+rate),k)))
            k=k+1
        val = val + rvValue / pow((1+rate),k)
    else :
        for scheduleRow in scheduleRows:
            val = val + (float(scheduleRow['rent'] / pow((1+rate),k+1)))
            k=k+1
        val = val + rvValue / pow((1+rate),k)

    # affichage du montant à financer
    return 'Amount = € {:0,.1f}, w/'.format(val)

# Alimentation du graphique
@app.expanded_callback(
    Output('graph', 'figure'),
    [Input('schedule', 'data')])
def update_graph(rows, **kwargs):
    i=0
    rentx = []
    renty = []
    crdx = []
    crdy = []
    for row in rows:
        crdx.append(row['date'])
        crdy.append(row['balance'])
        rentx.append(row['date'])
        renty.append(row['rent'])
        i=i+1
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=crdx, y=crdy, name="Balance", marker_color='#f6c23e', mode='markers'),
        secondary_y=True,
    )
    fig.add_trace(
        go.Bar(x=rentx, y=renty, name="Rent", marker_color='#4e73df'),
        secondary_y=False,
    )

    # Add figure 
    fig.update_layout(
        title_text="Balance and rent amounts"
    )

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Balance</b>", secondary_y=True)
    fig.update_yaxes(title_text="<b>Rent</b>", secondary_y=False)

    return fig



#Enregistrement en BDD
@app.expanded_callback(
    Output('output-one','children'),
        [   
            Input('save_quote_button', 'n_clicks'),
            Input('durationSlider', 'value'),
            Input('amountSlider', 'value'),
            Input('rvSlider', 'value'),
            Input('schedule', 'data'),
            Input('mode', 'value'),
            Input('rateSlider', 'value')
        ]
    )

def callback_c(n, durationValue, amountValue, rvValue, scheduleRows, modeValue, rateValue, **kwargs):
    user = kwargs['user']
    if n is None:
        user = kwargs['user']
        return [
                html.Div('Lease quote', className='h3 mb-0 text-gray-800'),
                dbc.Button("Save quote", id="save_quote_button", className="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm"),
        ]
    
        return dash.no_update
    else:
        if n > 1:
                return [
                html.Div('Lease quote', className='h3 mb-0 text-gray-800'),
  ]
        schedule = Schedule()
        schedule.contract = 1
        schedule.mode = modeValue
        schedule.rv = rvValue
        schedule.amount = amountValue
        schedule.start_date = startdate
        schedule.rate = rateValue/120000
        schedule.save()
        i=0
        for scheduleRow in scheduleRows:
            if (modeValue=='01') :
                date = startdate + relativedelta(months=i)
            else :
                date = startdate + relativedelta(months=i+1)
            i=i+1
            step = Step()
            step.schedule = schedule
            step.rent = scheduleRow['rent']
            step.balance = scheduleRow['balance']
            step.date = date
            step.save()

        return [
                html.Div('Lease quote', className='h3 mb-0 text-gray-800'),
                html.Div('Quote saved !', className='h3 mb-0 text-gray-800'),
        ]
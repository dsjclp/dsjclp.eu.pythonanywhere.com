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
from core.models import Customer
from core.models import Contract
from core.models import Schedule
from core.models import Step
from django.shortcuts import get_object_or_404
import dash_daq as daq


startdate = datetime.datetime.now()

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

    
BS = "../../../core/staticfiles/css/bootstrap.css"
app = DjangoDash("ReverseApp", external_stylesheets=[BS])

graphcolors = {
    'background': '#222',
    'text': '#fff'
}

app.layout = html.Div(
    [
        html.Div(id="output-one", className='d-sm-flex align-items-center justify-content-between mb-4',
            children=[
                html.Div('Reverse quote', className='h3 mb-0'),
                dbc.Button("Save quote", id="save_quote_button", className="d-none d-md-block btn btn-sm btn-primary shadow-sm"),
            ]
        ),
        dbc.CardDeck(
            [
                dbc.Card(
                    [
                        dbc.CardHeader("Your input", className="card-title font-weight-bold bg-primary"),
                        dbc.CardBody(
                            [
                                dbc.FormGroup(id='wrapper_amount',
                                    children=[
                                        dbc.Label("Monthly rent amount", html_for="amountInput"),
                                        dbc.InputGroup(
                                            [
                                                dbc.InputGroupAddon("€", addon_type="prepend"),
                                                dbc.Input(id="amountInput", type="text", min=100, max=10000, step=100,value=2000, className='bg-secondary')                       
                                            ]
                                            ),
                                        dcc.Slider(id='amountSlider',min=100,max=10000,value=2000,step=100,updatemode='drag',
                                              marks={100: {'label': '100€'},2000: {'label': '2000€'},5000: {'label': '5000€'},10000: {'label': '10000€'},
                                            }
                                        ),
                                    ]
                                ),
                                dbc.FormGroup(id='wrapper_rv',
                                    children=[
                                        dbc.Label("Residual value", html_for="rvInput"),
                                        dbc.InputGroup(
                                            [
                                                dbc.InputGroupAddon("€", addon_type="prepend"),
                                                dbc.Input(id="rvInput", type="text", min=0, max=30000, step=1000,value=0, className='bg-secondary')                         
                                            ],
                                            ),
                                        dcc.Slider(id='rvSlider',min=0,max=30000,value=0,step=1000,updatemode='drag',
                                            marks={00000: {'label': '0K'},10000: {'label': '10K'},20000: {'label': '20K'},30000: {'label': '30K'}
                                            }
                                        ),
                                    ]
                                ),
                                dbc.FormGroup(id='wrapper_duration',
                                    children=[
                                        dbc.Label("Duration", html_for="durationInput"),
                                        dbc.InputGroup(
                                            [
                                                dbc.InputGroupAddon("Months", addon_type="prepend"),
                                                dbc.Input(id="durationInput", type="text", min=0, max=30000, step=1000,value=0, className='bg-secondary')                               
                                            ],
                                            ),
                                        dcc.Slider(id='durationSlider',min=12,max=84,value=24,step=1,updatemode='drag',
                                            marks={12: {'label': '12M'},24: {'label': '24M'},36: {'label': '36M'},48: {'label': '48M'},60: {'label': '60M'},72: {'label': '72M'},84: {'label': '84M'}
                                            }
                                        ),
                                    ]
                                ),
                                dbc.FormGroup(id='wrapper_rate',
                                    children=[
                                        dbc.Label("Annual rate", html_for="rateInput"),
                                        dbc.InputGroup(
                                            [
                                                dbc.InputGroupAddon("%", addon_type="prepend"),
                                                dbc.Input(id="rateInput", type="text", min=0, max=500, step=10,value=200, className='bg-secondary')                             
                                            ],
                                            className="mb-2",
                                            ),
                                        dcc.Slider(id='rateSlider',min=0,max=500,value=200,step=10,updatemode='drag',
                                            marks={
                                                0: {'label': '0%'},100: {'label': '1%'},200: {'label': '2%'},300: {'label': '3%'}, 400: {'label': '4%'}, 500: {'label': '5%'}
                                            },
                                        ),
                                    ]
                                ),                    
                            ], className = 'bg-body'
                        ),
                    ],
                    className='card border-light mb-3'
                ),
                dbc.Card(
                    [
                        dbc.CardHeader("Your financed amount", className="card-title font-weight-bold bg-primary"),
                        dbc.CardBody(
                            [
                                        dbc.Alert(
                                            [
                                                html.Div(id='result', className='h2 text-center text-dark my-auto font-weight-bold'),
                                            ],
                                            color="warning",
                                            className = 'mb-4 mt-2'
                                        ),
                                        dbc.Alert(
                                            [
                                                html.Img(src="../staticfiles/img/advance.png", alt='formula', className='img-fluid text-center my-auto')
                                            ],
                                            color='light',
                                            id='formula',
                                            className = 'mb-4'
                                        ),
                                        dbc.Alert(
                                            [
                                             dbc.Label("Payments in:", className='font-weight-bold'),
                                                dbc.RadioItems(
                                                    options=[
                                                        {"label": "Advance", "value": '01'},
                                                        {"label": "Arrears", "value": '02'},
                                                    ],
                                                    value='01',
                                                    id="mode",
                                                    inline=True,
                                                ),

                                            ],
                                            color="light",
                                            className='text-dark mb-4'
                                        ),
                                        dbc.Alert(
                                            [
                                                dbc.Label("With manual rents:", className='font-weight-bold'),
                                                dbc.RadioItems(
                                                    options=[
                                                        {"label": "No", "value": '02'},
                                                        {"label": "Yes", "value": '01'},
                                                    ],
                                                    value='02',
                                                    id="manual",
                                                    inline=True,
                                                ),
                                            ],
                                            color="light",
                                            className='text-dark d-none d-md-block'
                                        ),
                            ], className = 'bg-body'
                        ),
                    ],
                    className='card border-warning mb-3'
                ),
            ]
        ),
            html.Div(id='table-container',
            children=[
                dbc.Card(
                    [
                        dbc.CardHeader("Your manual rents", className="card-title font-weight-bold text-white bg-primary"),
                        dbc.CardBody(
                            [
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
                                    style_cell={
                                        'backgroundColor': '#888'
                                    },
                                    style_data_conditional=[
                                        {
                                            'if': {'row_index': 'odd'},
                                            'backgroundColor': '#444'
                                        },
                                    ],
                                    style_header={
                                        'backgroundColor': '#375a7f',
                                        'fontWeight': 'bold'
                                    },
                                    style_table={'font-size': '1.2rem'}
                                ),
                            ]
                        ),
                    ],
                    className='d-none d-md-block card border-light mb-3 text-dark',
                ),
            ]
        ),

        dbc.Card(
            [
                dbc.CardHeader("Your graph", className="card-title font-weight-bold text-white bg-primary"),
                dbc.CardBody(
                    [
                        dcc.Graph(id='graph',figure=fig)
                    ],
                 
                ),
            ],
            className='d-none d-md-block card border-light mb-3 bg-body'
        ),
        dbc.Card(
            [
                dbc.CardHeader("Your schedule", className="card-title font-weight-bold text-white bg-primary"),
                dbc.CardBody(
                    [
                        dct.DataTable(id='schedule',
                            data=[],
                            columns=[
                                    {'id': 'date', 'name': 'Date', 'type': 'datetime'},
                                    {'id': 'rent', 'name': 'Rent', 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=1,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                    {'id': 'balance',  'name': 'Balance', 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=1,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                ],
                            page_size=12,
                            export_format="csv",
                            style_cell={
                                'backgroundColor': '#888'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': '#444'
                                },
                            ],
                            style_header={
                                'backgroundColor': '#375a7f',
                                'fontWeight': 'bold'
                            },
                            style_table={'font-size': '1.2rem'}
                        )
                    ],
                    className = 'mb-4 bg-body'
                ),
            ],
            className='d-none d-md-block card border-light mb-3 bg-body'
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
        valueForinput = "{:0,.0f}".format(valueSlider)
        valueForslider = valueSlider
    
    if trigger_id == "amountInput.value":
        valueInput = valueInput.replace(',','')
        valueInput = valueInput.replace('.','')
        valueForinput = "{:0,.0f}".format(int(valueInput))
        valueForslider = int(valueInput)

    return[                
        dbc.Label("Financed amount", html_for="amountInput", className='mb-2'),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("€", addon_type="prepend"),
                dbc.Input(id="amountInput", type="text", min=100, max=10000, step=100,value=valueForinput, debounce=True, className='form-control bg-secondary text-white font-weight-bold'),                             
            ],
            className="mb-2",
            ),
        dcc.Slider(id='amountSlider',min=100,max=10000,value=valueForslider,step=100,updatemode='drag',
            marks={100: {'label': '100€'},2000: {'label': '2000€'},5000: {'label': '5000€'},10000: {'label': '10000€'},
            },
            tooltip = 'always_visible',
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
        valueForinput = "{:0,.0f}".format(valueSlider)
        valueForslider = valueSlider
    
    if trigger_id == "rvInput.value":
        valueInput = valueInput.replace(',','')
        valueInput = valueInput.replace('.','')
        valueForinput = "{:0,.0f}".format(int(valueInput))
        valueForslider = int(valueInput)

    return [
        dbc.Label("Residual value", html_for="rvInput", className='mb-2'),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("€", addon_type="prepend"),
                dbc.Input(id="rvInput", type="text", min=0, max=30000, step=1000,value=valueForinput, debounce=True, className='form-control bg-secondary text-white font-weight-bold'),                                
            ],
            className="mb-2",
            ),
        dcc.Slider(id='rvSlider',min=0,max=30000,value=valueForslider,step=1000,updatemode='drag',
            marks={
                00000: {'label': '0K'},10000: {'label': '10K'},20000: {'label': '20K'},30000: {'label': '30K'}
            },
            tooltip = 'always_visible',
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
        dbc.Label("Duration", html_for="durationInput", className='mb-2'),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Months", addon_type="prepend"),
                dbc.Input(id="durationInput", type="text", min=0, max=30000, step=1000,value=valueForinput, debounce=True, className='form-control bg-secondary text-white font-weight-bold'),                                   
            ],
            className="mb-2",
            ),
        dcc.Slider(id='durationSlider',min=12,max=84,value=valueForslider,step=1,updatemode='drag',
            marks={
                12: {'label': '12M'},24: {'label': '24M'},36: {'label': '36M'},48: {'label': '48M'},60: {'label': '60M'},72: {'label': '72M'},84: {'label': '84M'}
            },
            tooltip = 'always_visible',
        ),
    ]
    return dash.no_update


# Mise à jour alignée des zones input et slider pour rate
@app.expanded_callback(
    Output('wrapper_rate', 'children'),
    [Input('rateInput', 'value'), Input('rateSlider', "value")]
)
def rate_update(valueInput, valueSlider, **kwargs):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_id = "rateSlider.value"
    else:
        trigger_id = ctx.triggered[0]['prop_id']

    if trigger_id == "rateSlider.value":
        valueForinput = "{:0,.2f}".format(valueSlider/100)
        valueForslider = valueSlider
    
    if trigger_id == "rateInput.value":
        valueInput = valueInput.replace('.','')
        valueInput = valueInput.replace(',','')
        valueForinput = "{:0,.2f}".format(int(valueInput)/100)
        valueForslider = valueInput

    return [
        dbc.Label("Annual rate", html_for="rateInput"),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("%", addon_type="prepend"),
                dbc.Input(id="rateInput", type="text", min=0, max=500, step=10,value=valueForinput, debounce=True, className='form-control bg-secondary text-white font-weight-bold'),    
                                            
            ],
            className="mb-2",
            ),
        dcc.Slider(id='rateSlider',min=0,max=500,value=valueForslider,step=10,updatemode='drag',
            marks={
                0: {'label': '0%'},100: {'label': '1%'},200: {'label': '2%'},300: {'label': '3%'}, 400: {'label': '4%'}, 500: {'label': '5%'}
            },
            tooltip = 'always_visible',
        ),
    ]   
    return dash.no_update

# Affichage des loyers manuels
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
    #création du calendrier à partir de la table des loyers manuels
    rent = []
    j=1
    amountvalue = int(amountValue)
    rvvalue = int(rvValue)
    durationValue = int(durationValue)
    rateValue = int(rateValue)
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
    crdo= []
    rento = []
    k=0
    j=0   
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


# Alimentation du schedule
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
    return '€ {:0,.1f}'.format(val)

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
        go.Scatter(x=rentx, y=renty, name="Rent", marker_color='#f6c23e', mode='markers', marker_size=12),
        secondary_y=True,
    )
    fig.add_trace(
        go.Bar(x=crdx, y=crdy, name="Balance", marker_color='#858796'),
        secondary_y=False,
    )
    fig.update_layout(
        title_text="Balance and rent amounts",
        plot_bgcolor= graphcolors['background'],
        paper_bgcolor = graphcolors['background'],
        font = {'color': graphcolors['text']}
    ),
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Rent</b>", secondary_y=True)
    fig.update_yaxes(title_text="<b>Balance</b>", secondary_y=False)

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
                dbc.Button("Save quote", id="save_quote_button", className="d-none d-md-block btn btn-sm btn-primary shadow-sm"),
        ]
    
        return dash.no_update
    else:
        if n > 1:
                return [
                html.Div('Lease quote', className='h3 mb-0 text-gray-800'),
  ]
        customer = get_object_or_404(Customer, pk=1)
        contract = Contract()
        contract.customer = customer
        contract.user = user
        contract.save()
        schedule = Schedule()
        schedule.contract = contract
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

# Alimentation de la carte formule
@app.expanded_callback(
    Output('formula', 'children'),
        [
            Input('mode', 'value'),
         ]
    )
def update_formula(modeValue, **kwargs):
    formule = '../staticfiles/img/advance.png'
    modeValue = int(modeValue)
    if modeValue == 2:
        formule = '../staticfiles/img/arrear.png'
    return [html.Img(src=formule, alt='formula', className='img-fluid text-center my-auto')]
    return dash.no_update
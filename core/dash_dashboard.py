import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table as dct
import dash_html_components as html
import pandas as pd
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output, State
from dash_table.Format import Format, Group, Scheme, Symbol
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from core.models import Schedule
from core.models import Contract
from django.db.models import  Q, Count
import dash_daq as daq


theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#f39c12',
    'secondary': '#6E6E6E',
}

led1Layout = html.Div(
    [
        daq.LEDDisplay(
            id='led1',
            value="0000",
            className='dark-theme-control',
             color = 'black'
        ),
        html.Br(),
        html.Div('Deals created #', className='h4 mb-0 text-center text-light'),
    ],className='mb-4'
)

led2Layout = html.Div(
    [
        daq.LEDDisplay(
            id='led2',
            value="0000",
            className='dark-theme-control',
            color = 'black'
        ),
        html.Br(),
        html.Div('Deals validated #', className='h4 mb-0 text-center text-light'),
    ],className='mb-4'
)

led3Layout = html.Div(
    [
        daq.LEDDisplay(
            id='led3',
            value="0000",
            className='dark-theme-control',
            color = 'black'
        ),
        html.Br(),
        html.Div('Deals activated #', className='h4 mb-0 text-center text-light'),
    ],className='mb-4'
)

gauge1Layout = html.Div(
    [
        daq.Gauge(
            id='gauge1',
            min=0,
            max=10,
            value=0,
            className='dark-theme-control'
        ),
        html.Div('Validation leadtime (days #)', className='h4 mb-4 text-center text-light'),
    ]
)

gauge2Layout = html.Div(
    [
        daq.Gauge(
            id='gauge2',
            min=0,
            max=10,
            value=0,
            className='dark-theme-control'
        ),
        html.Div('Activation leadtime (days #)', className='h4 mb-0 text-center text-light'),
    ]
)

graduate1Layout = html.Div(
    [
        daq.GraduatedBar(
            id='graduate1',
            value=0,
            className='dark-theme-control'
        ),
        html.Br(),
        html.Div('Activation %', className='h4 mb-4 text-center text-light'),
    ]
)

graduate2Layout = html.Div(
    [
        daq.GraduatedBar(
            id='graduate2',
            value=0,
            className='dark-theme-control'
        ),
        html.Br(),
        html.Div('Cancellation %', className='h4 mb-0 text-center text-light'),
    ]
)


app = DjangoDash("DashboardApp")

app.layout = html.Div(
    [

        html.Div(id="output-one", className='d-sm-flex align-items-center justify-content-between mb-4',
            children=[
                html.Div('Your dashboard', className='h3 mb-0'),
                daq.PowerButton(
                    on=False,
                    color=theme['detail'],
                    id='powerbutton',
                    className='dark-theme-control',
                ),
            ]
        ),
    
        dbc.Row(
            [
                daq.DarkThemeProvider(theme=theme, children=led1Layout),
                daq.DarkThemeProvider(theme=theme, children=led2Layout),
                daq.DarkThemeProvider(theme=theme, children=led3Layout),
            ],
            id='dark-theme-components',
            className = 'd-flex justify-content-around',
            style={'border': 'solid 1px #A2B1C6', 'border-radius': '5px', 'padding': '20px', 'margin-top': '20px'}          
        ),
 
        dbc.Row(
            [
                daq.DarkThemeProvider(children=gauge1Layout),
                daq.DarkThemeProvider(children=gauge2Layout),
            ],
            id='gauge',
            className = 'd-flex justify-content-around mb-4 ',
            style={'border': 'solid 1px #A2B1C6', 'border-radius': '5px', 'padding': '20px', 'margin-top': '20px'}          
        ),

        dbc.Row(
            [
                daq.DarkThemeProvider(children=graduate1Layout),
                daq.DarkThemeProvider(theme=theme, children=graduate2Layout),
            ],
            id='gauge',
            className = 'd-flex justify-content-around mb-4 ',
            style={'border': 'solid 1px #A2B1C6', 'border-radius': '5px', 'padding': '20px', 'margin-top': '20px'}          
        ),

        dbc.Row(
            [
                dbc.CardHeader("Your pipeline", className="card-title font-weight-bold text-white bg-primary"),
                dbc.CardBody(
                    [
                dct.DataTable(id='schedules_list',
                            data=[],
                            columns=[
                                    {'id': 'id', 'name': 'Id', 'type': 'numeric'},
                                    {'id': 'status',  'name': 'Status', 'type': 'string'},
                                    {'id': 'status_date',  'name': 'Status date', 'type': 'date'},
                                    #{'id': 'amount', 'name': 'Amount', 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=1,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                    #{'id': 'rv',  'name': 'RV', 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=1,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                    #{'id': 'rate',  'name': 'Rate', 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=2,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'%')},
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
                    className = 'mb-4'
                ),
            ],
            className='d-none d-md-block card border-light mb-3 bg-body'
        ),
    ],
    id='contracts', className = 'mx-1'
)



# Mise à jour de la led created
@app.expanded_callback(
    Output('led1', 'value'),
    [Input('powerbutton', 'on')]
)
def update_led(on, **kwargs):
    val = '0000'
    if on==True:
        user = kwargs['user']
        val = Contract.objects.filter(user=user).count()
        val = str(val).zfill(4)
    return val

# Mise à jour de la led validated
@app.expanded_callback(
    Output('led2', 'value'),
    [Input('powerbutton', 'on')]
)
def update_led(on, **kwargs):
    val = '0000'
    if on==True:
        user = kwargs['user']
        status = 'Validated'
        val = Contract.objects.filter(user=user, status=status).count()
        val = str(val).zfill(4)
    return val

# Mise à jour de la led activated
@app.expanded_callback(
    Output('led3', 'value'),
    [Input('powerbutton', 'on')]
)
def update_led(on, **kwargs):
    val = '0000'
    if on==True:
        user = kwargs['user']
        status = 'Activated'
        val = Contract.objects.filter(user=user, status=status).count()
        val = str(val).zfill(4)
    return val


# Mise à jour du format de la led created
@app.expanded_callback(
    Output('led1', 'color'),
    [Input('powerbutton', 'on')]
)
def update_led(on, **kwargs):
    color = 'black'
    if on==True:
        color= theme['primary']
    return color


# Mise à jour du format de la led validated
@app.expanded_callback(
    Output('led2', 'color'),
    [Input('powerbutton', 'on')]
)
def update_led(on, **kwargs):
    color = 'black'
    if on==True:
        color= theme['primary']
    return color


# Mise à jour du format de la led activated
@app.expanded_callback(
    Output('led3', 'color'),
    [Input('powerbutton', 'on')]
)
def update_led_format(on, **kwargs):
    color = 'black'
    if on==True:
        color= theme['primary']
    return color

# Mise à jour de la jauge validation leadtime
@app.expanded_callback(
    Output('gauge1', 'value'),
    [Input('powerbutton', 'on')]
)
def update_gauge(on, **kwargs):
    val = 0
    if on==True:
        user = kwargs['user']
        val = 0
        status = 'Validated'
        contract_list = Contract.objects.filter(user=user, status=status)
        contract_count = Contract.objects.filter(user=user, status=status).count()
        for contract in contract_list:
            delta = contract.validation_date - contract.creation_date
            delta = delta.days
            val = val + delta
        val = val / contract_count
    return val

# Mise à jour de la jauge activation leadtime
@app.expanded_callback(
    Output('gauge2', 'value'),
    [Input('powerbutton', 'on')]
)
def update_gauge(on, **kwargs):
    val = 0
    if on==True:
        user = kwargs['user']
        val = 0
        status = 'Activated'
        contract_list = Contract.objects.filter(user=user, status=status)
        contract_count = Contract.objects.filter(user=user, status=status).count()
        for contract in contract_list:
            delta = contract.activation_date - contract.validation_date
            delta = delta.days
            val = val + delta
        val = val / contract_count
    return val

# Mise à jour du format de la jauge validation leadtime
@app.expanded_callback(
    Output('gauge1', 'color'),
    [Input('powerbutton', 'on')]
)
def update_gauge_format(on, **kwargs):
    color = 'black'
    if on==True:
        color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}}
    return color

# Mise à jour du format de la jauge activation leadtime
@app.expanded_callback(
    Output('gauge2', 'color'),
    [Input('powerbutton', 'on')]
)
def update_gauge_format(on, **kwargs):
    color = 'black'
    if on==True:
        color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}}
    return color

# Mise à jour de la graduation activation
@app.expanded_callback(
    Output('graduate1', 'value'),
    [Input('powerbutton', 'on')]
)
def update_graduate(on, **kwargs):
    val = 0
    if on==True:
        user = kwargs['user']
        status = 'Activated'
        activated = Contract.objects.filter(user=user, status=status).count()
        allcontracts = Contract.objects.filter(user=user).count()
        val = activated / allcontracts
        val = int (val*10)
    return val

# Mise à jour de la graduation cancellation
@app.expanded_callback(
    Output('graduate2', 'value'),
    [Input('powerbutton', 'on')]
)
def update_graduate(on, **kwargs):
    val = 0
    if on==True:
        user = kwargs['user']
        status = 'Cancelled'
        cancelled = Contract.objects.filter(user=user, status=status).count()
        allcontracts = Contract.objects.filter(user=user).count()
        val = cancelled / allcontracts
        val = int (val*10)
    return val
    
# Mise à jour du format de la graduation activation
@app.expanded_callback(
    Output('graduate1', 'color'),
    [Input('powerbutton', 'on')]
)
def update_graduate_format(on, **kwargs):
    color = 'black'
    if on==True:
        color={"gradient":True,"ranges":{"red":[0,6],"yellow":[6,8],"green":[8,10]}}
    return color

# Mise à jour du format de la graduation cancellation
@app.expanded_callback(
    Output('graduate2', 'color'),
    [Input('powerbutton', 'on')]
)
def update_graduate_format(on, **kwargs):
    color = 'black'
    if on==True:
        color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}}
    return color


# Mise à jour du pipeline
@app.expanded_callback(
    Output('schedules_list', 'data'),
    [Input('powerbutton', 'on')] 
)
def contract_list_update(on, **kwargs):
    if on==True:
        d = []
        contracts = Contract.objects.exclude(status='Activated')
        for row in contracts:
            d.append([row.id,row.status, row.status_date])
        df= pd.DataFrame(d, columns=['id','status','status_date'])
        return df.to_dict('rows')
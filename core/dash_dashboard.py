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

import dash_daq as daq


theme =  {
    'dark': True,
    'detail': '#f39c12',
    'primary': '#f39c12',
    'secondary': 'green',
}

rootLayout = html.Div([
    daq.BooleanSwitch(
        on=True,
        id='darktheme-daq-booleanswitch',
        className='dark-theme-control'
    ), html.Br(),
    daq.ToggleSwitch(
        id='darktheme-daq-toggleswitch',
        className='dark-theme-control'
    ), html.Br(),

    daq.GraduatedBar(
        value=4,
        color=theme['primary'],
        id='darktheme-daq-graduatedbar',
        className='dark-theme-control'
    ), html.Br(),
    daq.Indicator(
        value=True,
        color=theme['primary'],
        id='darktheme-daq-indicator',
        className='dark-theme-control'
    ), html.Br(),

    daq.PowerButton(
        on=True,
        color=theme['primary'],
        id='darktheme-daq-powerbutton',
        className='dark-theme-control'
    ), html.Br(),
    daq.StopButton(
        id='darktheme-daq-stopbutton',
        className='dark-theme-control'
    ), html.Br(),

    daq.Tank(
        min=0,
        max=10,
        value=5,
        id='darktheme-daq-tank',
        className='dark-theme-control'
    ), html.Br(),

])


ledLayout = html.Div(
    [
        daq.LEDDisplay(
            value="3.14",
            color=theme['primary'],
            className='dark-theme-control justify-content-center'
        ),
        html.Div('Status', className='h3 mb-0 text-center text-light'),
    ],className='justify-content-center mb-2'
)

gaugeLayout = html.Div(
    [
    daq.Gauge(
        min=0,
        max=10,
        value=6,
        color=theme['primary'],
        className='dark-theme-control'
        ),
        html.Br(),
        daq.Indicator(
        value=True,
        color=theme['primary'],
        className='dark-theme-control'
        ),
        html.Br(),
        daq.GraduatedBar(
        value=4,
        color=theme['primary'],
        className='dark-theme-control'
        ),
    ],className='justify-content-center'
)



app = DjangoDash("DashboardApp")

app.layout = html.Div(
    [
        html.Div(id="output-one", className='d-sm-flex align-items-center justify-content-between mb-4',
            children=[
                html.Div('Your dashboard', className='h3 mb-0 text-gray-800'),
                daq.ToggleSwitch(id='toggle-theme', label=['Light', 'Dark'], value=True),
            ]
        ),
        dbc.Row(
            [
                daq.DarkThemeProvider(theme=theme, children=ledLayout),
                daq.DarkThemeProvider(theme=theme, children=ledLayout),
                daq.DarkThemeProvider(theme=theme, children=ledLayout),
                daq.DarkThemeProvider(theme=theme, children=ledLayout)
            ],
            id='dark-theme-components',
            className = 'd-flex justify-content-between',
            style={'border': 'solid 1px #A2B1C6', 'border-radius': '5px', 'padding': '50px', 'margin-top': '20px'}          
        ),
 
        dbc.Row(
            [
                daq.DarkThemeProvider(theme=theme, children=gaugeLayout),
                daq.DarkThemeProvider(theme=theme, children=gaugeLayout),
                daq.DarkThemeProvider(theme=theme, children=gaugeLayout),
                daq.DarkThemeProvider(theme=theme, children=gaugeLayout)
            ],
            id='gauge',
            className = 'd-flex justify-content-between mb-4',
            style={'border': 'solid 1px #A2B1C6', 'border-radius': '5px', 'padding': '50px', 'margin-top': '20px'}          
        ),

        dbc.Card(
            [
                dbc.CardHeader("Your contracts", className="card-title font-weight-bold text-white bg-primary"),
                dbc.CardBody(
                    [
                dct.DataTable(id='schedules_list',
                            data=[],
                            columns=[
                                    {'id': 'amount', 'name': 'Amount', 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=1,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                    {'id': 'rv',  'name': 'RV', 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=1,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'€')},
                                    {'id': 'rate',  'name': 'Rate', 'type': 'numeric', 'format': Format(scheme=Scheme.fixed, precision=2,group=Group.yes,groups=3,group_delimiter='.',decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix=u'%')},
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
    ],
    id='contracts', 
)


@app.callback(
    dash.dependencies.Output('dark-theme-components', 'style'),
    [dash.dependencies.Input('toggle-theme', 'value')],
    state=[dash.dependencies.State('dark-theme-components', 'style')]
)
def switch_bg(dark, currentStyle):

    if(dark):
        currentStyle.update(
            backgroundColor='#303030'
        )
    else:
        currentStyle.update(
            backgroundColor='white'
        )
    return currentStyle


@app.callback(
    Output('schedules_list', 'data'),
    [dash.dependencies.Input('toggle-theme', 'value')],
    state=[dash.dependencies.State('dark-theme-components', 'style')]
)
def switch_bg(dark, currentStyle):
    d = []
    schedules = Schedule.objects.all()
    for row in schedules:
        d.append([row.amount,row.rv, row.rate])
    df= pd.DataFrame(d, columns=['amount','rv','rate'])
    return df.to_dict('rows')
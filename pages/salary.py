from dash import Dash, html, dcc ,callback, Output, Input

import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.YETI]


df = pd.read_csv('salary.csv', sep=',')

all_cont = df['Country'].unique()
app = Dash(__name__, external_stylesheets=external_stylesheets)

layout = dbc.Container([
    dbc.Row ([
        dbc.Col(    
                html.Div([
                html.H3("Статистика"),
                html.Hr(style={'color': 'black'}),
            ], style={'textAlign': 'center'})
        )

    ]),
     html.Br(),
    html.Div([
            html.Div([
                html.Label('Страны'),
                dcc.Dropdown(
                    id = 'crossfilter1-cont',
                    options = [{'label': i, 'value': i} for i in all_cont],
                    # значение континента, выбранное по умолчанию
                    value = ['Russia'],
                    # возможность множественного выбора
                    multi = True
                )
            ],
            style = {'width': '48%', 'display': 'inline-block'}),
       
            html.Div([
                html.Label('Основные показатели'),
                dcc.RadioItems(
                options = [
                    {'label':'Зарплата', 'value': 'SalaryUSD'},
                    {'label':'Должность', 'value': 'JobTitle'},
                    {'label':'Основная база данных', 'value': 'PrimaryDatabase'},
                    {'label':'Другие базы данных', 'value': 'OtherDatabases'},
                    {'label':'Года опыта', 'value': 'YearsWithThisTypeOfJob'},
                    # {'label':'Статус', 'value': 'Status'},

                ],
                id = 'crossfilter1-ind',
                value = 'YearsWithThisTypeOfJob',
                labelStyle={'display': 'inline-block'   }
                )
            ],
            style = {'width': '48%',  'float': 'right', 'display': 'inline-block'}),
        ], style = {
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(256,256,256)',
            'padding': '10px 5px',
            'marginBottom': '20px'
        }),




     html.Br(),

     html.Div(
            dcc.Slider(
                id = 'crossfilter-year',
                min = df['Survey Year'].min(),
                max = df['Survey Year'].max(),
                value = 2017,
                step = None,
                marks = {str(year):
                    str(year) for year in df['Survey Year'].unique()}
                ),
            style = {'width': '95%', 'padding': '0px 20px 20px 20px'}
        ),
       html.Div(
            dcc.Graph(id = 'pie'),
            style = {'width': '100%', 'display': 'inline-block'}
        ),
        
         html.Div(
            dcc.Graph(id = 'bar'),
            style = {'width': '100%', 'display': 'inline-block'}
        ),
       
        html.Div(
            dcc.Graph(id = 'line'),
            style = {'width': '100%', 'float': 'center', 'display': 'inline-block'}
        ),
     
])

@callback(
    Output('bar', 'figure'),
    [Input('crossfilter1-cont', 'value'),
    Input('crossfilter1-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_stacked_area(country, indication, year):
    filtered_data = df[(df['Survey Year'] <= year) &
        (df['Survey Year'].isin(country))]
    figure = px.bar(
        filtered_data,
        x = 'Survey Year',
        y = indication,
        color = 'Country'
        )
    return figure

@callback(
    Output('line', 'figure'),
    [Input('crossfilter1-cont', 'value'),
    Input('crossfilter1-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_scatter(continent, indication, year):
    filtered_data = df[(df['Survey Year'] <= year) &
        (df['Country'])]
    figure = px.line(
        filtered_data,
        x = "Survey Year",
        y = indication,
        
        color = 'JobTitle',
        title = "Значения показателя по странам",
        markers = True,
    )
    return figure
@callback(
    Output('pie', 'figure'),
    [Input('crossfilter1-cont', 'value'),
    Input('crossfilter1-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_scatter(continent, indication, year):
    filtered_data = df[(df['Survey Year'] <= year) &
        (df['Country'])]
    figure = px.pie(
        filtered_data,
        names  = 'JobTitle',
        values = indication,
        
        # color = 'JobTitle',
        title = "Значения показателя по странам",
        # markers = True,
    )
    return figure

@callback(
    Output('choropleth1', 'figure1'),
    Input('crossfilter1-ind', 'value')
)
def update_choropleth(indication):
    figure = px.choropleth(
        df,
        locations='Country',    
        locationmode = 'country names',
        color=indication,
        hover_name='Country',
        title='Показатели по странам',
        color_continuous_scale=px.colors.sequential.BuPu,
        animation_frame='Survey Year',
        height=650
        )
    return figure

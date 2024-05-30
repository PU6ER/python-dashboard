from dash import Dash, html, dcc ,callback, Output, Input

import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.YETI]


df = pd.read_csv('LifeExpectancy.csv', sep=',')

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
                    value = ['Russian Federation'],
                    # возможность множественного выбора
                    multi = True
                )
            ],
            style = {'width': '48%', 'display': 'inline-block'}),
       
            html.Div([
                html.Label('Основные показатели'),
                dcc.RadioItems(
                options = [
                    {'label':'Продолжительность жизни(мужчины)', 'value': 'Life expectancy (men)'},
                    {'label':'Продолжительность жизни(женщины)', 'value': 'Life expectancy(women)'},
                    {'label':'Потребление алкоголя', 'value': 'Alcohol'},
                    {'label':'Индекс массы тела', 'value': 'BMI'},
                    {'label':'ВВП', 'value': 'GDP'},
                    {'label':'Статус', 'value': 'Status'},

                ],
                id = 'crossfilter1-ind',
                value = 'GDP',
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


        html.Div(
            dcc.Slider(
                id = 'crossfilter-year',
                min = df['Year'].min(),
                max = df['Year'].max(),
                value = 2000,
                step = None,
                marks = {str(year):
                    str(year) for year in df['Year'].unique()}
                ),
            style = {'width': '95%', 'padding': '0px 20px 20px 20px'}
        ),

         html.Div(
            dcc.Graph(id = 'bar'),
            style = {'width': '49%', 'display': 'inline-block'}
        ),
       
        html.Div(
            dcc.Graph(id = 'line'),
            style = {'width': '49%', 'float': 'right', 'display': 'inline-block'}
        ),


        html.Div(
            dcc.Graph(id = 'choropleth1'),
            style = {'width': '100%', 'display': 'inline-block'}
        ),






], fluid=True)

@callback(
    Output('bar2', 'figure2'),
    [Input('crossfilter1-cont', 'value'),
    Input('crossfilter1-ind', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_stacked_area(country, indication, year):
    filtered_data = df[(df['Year'] <= year) &
        (df['Country'].isin(country))]
    figure = px.bar(
        filtered_data,
        x = 'Year',
        y = indication,
        color = 'Country'
        )
    return figure

@callback(
    Output('line2', 'figure2'),
    [Input('crossfilter21-cont', 'value'),
    Input('crossfilter21-ind', 'value'),
    Input('crossfilte2r-year', 'value')]
)
def update_scatter(continent, indication, year):
    filtered_data = df[(df['Year'] <= year) &
        (df['Country'].isin(continent))]
    figure = px.line(
        filtered_data,
        x = "Year",
        y = indication,
        color = "Country",
        title = "Значения показателя по странам",
        markers = True,
    )
    return figure

@callback(
    Output('choropleth212', 'figure11'),
    Input('crossfilter212-ind', 'value')
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
        animation_frame='Year',
        height=650
        )
    return figure





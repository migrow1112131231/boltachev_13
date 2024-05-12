from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df

layout = html.Div([
    dcc.Dropdown(
        id='continent-dropdown',
        options=[{'label': i, 'value': i} for i in df['continent'].unique()],
        value=df['continent'].unique()[0]
    ),
    dcc.RangeSlider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=[df['Year'].min(), df['Year'].max()],
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    ),
    dbc.Container(id='indicator-graphs')
])

@callback(
    Output('indicator-graphs', 'children'),
    [Input('continent-dropdown', 'value'),
    Input('year-slider', 'value')])
def update_graphs(selected_continent, selected_years):
    filtered_df = df[(df['continent'] == selected_continent) &
                     (df['Year'] >= selected_years[0]) &
                     (df['Year'] <= selected_years[1])]

    graphs = []

    rus_indicators = {
        'Life expectancy': 'Продолжительность жизни',
        'Population': 'Население',
        'Schooling': 'Образование',
        'GDP': 'ВВП'
    }

    for indicator in ['Life expectancy', 'Population', 'Schooling', 'GDP']:
        fig = px.line(filtered_df, x='Year', y=indicator, color='Country', title=f'{rus_indicators[indicator]}')
        graphs.append(dcc.Graph(figure=fig))

    return graphs

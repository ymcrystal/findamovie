"""
Project

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# pandas dataframe to html table
def generate_table(dataframe):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range (len(dataframe))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)

server = app.server
'''
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
'''
df = pd.read_csv('./movie-Info1.csv')
df2 = pd.read_csv('./rating.csv')

fig = px.bar(df, x="title", y="rating", color="imdbId", barmode="group")

app.layout = html.Div([

    html.H1('Choose a movie you like!', style={'textAlign': 'center'}),
    html.Div([html.H4('Rating of movie:'),
              dcc.Slider(id="ratings_slider", min=1, max=5, value=5,
              marks={i:str(i) for i in range(6)}),#slider marks
              html.H4('Select the genre you like:'),
              dcc.Dropdown(options=[{'label': 'Action', 'value': 'Action'},
                                     {'label': 'Comedy', 'value': 'Comedy'},
                                     {'label': 'Crime', 'value': 'Crime'},
                                     {'label': 'Documentary', 'value': 'Documentary'},
                                     {'label': 'Drama', 'value': 'Drama'},
                                     {'label': 'Horror', 'value': 'Horror'},
                                     {'label': 'Musical', 'value': 'Musical'},
                                     {'label': 'Romance', 'value': 'Romance'},
                                     {'label': 'Sci-Fi', 'value': 'Sci-Fi'},
                                     {'label': 'Thriller', 'value': 'Thriller'},
                                     {'label': 'War', 'value': 'War'},
                                     {'label': 'Western', 'value': 'Western'}],
                           id="genres_select_checklist",
                           value=''),
               html.Div(html.Div(id="df_div"))
                           ],
             style={'width': '49%', 'display': 'inline-block'}),
    
    html.Div([html.H4('The rating distribution of this genre:'),dcc.Graph(id='df_graph')],
             style={'width': '49%', 'display': 'inline-block', 'float': 'right'})
    ])

# Update the table
@app.callback(
    Output(component_id='df_div', component_property='children'),
    [Input(component_id='ratings_slider', component_property='value'),
     Input(component_id='genres_select_checklist', component_property='value'),]
)
def update_table(select_rating, genres_select):
    ratex = df[df.rating==select_rating]
    finalx =  ratex[ratex.genres == genres_select]
    return generate_table(finalx)

# Update the bar chart
@app.callback(
    Output("df_graph", "figure"), 
    [Input(component_id='genres_select_checklist', component_property='value')])
def update_bar_chart(genres_select):
    mask = df2[genres_select]
    fig = px.bar(mask, x=[1,2,3,4,5], y=genres_select, 
                 barmode="group")
    return fig
    
if __name__ == '__main__':
    app.run_server(debug=True)
    






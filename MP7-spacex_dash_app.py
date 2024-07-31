# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=
    [html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign':'center','color':'#503D36','font-size':40}
    ),
# Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label':'All Sites', 'value':'ALL'},
            {'label':'Cape Canaveral Launch Complex 40','value':'CCAFS LC-40'},
            {'label':'Cape Canaveral Space Launch Complex 40','value':'CCAFS SLC-40'},
            {'label':'Kennedy Space Center Launch Complex 39A','value':'KSC LC-39A'},
            {'label':'Vandenberg Space Launch Complex 4','value':'VAFB SLC-4E'}
        ],
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True
    ),
    html.Br(),
# Pie charts
    html.Div(dcc.Graph(id='pie-chart')),
    html.Br(),
# Slider
    html.P("Payload Range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[0,10000]
    ),
# Scatter plot
    html.Div(dcc.Graph(id='scatter-plot')),
])

# Pie chart callback function and decorator
@app.callback(Output(component_id='pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df, 
            values='class', 
            names='Launch Site', 
            title='Successful Launches by Site'
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title='Launch Success Rate for {}'.format(entered_site)
        )
        return fig

# Scatter plot callback function and decorator
@app.callback(Output(component_id='scatter-plot', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(entered_site, payload_range):
    scatter_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                           (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    if entered_site == 'ALL':
        fig = px.scatter(
            scatter_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Success by Payload'
        )
        return fig
    else:
        scatter_df = scatter_df[scatter_df['Launch Site']==entered_site]
        fig = px.scatter(
            scatter_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Success by Payload for {}'.format(entered_site)
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
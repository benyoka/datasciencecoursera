# Import required packages
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
# data = airline_data.sample(n=500, random_state=42)
# Pie Chart Creation
# fig = px.pie(data, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')

# Create a dash application
app = dash.Dash(__name__)
# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add description about the graph using HTML P (paragraph) component
# Finally, add graph component.
# app.layout = html.Div(children=[html.H1('Airline On-time Performance Dashboard',
#                                         style={'textAlign': 'center', 
#                                                'color': '#503D36', 
#                                                'font-size': 50}),
#                                 html.P('Proportion of distance group (250 mile distance interval group) by flights.', 
#                                        style={'textAlign':'center', 'color': '#F57241'}),
#                                 dcc.Graph(figure = fig),                          
                    # ])

app.layout = html.Div(children=[ 
    html.H1('Airline Performance Dashboard',style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Div(["Input Year: ", dcc.Input(id='input-year', 
        value='2010', 
        type='number', 
        style={'height':'50px', 'font-size': 35}),], 
    style={'font-size': 40}),
    html.Br(),
    html.Br(),
    html.Div(dcc.Graph(id='line-plot')),
    html.Br(),
    html.Div(dcc.Graph(id='bar-plot')),
    ])

# add callback decorator
@app.callback( Output(component_id='line-plot', component_property='figure'),
               Input(component_id='input-year', component_property='value'))
# Add computation to callback function and return graph
def get_graph(entered_year):
    # Select 2019 data
    df =  airline_data[airline_data['Year']==int(entered_year)]
    
    # Group the data by Month and compute average over arrival delay time.
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()
    print(line_data)
    fig = go.Figure(data=go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green')))
    fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
    return fig

@app.callback( Output(component_id='bar-plot',component_property='figure'),
             Input(component_id='input-year', component_property='value'))
def get_bar_plot(entered_year):
    df = airline_data[airline_data['Year']==int(entered_year)]
    bar_data = df.groupby('DestState')['Flights'].sum().reset_index()
    print(bar_data)
    fig = px.bar(bar_data, x="DestState", y="Flights", title='Total number of flights to the destination state split by reporting airline') 
    fig.update_layout(title='Flights to Destination State', xaxis_title='DestState', yaxis_title='Flights')
    return fig       


# Run the application                   
if __name__ == '__main__':
    app.run_server()
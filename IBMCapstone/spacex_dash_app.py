# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'ALL'}] +  [{'label': site, 'value': site} for site in launch_sites],
                                    value='ALL',
                                    placeholder="place holder here",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=50,
                                    marks={0: '0',
                                        2500: '2500',
                                        5000: '5000',
                                        7500: '7500',
                                        10000: '10000'},
                                    value=[0, 1000]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    # filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered = spacex_df[spacex_df['Launch Site'] == entered_site][['class', 'Launch Site']].groupby(['class']).count().add_suffix(' Count').reset_index()
        # print('filtered\n', filtered)
        fig = px.pie(filtered, values='Launch Site Count', 
        names='class',
        title=f"Total Success Launches for Site {entered_site}")
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# Next, we want to plot a scatter plot with the x axis to be the payload and the y axis to be the launch outcome (i.e., class column).
# As such, we can visually observe how payload may be correlated with mission outcomes for selected site(s).

# In addition, we want to color-label the Booster version on each scatter point so that we may
# observe mission outcomes with different boosters.

# Now, let’s add a call function including the following application logic:

# Input to be [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
# Note that we have two input components, one to receive selected launch site and another to receive selected payload range
# Output to be Output(component_id='success-payload-scatter-chart', component_property='figure')
# A If-Else statement to check if ALL sites were selected or just a specific launch site was selected
# If ALL sites are selected, render a scatter plot to display all values for variable Payload Mass (kg) and variable class.
# In addition, the point color needs to be set to the booster version i.e., color="Booster Version Category"
# If a specific launch site is selected, you need to filter the spacex_df first, and render a scatter chart to show
# values Payload Mass (kg) and class for the selected site, and color-label the point using Boosster Version Category likewise.

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='payload-slider', component_property='value'), Input(component_id='site-dropdown', component_property='value')])
def get_scatter(payload_range, entered_site):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] <= payload_range[1]) & (spacex_df['Payload Mass (kg)'] >= payload_range[0])]
    # print(payload_range)
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', title="Correlation Between Payload and Success for All Sites", color='Booster Version Category')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        # print('filtered\n', filtered_df)
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', title=f"Correlation Between Payload and Success for {entered_site}", color='Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug = True)

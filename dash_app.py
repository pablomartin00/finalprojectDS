# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
rrrrrr_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = rrrrrr_df['Payload Mass (kg)'].max()
min_payload = rrrrrr_df['Payload Mass (kg)'].min()
print(rrrrrr_df.columns)
# Create a dash application
app = dash.Dash(__name__)

# Obtener una lista única de los nombres de los sitios de lanzamiento
launch_sites = rrrrrr_df['Launch Site'].unique()

# Crear la lista de opciones para el menú desplegable
options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]

# Create an app layout
app.layout = html.Div(children=[html.H1('rrrrrr Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=options,
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload]),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# Función decoradora para especificar la entrada y salida de la función
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = rrrrrr_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        # Filtrar el dataframe para incluir solo datos del sitio seleccionado
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', title=f'Total Success Launches for site {entered_site}')
        return fig

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter(site, payload):
    low, high = payload
    mask = (rrrrrr_df['Payload Mass (kg)'] > low) & (rrrrrr_df['Payload Mass (kg)'] < high)
    filtered_df = rrrrrr_df[mask]
    if site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == site]
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                     title='Correlation between Payload and Success for all Sites' if site == 'ALL' else f'Correlation between Payload and Success for {site}')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()

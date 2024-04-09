import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Load data
data = pd.read_csv('subsciber_DB.csv', parse_dates=["acquisition_timestamp"])
# Create a Dash app
app = dash.Dash(__name__)

# Get a list of unique topics
species = data['species'].unique()

app.layout = html.Div([
    dcc.Markdown(' SELECT SPECIES:'),
    dcc.Dropdown(
        id='species-dropdown',
        options=[{'label': species, 'value': species} for species in species],
        value=species[0]
    ),
    dcc.Markdown(' SELECT PARAMETER TO CONFRONT: LENGTH OR WIDTH:'),

    dcc.Dropdown(
        id='comparison-parameter-dropdown',
        options=[{'label': 'Length', 'value': 'length'}, {'label': 'Width', 'value': 'width'}],
        value='length'
    ),
    dcc.Graph(id='line-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 500,  # in milliseconds
        n_intervals=0,
        max_intervals=-1
    )
])

@app.callback(
    [Output('line-graph', 'figure'),
     Output('species-dropdown', 'options'),
     Output('species-dropdown', 'value'),],
    [Input('species-dropdown', 'value'),
     Input('comparison-parameter-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_graph(selected_species, selected_parameter, n_intervals ):
    data = pd.read_csv('subsciber_DB.csv', parse_dates=["acquisition_timestamp"])
    # Get a list of unique species
    species = data['species'].unique()

    # If no species is selected, select the first one
    if selected_species is None and len(species) > 0:
        selected_species = species[0]
    if selected_parameter is None:
        selected_parameter = 'length'

    # Filter data
    filtered_data = data[data['species'] == selected_species] if selected_species else pd.DataFrame()
    # Create traces based on the selected parameter
    traces = []
    print(selected_parameter)
    if selected_parameter == 'length':
        traces.append(go.Scatter(
            x=filtered_data['sepal_length'],
            y=filtered_data['petal_length'],
            mode='markers',
            name='Petal Length'
        ))
    elif selected_parameter == 'width':
        traces.append(go.Scatter(
            x=filtered_data['sepal_width'],
            y=filtered_data['petal_width'],
            mode='markers',
            name='Petal Width'
        ))



    figure = {
        'data': traces,
        'layout': go.Layout(
            title='Time series for species: ' + (selected_species if selected_species else ''),
            xaxis={'title': 'Petal length' if selected_parameter == 'length' else 'Petal width'},
            yaxis={'title': 'Sepal length'  if selected_parameter == 'length' else 'Sepal width'},
        )
    }

    # Update dropdown options
    species_dropdown_options = [{'label': s, 'value': s} for s in species]

    return figure, species_dropdown_options, selected_species

if __name__ == '__main__':
    app.run_server(debug=True)
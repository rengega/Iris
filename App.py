import collections
import threading
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import dash_table

from IrisPublisher import IrisPublisher
from IrisSubscriber import IrisSubscriber

# shared queue, global to be accessed by the callback
global shared_queue

# using a global variable to store the data to be displayed in the table
# this is to avoid the callback from being called multiple times
global current_data
# shared queue to store the incoming data: only the last 5 data points will be stored
shared_queue = collections.deque(maxlen=5)
current_data = []

# start the subscriber
irisSubs = IrisSubscriber(shared_queue)
thread = threading.Thread(target=irisSubs.start).start()

# start the publisher
irisPub = IrisPublisher()
thread = threading.Thread(target=irisPub.start_loop).start()


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Iris Incoming Data Table"),
    html.H2("The following table displays the 25 latest incoming data points from the mqtt topic ."),
    # component updates every 1 second (mqtt client running on the thread sends data every 2 seconds)
    dcc.Interval(id='interval-component', interval=1 * 1000, n_intervals=0),
    html.Button('Clear Table', id='clear-button', n_clicks=0,
                style={'width': '100%', 'height': '30px', 'background-color': '#4CAF50', 'color': 'white',
                       'font-size': '20px', 'display': 'block', 'margin-bottom': '10px', 'position': 'relative'}),
    dash_table.DataTable(id='table', columns=[{"name": i, "id": i} for i in
                                              ["species", "sepal_length", "sepal_width", "petal_length",
                                               "petal_width", "acquisition_timestamp"]])
])

@app.callback(
    Output('table', 'data'),
    Input('interval-component', 'n_intervals'),
)
def update_table(n):
    global shared_queue
    global current_data
    # keep the size of the current data under control (50 data points)
    while shared_queue:
        if len(current_data) > 25:
            current_data.pop(0)
        current_data.append(shared_queue.popleft())
    return current_data

@app.callback(
    Output('interval-component', 'n_intervals'),
    Input('clear-button', 'n_clicks'),
)
def clear_table(n_clicks):
    global current_data
    current_data = []
    return 0

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')



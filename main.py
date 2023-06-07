# external dependencies
from dash import Dash
from dash.dependencies import Input, Output, State

# local files
import user_interface as ui
import layout

# Create the Dash app
app = Dash(__name__)

# Define the layout
app.layout = layout.layout

#----------------------- attaching UI functions to the app callback ------------------------#
app.callback(
    Output('tut-skip', 'children'),
    Output('tut-skip', 'style'),
    Input('add-connection', 'n_clicks'),
    Input('remove-selected', 'n_clicks'),
    Input('calculate-shortest', 'n_clicks'),
    Input('clear-shortest', 'n_clicks'),
    Input('tut-skip', 'n_clicks'),
    Input('text-tips', 'value'), # ensures that button disappears correctly
)(ui.update_skip_button)

app.callback(
    Output('text-tips', 'value'),
    Input('add-host', 'n_clicks'),
    Input('add-router', 'n_clicks'),
    Input('add-connection', 'n_clicks'),
    Input('calculate-shortest', 'n_clicks'),
    Input('clear-shortest', 'n_clicks'),
    Input('tut-skip', 'n_clicks'),
    Input('network-graph', 'elements'), # ensures correct error messages
)(ui.update_tips_textarea)

app.callback(
    Output('network-graph', 'elements'),
    Input('add-host', 'n_clicks'),
    Input('add-router', 'n_clicks'),
    Input('add-connection', 'n_clicks'),
    Input('remove-selected', 'n_clicks'),
    Input('reset-network', 'n_clicks'),
    Input('sp-data', 'data'), # triggers graph update when new sp calculated
    State('host-name', 'value'),
    State('router-name', 'value'),
    State('connection-cost', 'value'),
    State('network-graph', 'selectedNodeData'),
    State('network-graph', 'selectedEdgeData'),
)(ui.update_graph)

app.callback(
    Output('host-name', 'value'),
    Input('network-graph', 'elements'),
)(ui.update_hostname_field)

app.callback(
    Output('router-name', 'value'),
    Input('network-graph', 'elements'),
)(ui.update_routername_field)

app.callback(
    Output('connection-cost', 'value'),
    Input('network-graph', 'elements'),
)(ui.update_cost_field)

app.callback(
    Output('text-total-cost', 'value'),
    Input('sp-data', 'data'),
)(ui.update_total_cost_text)

app.callback(
    Output('sp-data', 'data'),
    Input('calculate-shortest', 'n_clicks'),
    Input('clear-shortest', 'n_clicks'),
    State('sp-data', 'data'),
    State('network-graph', 'selectedNodeData'),
)(ui.modify_sp)

#-----------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run_server(debug=True)

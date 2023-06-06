# external dependencies
from dash import Dash
from dash.dependencies import Input, Output, State

# local files
import network
import layout
from states import TutorialState, ErrorState, msg


# Create the Dash app
app = Dash(__name__)

# Define the layout
app.layout = layout.layout

# instantiate network
net = network.NetworkGraph()

# instantiate states
tut_state = TutorialState.START
err_state = ErrorState.OK

# returns text and style of the skip button based on states
def skip_button_text_style(tut, err):
    # decide text based on states
    if err == ErrorState.OK:
        text = 'Skip'
    else:
        text = 'Dismiss'

    # decide style based on states
    style = layout.skip_button_style.copy()
    if tut == TutorialState.FINISH and err == ErrorState.OK:
        style['display'] = 'none'

    return text, style

#----------------------- attaching NetworkGraph functions to the app callback ------------------------#
@app.callback(
    Output('network-graph', 'elements', allow_duplicate=True),
    Output('host-name', 'value', allow_duplicate=True),
    Output('text-tips', 'value', allow_duplicate=True),
    Input('add-host', 'n_clicks'),
    State('host-name', 'value'),
    prevent_initial_call='initial_duplicate'
)
def add_host(n_clicks, host_name):
    global tut_state, err_state

    if n_clicks > 0:
        net.add_host(host_name)

        # change tutorial state
        if tut_state == TutorialState.START: tut_state = TutorialState.HOST_ADDED
        if tut_state == TutorialState.ROUTER_ADDED: tut_state = TutorialState.NODES_ADDED

    return net.get_elements(), f'H{net.n_hosts + 1}', msg(tut_state, err_state)

@app.callback(
    Output('network-graph', 'elements', allow_duplicate=True),
    Output('router-name', 'value', allow_duplicate=True),
    Output('text-tips', 'value', allow_duplicate=True),
    Input('add-router', 'n_clicks'),
    State('router-name', 'value'),
    prevent_initial_call='initial_duplicate'
)
def add_router(n_clicks, router_name):
    global tut_state, err_state

    if n_clicks > 0:
        net.add_router(router_name)

        # change tutorial state
        if tut_state == TutorialState.START: tut_state = TutorialState.ROUTER_ADDED
        if tut_state == TutorialState.HOST_ADDED: tut_state = TutorialState.NODES_ADDED

    return net.get_elements(), f'R{net.n_routers + 1}', msg(tut_state, err_state)

@app.callback(
    Output('network-graph', 'elements', allow_duplicate=True),
    Output('text-tips', 'value', allow_duplicate=True),
    Output('tut-skip', 'children', allow_duplicate=True),
    Output('tut-skip', 'style', allow_duplicate=True),
    Input('add-connection', 'n_clicks'),
    State('network-graph', 'selectedNodeData'),
    State('connection-cost', 'value'),
    prevent_initial_call='initial_duplicate'
)
def add_connection(n_clicks, sel_nodes, cost):
    global tut_state, err_state

    if n_clicks > 0:
        # check that the passed cost is valid
        if not cost or cost < 1:
            err_state = ErrorState.INV_COST
        # check if exactly two nodes are selected
        elif not sel_nodes or len(sel_nodes) != 2:
            err_state = ErrorState.SELECT_2
        else:
            # change tutorial state
            if tut_state == TutorialState.NODES_ADDED: tut_state = TutorialState.CON_ADDED

            # add connection
            rs = net.add_connection(sel_nodes[0]['id'], sel_nodes[1]['id'], cost)
            if rs != ErrorState.OK:
                err_state = rs

    text, style = skip_button_text_style(tut_state, err_state)
    return net.get_elements(), msg(tut_state, err_state), text, style

@app.callback(
    Output('network-graph', 'elements', allow_duplicate=True),
    Output('host-name', 'value', allow_duplicate=True),
    Output('router-name', 'value', allow_duplicate=True),
    Output('text-tips', 'value', allow_duplicate=True),
    Output('tut-skip', 'children', allow_duplicate=True),
    Output('tut-skip', 'style', allow_duplicate=True),
    Input('remove-selected', 'n_clicks'),
    State('network-graph', 'selectedNodeData'),
    State('network-graph', 'selectedEdgeData'),
    prevent_initial_call=True
)
def remove_selected(n_clicks, sel_nodes, sel_edges):
    global tut_state, err_state

    if n_clicks > 0:
        # check if any elements are selected
        if not sel_nodes and not sel_edges:
            err_state = ErrorState.SELECT_1

        if sel_nodes is not None:
            for n in sel_nodes: net.remove_node(n['id'])
        if sel_edges is not None:
            for e in sel_edges: net.remove_edge(e['source'], e['target'])
    
    text, style = skip_button_text_style(tut_state, err_state)
    return (
        net.get_elements(),
        f'H{net.n_hosts+1}',
        f'R{net.n_routers+1}',
        msg(tut_state, err_state),
        text,
        style
    )

@app.callback(
    Output('network-graph', 'elements', allow_duplicate=True),
    Output('text-total-cost', 'value', allow_duplicate=True),
    Output('text-tips', 'value', allow_duplicate=True),
    Output('tut-skip', 'children', allow_duplicate=True),
    Output('tut-skip', 'style', allow_duplicate=True),
    Input('calculate-shortest', 'n_clicks'),
    State('network-graph', 'selectedNodeData'),
    prevent_initial_call='initial_duplicate'
)
def calculate_path(n_clicks, sel_nodes):
    global tut_state, err_state
    cost = ''

    if n_clicks > 0:
        # check if exactly two nodes are selected
        if not sel_nodes or len(sel_nodes) != 2: 
            err_state = ErrorState.SELECT_2
        else:
            # calculate sp
            path, cost = net.dijkstra(sel_nodes[0]['id'], sel_nodes[1]['id'])

            # check if path exists
            if cost != 'Unreachable':
                # unhighlight previous path
                net.unhighlight_path()

                # highlight path on graph
                net.highlight_path(path)

                # change tutorial state
                if tut_state == TutorialState.CON_ADDED: tut_state = TutorialState.SP_SHOWN

    text, style = skip_button_text_style(tut_state, err_state)
    return net.get_elements(), cost, msg(tut_state, err_state), text, style
        

@app.callback(
    Output('network-graph', 'elements', allow_duplicate=True),
    Output('text-total-cost', 'value', allow_duplicate=True),
    Output('text-tips', 'value', allow_duplicate=True),
    Output('tut-skip', 'style', allow_duplicate=True),
    Input('clear-shortest', 'n_clicks'),
    prevent_initial_call='initial_duplicate'
)
def clear_path(n_clicks):
    global tut_state, err_state

    

    if n_clicks > 0:
        net.unhighlight_path()

        # change tutorial state
        if tut_state == TutorialState.SP_SHOWN: tut_state = TutorialState.FINISH
    else:
        net.unhighlight_path()

        # need to go back one state since sp is reset by design
        if tut_state == TutorialState.SP_SHOWN: tut_state = TutorialState.CON_ADDED

    # decide style based on states
    style = layout.skip_button_style.copy()
    if tut_state == TutorialState.FINISH and err_state == ErrorState.OK:
        style['display'] = 'none'

    return net.get_elements(), '', msg(tut_state, err_state), style

@app.callback(
    Output('tut-skip', 'children', allow_duplicate=True),
    Output('tut-skip', 'style', allow_duplicate=True),
    Output('text-tips', 'value', allow_duplicate=True),
    Input('tut-skip', 'n_clicks'),
    prevent_initial_call='initial_duplicate'
)
def skip(n_clicks):
    global tut_state, err_state

    if n_clicks > 0:
        # if there is an error, change err state back to normal
        if err_state != ErrorState.OK:
            err_state = ErrorState.OK
        # otherwise, skip the tutorial
        else:
            tut_state = TutorialState.FINISH

    text, style = skip_button_text_style(tut_state, err_state)
    return text, style, msg(tut_state, err_state)

@app.callback(
    Output('network-graph', 'elements', allow_duplicate=True),
    Output('host-name', 'value', allow_duplicate=True),
    Output('router-name', 'value', allow_duplicate=True),
    Output('connection-cost', 'value', allow_duplicate=True),
    Output('text-total-cost', 'value', allow_duplicate=True),
    Input('reset-network', 'n_clicks'),
    prevent_initial_call=True
)
def reset_network(n_clicks):
    if n_clicks > 0:
        net.reset()

    return (
        net.get_elements(),
        f'H{net.n_hosts + 1}',
        f'R{net.n_routers + 1}',
        5,
        ''
    )

    

#-----------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run_server(debug=True)

# external dependencies
from dash import Dash
from dash.dependencies import Input, Output, State

# local files
import network
import layout


# Create the Dash app
app = Dash(__name__)

# Define the layout
app.layout = layout.layout

# class that represents the entire network
net = network.NetworkGraph()

#----------------------- attaching NetworkGraph functions to the app callback ------------------------#
@app.callback(
    Output('network-graph', 'elements', allow_duplicate=True),
    Output('host-name', 'value', allow_duplicate=True),
    Input('add-host', 'n_clicks'),
    State('host-name', 'value'),
    prevent_initial_call=True # function is not called on startup
)
def add_host(n_clicks, host_name):
    net.add_host(host_name)
    return net.get_elements(), f'H{net.n_hosts + 1}'

@app.callback(
    Output('network-graph', 'elements', allow_duplicate=True),
    Output('router-name', 'value', allow_duplicate=True),
    Input('add-router', 'n_clicks'),
    State('router-name', 'value'),
    prevent_initial_call=True # function is not called on startup
)
def add_router(n_clicks, router_name):
    net.add_router(router_name)
    return net.get_elements(), f'R{net.n_routers + 1}'

@app.callback(
    Output('network-graph', 'elements', allow_duplicate=True),
    Input('add-connection', 'n_clicks'),
    State('network-graph', 'selectedNodeData'),
    State('connection-cost', 'value'),
    prevent_initial_call=True # function is not called on startup
)
def add_connection(n_clicks, sel_nodes, cost):
    if len(sel_nodes) == 2: # exactly two nodes are selected
        print(sel_nodes)
        net.add_connection(sel_nodes[0]['id'], sel_nodes[1]['id'], cost)
    return net.get_elements()

@app.callback(
    Output('network-graph', 'elements', allow_duplicate=True),
    Output('host-name', 'value', allow_duplicate=True),
    Output('router-name', 'value', allow_duplicate=True),
    Input('remove-selected', 'n_clicks'),
    State('network-graph', 'selectedNodeData'),
    State('network-graph', 'selectedEdgeData'),
    prevent_initial_call=True # function is not called on startup
)
def remove_selected(n_clicks, sel_nodes, sel_edges):
    print(sel_edges)
    if sel_nodes is not None:
        for n in sel_nodes: net.remove_node(n['id'])
    if sel_edges is not None:
        for e in sel_edges: net.remove_edge(e['source'], e['target'])
    print(net.get_elements())
    return net.get_elements(), f'H{net.n_hosts+1}', f'R{net.n_routers+1}'


# Router list
#routers = []

# # Add random neighbors to routers
# def add_neighbors(routers):
#     for i, router in enumerate(routers):
#         for j, neighbor in enumerate(routers):
#             if i != j:
#                 cost = random.randint(1, 100)
#                 router.add_neighbor(neighbor, cost)

# Create routers
# @app.callback(
#     Output('start-router', 'options'),
#     Output('dest-router', 'options'),
#     Input('create-routers', 'n_clicks'),
#     State('num-routers', 'value')
# )
# def create_routers(n_clicks, num_routers):
#     if n_clicks > 0 and num_routers is not None:
#         global routers
#         routers = [Router(f"R{i}") for i in range(1, num_routers+1)]
#         add_neighbors(routers)
#         options = [{'label': router.name, 'value': router.name} for router in routers]
#         return options, options
#     return [], []

# Calculate the shortest path and update graph and table
# @app.callback(
#     Output('network-graph', 'figure'),
#     Output('table', 'figure'),
#     Input('calculate-path', 'n_clicks'),
#     State('start-router', 'value'),
#     State('dest-router', 'value')
# )
# def calculate_path(n_clicks, start_router_name, dest_router_name):
#     if n_clicks > 0 and start_router_name is not None and dest_router_name is not None:
#         start_router = next(filter(lambda r: r.name == start_router_name, routers))
#         dest_router = next(filter(lambda r: r.name == dest_router_name, routers))

#         shortest_path, total_cost = start_router.dijkstra(routers, dest_router)

#         # Create networkx graph
#         G = nx.Graph()

#         # Add routers and their connections to graph
#         G.add_nodes_from([router.name for router in routers])
#         for router in routers:
#             for cost, neighbor in router.neighbors:
#                 G.add_edge(router.name, neighbor.name, cost=cost)

#         # Set position of nodes using spring layout
#         pos = nx.spring_layout(G, seed=42)

#         # Create edges
#         edge_x = []
#         edge_y = []
#         edge_text = []
#         for edge in G.edges(data=True):
#             edge_x += [pos[edge[0]][0], pos[edge[1]][0], None]
#             edge_y += [pos[edge[0]][1], pos[edge[1]][1], None]
#             edge_text.append(f"Cost: {edge[2]['cost']}")

#         # Create nodes
#         node_x = []
#         node_y = []
#         node_text = []
#         for node in G.nodes():
#             node_x.append(pos[node][0])
#             node_y.append(pos[node][1])
#             node_text.append(f"{node}<br>IP: {next(router.ipv6_address for router in routers if router.name == node)}")

#         # Create plotly figure for network graph
#         fig = go.Figure()

#         # Add edges to figure
#         fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=1), hovertext=edge_text, hoverinfo='text'))

#         # Add nodes to figure
#         fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text', text=node_text, hoverinfo='text', textposition='top center', marker=dict(size=25, line=dict(width=2), color='white')))

#         # Update layout
#         fig.update_layout(showlegend=False, margin=dict(t=50, b=10, l=10, r=10))

#         # Create table with router information
#         table_trace = go.Table(header=dict(values=['Router', 'Neighbors and Cost']),
#                                cells=dict(values=[list(G.nodes()), [", ".join([f"{neighbor} ({data['cost']})" for neighbor, data in G[node].items() if node != neighbor]) for node in G.nodes()]]))

#         return fig, go.Figure(data=[table_trace])

#     return go.Figure(), go.Figure()

if __name__ == '__main__':
    app.run_server(debug=True)

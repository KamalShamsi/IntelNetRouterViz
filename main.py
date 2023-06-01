import random
import heapq
import networkx as nx
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc

class Router:
    def __init__(self, name):
        self.name = name
        self.ipv6_address = "2001:db8::" + str(random.randint(0, 65535))
        self.neighbors = []

    def add_neighbor(self, neighbor, cost):
        for c, n in self.neighbors:
            if n == neighbor:
                return
        self.neighbors.append((cost, neighbor))
        neighbor.add_neighbor(self, cost)

    def dijkstra(self, routers, dest):
        distances = {router: float("inf") for router in routers}
        distances[self] = 0
        prev_nodes = {router: None for router in routers}

        queue = [(0, self)]
        while queue:
            curr_dist, curr_router = heapq.heappop(queue)
            if curr_router == dest:
                break
            if curr_dist > distances[curr_router]:
                continue
            for cost, neighbor in curr_router.neighbors:
                dist = curr_dist + cost
                if dist < distances[neighbor]:
                    distances[neighbor] = dist
                    prev_nodes[neighbor] = curr_router
                    heapq.heappush(queue, (dist, neighbor))

        path = []
        curr_router = dest
        while curr_router is not None:
            path.append(curr_router)
            curr_router = prev_nodes[curr_router]
        path.reverse()

        total_cost = 0
        for i in range(len(path) - 1):
            for cost, neighbor in path[i].neighbors:
                if neighbor == path[i+1]:
                    total_cost += cost

        return path, total_cost

    def __lt__(self, other):
        return self.name < other.name

# Create the Dash app
app = Dash(__name__)

# Define the layout
app.layout = html.Div([
    dcc.Input(id='num-routers', type='number', min=2, step=1, placeholder='Enter number of routers'),
    html.Button(id='create-routers', n_clicks=0, children='Create routers'),
    dcc.Dropdown(id='start-router', placeholder='Select start router'),
    dcc.Dropdown(id='dest-router', placeholder='Select destination router'),
    html.Button(id='calculate-path', n_clicks=0, children='Calculate path'),
    dcc.Graph(id='network-graph'),
    dcc.Graph(id='table')
])

# Router list
routers = []

# Add random neighbors to routers
def add_neighbors(routers):
    for i, router in enumerate(routers):
        for j, neighbor in enumerate(routers):
            if i != j:
                cost = random.randint(1, 100)
                router.add_neighbor(neighbor, cost)

# Create routers
@app.callback(
    Output('start-router', 'options'),
    Output('dest-router', 'options'),
    Input('create-routers', 'n_clicks'),
    State('num-routers', 'value')
)
def create_routers(n_clicks, num_routers):
    if n_clicks > 0 and num_routers is not None:
        global routers
        routers = [Router(f"R{i}") for i in range(1, num_routers+1)]
        add_neighbors(routers)
        options = [{'label': router.name, 'value': router.name} for router in routers]
        return options, options
    return [], []

# Calculate the shortest path and update graph and table
@app.callback(
    Output('network-graph', 'figure'),
    Output('table', 'figure'),
    Input('calculate-path', 'n_clicks'),
    State('start-router', 'value'),
    State('dest-router', 'value')
)
def calculate_path(n_clicks, start_router_name, dest_router_name):
    if n_clicks > 0 and start_router_name is not None and dest_router_name is not None:
        start_router = next(filter(lambda r: r.name == start_router_name, routers))
        dest_router = next(filter(lambda r: r.name == dest_router_name, routers))

        shortest_path, total_cost = start_router.dijkstra(routers, dest_router)

        # Create networkx graph
        G = nx.Graph()

        # Add routers and their connections to graph
        G.add_nodes_from([router.name for router in routers])
        for router in routers:
            for cost, neighbor in router.neighbors:
                G.add_edge(router.name, neighbor.name, cost=cost)

        # Set position of nodes using spring layout
        pos = nx.spring_layout(G, seed=42)

        # Create edges
        edge_x = []
        edge_y = []
        edge_text = []
        for edge in G.edges(data=True):
            edge_x += [pos[edge[0]][0], pos[edge[1]][0], None]
            edge_y += [pos[edge[0]][1], pos[edge[1]][1], None]
            edge_text.append(f"Cost: {edge[2]['cost']}")

        # Create nodes
        node_x = []
        node_y = []
        node_text = []
        for node in G.nodes():
            node_x.append(pos[node][0])
            node_y.append(pos[node][1])
            node_text.append(f"{node}<br>IP: {next(router.ipv6_address for router in routers if router.name == node)}")

        # Create plotly figure for network graph
        fig = go.Figure()

        # Add edges to figure
        fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=1), hovertext=edge_text, hoverinfo='text'))

        # Add nodes to figure
        fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text', text=node_text, hoverinfo='text', textposition='top center', marker=dict(size=25, line=dict(width=2), color='white')))

        # Update layout
        fig.update_layout(showlegend=False, margin=dict(t=50, b=10, l=10, r=10))

        # Create table with router information
        table_trace = go.Table(header=dict(values=['Router', 'Neighbors and Cost']),
                               cells=dict(values=[list(G.nodes()), [", ".join([f"{neighbor} ({data['cost']})" for neighbor, data in G[node].items() if node != neighbor]) for node in G.nodes()]]))

        return fig, go.Figure(data=[table_trace])

    return go.Figure(), go.Figure()

if __name__ == '__main__':
    app.run_server(debug=True)

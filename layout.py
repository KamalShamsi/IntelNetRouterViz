from dash import dcc, html
import dash_cytoscape as cyto

layout = html.Div([
    #dcc.Input(id='num-routers', type='number', min=2, step=1, placeholder='Enter number of routers'),
    #html.Button(id='create-routers', n_clicks=0, children='Create routers'),
    #dcc.Dropdown(id='start-router', placeholder='Select start router'),
    #dcc.Dropdown(id='dest-router', placeholder='Select destination router'),
    #html.Button(id='calculate-path', n_clicks=0, children='Calculate path'),
    #dcc.Graph(id='network-graph'),
    #dcc.Graph(id='table'),
    cyto.Cytoscape(
        id='network-graph',
        layout={'name': 'preset', 'fit': True, 'animate': True, 'animationDuration': 200},
        style={
            'width': '98%',
            'height': '600px',
            'border': 'solid',
            'margin': 'auto',
            'marginBottom': '15px',
        },
        stylesheet=[
            {
                'selector': '.host',
                'style': {
                    'shape': 'triangle'
                }
            },
            {
                'selector': '.router',
                'style': {
                }
            },
            {
                'selector': 'node',
                'style': {
                    'content': 'data(label)',
                    'fontSize': '10px',
                    'text-halign': 'center',
                    'text-valign': 'bottom',
                    'text-wrap': 'wrap',
                    'text-margin-y': '3px'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'content': 'data(label)',
                    'fontSize': '10px',
                    'text-halign': 'center',
                    'text-valign': 'center',
                }
            },
        ],
        autoRefreshLayout=True,
        boxSelectionEnabled=False,
        userZoomingEnabled=False,
        userPanningEnabled=False,
        maxZoom=2,
        elements=[]
    ),
    html.Div([
        html.Div([
            dcc.Input(
                id='host-name', type='text', value='H1', placeholder='Name',
                style={
                    'marginRight': '5px',
                    'padding': '10px 10px',
                    'fontSize': '20px',
                    'width': '250px'
                }
            ),
            html.Button(
                id='add-host', n_clicks=0, children='Add Host',
                style={
                    'width': '170px',
                    'padding': '10px 10px',
                    'fontSize'   : '20px',
                }
            )
        ]),
        html.Div([
            dcc.Input(
                id='router-name', type='text', value='R1', placeholder='Name',
                style={
                    'marginRight': '5px',
                    'padding': '10px 10px',
                    'fontSize': '20px',
                    'width': '250px'
                }
            ),
            html.Button(
                id='add-router', n_clicks=0, children='Add Router',
                style={
                    'width': '170px',
                    'padding': '10px 10px',
                    'fontSize' : '20px',
                }
            )
        ]),
        html.Div([
            dcc.Input(
                id='connection-cost', type='number', value=5, placeholder='Cost (e.g. 5)',
                style={
                    'marginRight': '5px',
                    'padding': '10px 10px',
                    'fontSize': '20px',
                    'width': '250px'
                }
            ),
            html.Button(
                id='add-connection', n_clicks=0, children='Add Connection',
                style={
                    'width': '170px',
                    'padding': '10px 10px',
                    'fontSize': '20px',
                }
            )
        ]),
        html.Button(
            id='remove-selected', n_clicks=0, children='Remove',
            style={
                'marginTop': '5px',
                'padding': '10px 10px',
                'fontSize': '20px',
                'width': '449px',
            }
        ),
    ], style={
        'margin': 'auto',
        'textAlign': 'center'
    })
])
from dash import dcc, html
import dash_cytoscape as cyto

skip_button_style = {
    'position': 'absolute',
    'right': 'calc(0.5% + 7px)',
    'bottom': '10px',
    'padding': '3px',
    'fontSize': '15px',
}

layout = html.Div([
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
            {
                'selector': 'edge:unselected[is_highlighted = "true"],'\
                            ' node:unselected[is_highlighted = "true"]',
                'style': {
                    'line-color': 'green',
                    'background-color': 'green'
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
        dcc.Textarea(
            id='text-tips',
            value='Add a router or a host to start!',
            readOnly='readonly',
            draggable='false',
            style={
                'width': '100%',
                'height': '100%',
                'resize': 'none',
                'padding': '10px 2%',
                'fontSize': 'min(25px, 1.5vw)',
                'box-sizing': 'border-box'
            }
        ),
        html.Button(
            id='tut-skip', n_clicks=0, children='Skip',
            style=skip_button_style.copy()
        ),
    ], style={
        'position': 'absolute',
        'top': '629px',
        'left': 'calc(49.5% + 4px)',
        'transform': 'translate(-50%, 0%)',
        'width': 'calc(95% - 920px)',
        'height': '194px',
        'margin': 'none'
    }),
    html.Div([
        dcc.Textarea(
            id='text-total-cost',
            placeholder='...',
            readOnly='readonly',
            draggable='false',
            style={
                'resize': 'none',
                'width': '443px',
                'display': 'block',
                'height': '135px',
                'marginBottom': '5px',
                'fontSize': '70px',
                'textAlign': 'center'
            }
        ),
        html.Button(
            id='clear-shortest', n_clicks=0, children='Clear',
            style={
                'padding': '10px 10px',
                'fontSize': '20px',
                'width': '222px',
            }
        ),
        html.Button(
            id='calculate-shortest', n_clicks=0, children='Shortest Path',
            style={
                'padding': '10px 10px',
                'fontSize': '20px',
                'width': '222px',
                'marginLeft': '5px'
            }
        ),
    ], style={
        'position': 'absolute',
        'right': '2%',
        'textAlign': 'center'
    }),
    
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
        html.Div([
            html.Button(
                id='reset-network', n_clicks=0, children='Reset Network',
                style={
                    'marginTop': '5px',
                    'marginRight': '5px',
                    'padding': '10px 10px',
                    'fontSize': '20px',
                    'width': '274px',
                }
            ),
            html.Button(
                id='remove-selected', n_clicks=0, children='Remove',
                style={
                    'marginTop': '5px',
                    'padding': '10px 10px',
                    'fontSize': '20px',
                    'width': '170px',
                }
            )
        ]),
    ], style={'marginLeft': '1%'}),
])
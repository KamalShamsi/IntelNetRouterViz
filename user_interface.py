from dash import ctx

import states as st
import network
import layout

# instantiate states
tut_state = st.TutorialState.START
err_state = st.ErrorState.OK

# instantiate network
net = network.NetworkGraph()


def update_skip_button(*args):
    global tut_state, err_state

    # decide text based on states
    if err_state == st.ErrorState.OK:
        text = 'Skip'
    else:
        text = 'Dismiss'

    # decide style based on states
    style = layout.skip_button_style.copy()
    if tut_state == st.TutorialState.FINISH and err_state == st.ErrorState.OK:
        style['display'] = 'none'

    return text, style


def update_tips_textarea(n_hst, n_rtr, n_con, n_cal, n_clr, n_skp, _):
    '''
    Handles state switching of tut_state and err state.
    Updates the tips textarea with the relevant message based on those states.
    '''
    global tut_state, err_state
    
    # id of the element that triggered this callback
    id = ctx.triggered_id

    # advance state
    if id == 'add-host' and n_hst > 0:
        if tut_state == st.TutorialState.START and err_state == st.ErrorState.OK:
            tut_state = st.TutorialState.HOST_ADDED
        if tut_state == st.TutorialState.ROUTER_ADDED and err_state == st.ErrorState.OK:
            tut_state = st.TutorialState.NODES_ADDED
    if id == 'add-router' and n_rtr > 0:
        if tut_state == st.TutorialState.START and err_state == st.ErrorState.OK:
            tut_state = st.TutorialState.ROUTER_ADDED
        if tut_state == st.TutorialState.HOST_ADDED and err_state == st.ErrorState.OK:
            tut_state = st.TutorialState.NODES_ADDED
    if id == 'add-connection' and n_con > 0:
        if tut_state == st.TutorialState.NODES_ADDED and err_state == st.ErrorState.OK:
            tut_state = st.TutorialState.CON_ADDED
    if id == 'calculate-shortest' and n_cal > 0:
        if tut_state == st.TutorialState.CON_ADDED and err_state == st.ErrorState.OK:
            tut_state = st.TutorialState.SP_SHOWN
    if id == 'clear-shortest' and n_clr > 0:
        if tut_state == st.TutorialState.SP_SHOWN and err_state == st.ErrorState.OK:
            tut_state = st.TutorialState.FINISH
    if id == 'tut-skip' and n_skp > 0:
        if err_state == st.ErrorState.OK:
            tut_state = st.TutorialState.FINISH
        else:
            err_state = st.ErrorState.OK

    return st.state_message(tut_state, err_state)


def update_graph(n_hst, n_rtr, n_con, n_rem, n_rst,
                 _, h_name, r_name, cost, sel_nodes, sel_edges):
    global err_state

    # id of the element that triggered this callback
    id = ctx.triggered_id
    
    # handle "Add Host" click
    if id == 'add-host' and n_hst > 0:
        err_state = st.ErrorState.OK

        if not h_name or h_name == '':
            err_state = st.ErrorState.INV_NAME
        
        else:
            net.add_host(h_name)
    
    # handle "Add Router" click
    if id == 'add-router' and n_rtr > 0:
        err_state = st.ErrorState.OK

        if not r_name or r_name == '':
            err_state = st.ErrorState.INV_NAME
        
        else:
            net.add_router(r_name)
    
    # handle "Add Connection" click
    if id == 'add-connection' and n_con > 0:
        err_state = st.ErrorState.OK

        # check that the passed cost is valid
        if not cost or cost < 1:
            err_state = st.ErrorState.INV_COST
        
        # check if exactly two nodes are selected
        elif not sel_nodes or len(sel_nodes) != 2:
            err_state = st.ErrorState.SELECT_2
        
        # add connection
        else:
            rs = net.add_connection(sel_nodes[0]['id'], sel_nodes[1]['id'], cost)
            if rs != st.ErrorState.OK:
                err_state = rs
    
    # handle "Remove" click
    if id == 'remove-selected' and n_rem > 0:
        err_state = st.ErrorState.OK

        # check if any elements are selected
        if not sel_nodes and not sel_edges:
            err_state = st.ErrorState.SELECT_1
        
        # remove selected
        else:
            # remove selected nodes
            if sel_nodes is not None:
                for n in sel_nodes: net.remove_node(n['id'])
            
            # remove selected edges
            if sel_edges is not None:
                for e in sel_edges: net.remove_edge(e['source'], e['target'])
    
    # handle "Reset Network" click
    if id == 'reset-network' and n_rst > 0:
        err_state = st.ErrorState.OK

        net.reset()
        
    return net.get_elements()


def update_hostname_field(_):
    return f'H{net.n_hosts + 1}'


def update_routername_field(_):
    return f'R{net.n_routers + 1}'


def update_cost_field(_):
    return 5


def update_total_cost_text(sp_data):
    return sp_data.get('total_cost')


def modify_sp(n_cal, n_clr, prev_sp_data, sel_nodes):
    global err_state
    cost = prev_sp_data['total_cost']
    id = ctx.triggered_id

    # clear previos error state
    err_state = st.ErrorState.OK

    if id == 'calculate-shortest' and n_cal > 0:
        # check if exactly two nodes are selected
        if not sel_nodes or len(sel_nodes) != 2:
            err_state = st.ErrorState.SELECT_2
        
        # calculate and highlight
        else:
            # calculate sp
            path, cost = net.dijkstra(sel_nodes[0]['id'], sel_nodes[1]['id'])

            # highlight
            if cost != 'Unreachable':
                # unhighlight previous path
                net.unhighlight_path()

                # highlight new path
                net.highlight_path(path)
    
    if id == 'clear-shortest' and n_clr > 0:
        net.unhighlight_path()
        cost = ''
    
    # iter parameter makes sure sp data changes on every function call
    if prev_sp_data.get('total_cost') != cost:
        return {'total_cost': cost, 'iter': 0}
    else:
        return {'total_cost': cost, 'iter': (prev_sp_data['iter'] + 1)}
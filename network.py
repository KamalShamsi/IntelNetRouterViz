import node as n

class NetworkGraph():
    def __init__(self, elements=[]) -> None:
        # these fields are used for network display only
        self.elements = elements
        self.n_hosts = 0
        self.n_routers = 0

        # these fields are used for shortest path calculation
        self.nodes = []
    
    def add_router(self, id: str) -> None:
        # check if a node with the same name already exists
        router_idx = self.find_node_element(id)
        if router_idx is not None: # if it does
            self.elements.pop(router_idx) # remove it

        # create new node object
        node = n.Node(id)

        # add new node element (to self.elements)
        self.elements.append({
            'data': {'id': node.name, 'label': f'{node.name}\n{node.ipv6_address}'},
            'classes': 'router'
        })

        # increment router counter
        self.n_routers += 1
    
    def add_host(self, id) -> None:
        # check if a node with the same name already exists
        host_idx = self.find_node_element(id)
        if host_idx is not None: # if it does
            self.elements.pop(host_idx) # remove it

        # create new node object
        node = n.Node(id)

        # add new node element (to self.elements)
        self.elements.append({
            'data': {'id': node.name, 'label': f'{node.name}\n{node.ipv6_address}'},
            'classes': 'host'
        })

        # increment host counter
        self.n_hosts += 1

    def add_connection(self, id1: str, id2: str, cost: int) -> None:
        # check if connection already exists
        edge_idx = self.find_edge_element(id1, id2)
        if edge_idx is not None: # if it does
            self.elements.pop(edge_idx) # remove it

        # check if both nodes are hosts (hosts can't directly connect to each other)
        if (self.elements[self.find_node_element(id1)]['classes'] == 'host' and
            self.elements[self.find_node_element(id2)]['classes'] == 'host'):
            return

        self.elements.append({'data': {'source': id1, 'target': id2, 'label': str(cost)}})
        print(self.elements[-1])
    
    def remove_node(self, id: str) -> None:
        self.elements = [
            e for e in filter(
                lambda x:
                    x['data'].get('id') != id # filter out nodes with given id
                    and x['data'].get('source') != id  # filter out edges with given id as source
                    and x['data'].get('target') != id, # filter out edges with given id as target
                self.elements
            )
        ]

    def remove_edge(self, src: str, tgt: str) -> None:
        self.elements = [
            e for e in filter(
                lambda x:
                    x['data'].get('source') != src      # filter out edges with
                    or x['data'].get('target') != tgt,  # given source and target
                self.elements
            )
        ]
    
    def get_elements(self):
        return self.elements

    def find_node_element(self, id: str) -> int:
        for i, e in enumerate(self.elements):
            if e['data'].get('id') == id:
                return i
    
    def find_edge_element(self, src: str, tgt: str) -> int:
        for i, e in enumerate(self.elements):
            if (e['data'].get('source') == src and
                e['data'].get('target') == tgt):
                return i
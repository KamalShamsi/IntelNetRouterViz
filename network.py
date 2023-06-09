import node as n
import heapq

import states as st

class NetworkGraph():
    def __init__(self, elements=[]) -> None:
        # these fields are used for network display only
        self.elements = elements
        self.n_hosts = 0
        self.n_routers = 0

        # these fields are used for shortest path calculation
        self.nodes = {}
    
    def add_router(self, id: str) -> None:
        # if node already exists, remove the old one first
        self.remove_node(id)

        # create new node object
        node = n.Node(id)

        # add new node to self.nodes
        self.nodes[id] = node

        # add new node element (to self.elements)
        self.elements.append({
            'data': {
                'id': node.name,
                'label': f'{node.name}\n{node.ipv6_address}',
                'is_highlighted': 'false'
            },
            'classes': 'router'
        })

        # increment router counter
        self.n_routers += 1
    
    def add_host(self, id) -> None:
        # if node already exists, remove the old one first
        self.remove_node(id)

        # create new node object
        node = n.Node(id)

        # add new node to self.nodes
        self.nodes[id] = node

        # add new node element (to self.elements)
        self.elements.append({
            'data': {
                'id': node.name,
                'label': f'{node.name}\n{node.ipv6_address}',
                'is_highlighted': 'false'
            },
            'classes': 'host'
        })

        # increment host counter
        self.n_hosts += 1

    def add_connection(self, id1: str, id2: str, cost: int):
        # find nodes with given id's
        n1 = self.elements[self.find_node_element(id1)]
        n2 = self.elements[self.find_node_element(id2)]

        # check if both nodes are hosts (hosts can't directly connect to each other)
        if (n1['classes'] == 'host' and n2['classes'] == 'host'):
            return st.ErrorState.HOST_HOST_CON
        
        # check if any given node is a host with an existing connection
        for n in [n1, n2]:
            if n['classes'] == 'host' and len(self.nodes[n['data']['id']].neighbors) > 0:
                return st.ErrorState.HOST_SECOND_CON

        
        # if edge already exists, remove the old one first
        self.remove_edge(id1, id2)

        # add neighbor relations to self.nodes accordingly
        self.nodes[id1].add_neighbor(self.nodes[id2], cost)

        self.elements.append({
            'data': {
                'source': id1,
                'target': id2,
                'label': str(cost),
                'is_highlighted': 'false'
            }
        })

        return st.ErrorState.OK
    
    def remove_node(self, id: str) -> None:
        if id in self.nodes:
            # remove node from neighbors of other nodes
            for c, n in self.nodes[id].neighbors:
                n.remove_neighbor(self.nodes[id])
            
            # remove node from self.nodes
            self.nodes.pop(id)

            # remove node and adjacent connections from self.elements
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
        # remove neighbors from self.nodes[src] and self.nodes[tgt]
        if src in self.nodes:
            self.nodes[src].neighbors =\
                [n for n in filter(lambda n: n[1].name != tgt, self.nodes[src].neighbors)]
        if tgt in self.nodes:
            self.nodes[tgt].neighbors =\
                [n for n in filter(lambda n: n[1].name != src, self.nodes[tgt].neighbors)]
            
        # remove edges from self.elements
        self.elements = [
            e for e in filter(
                lambda x:
                    x['data'].get('source') != src      # filter out edges with
                    or x['data'].get('target') != tgt,  # given source and target
                self.elements
            )
        ]

    def dijkstra(self, id1: str, id2: str):
        src, dest = self.nodes[id1], self.nodes[id2]
        distances = {node: float("inf") for node in self.nodes.values()}
        distances[src] = 0
        prev_nodes = {node: None for node in self.nodes.values()}

        queue = [(0, src)]
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
        
        if total_cost == 0: return [],   'Unreachable'
        else:               return path, str(total_cost)
    
    def highlight_path(self, path):
        nodes = [n.name for n in path]
        edges = [set([nodes[i], nodes[i+1]]) for i in range(len(nodes) - 1)]
        for e in self.elements:
            if e['data'].get('id') is not None: # element is a node
                if e['data'].get('id') in nodes:
                    e['data']['is_highlighted'] = 'true'
            else:                               # element is an edge
                # use set to compare unordered pairs
                if set([e['data'].get('source'), e['data'].get('target')]) in edges:
                    e['data']['is_highlighted'] = 'true'
                
    def unhighlight_path(self):
        for e in self.elements:
            e['data']['is_highlighted'] = 'false'
    
    def reset(self):
        self.elements = []
        self.n_hosts = 0
        self.n_routers = 0
        self.nodes = {}

    def get_elements(self):
        return self.elements

    def find_node_element(self, id: str) -> int:
        for i, e in enumerate(self.elements):
            if e['data'].get('id') == id:
                return i
    
    def find_edge_element(self, id1: str, id2: str) -> int:
        for i, e in enumerate(self.elements):
            if (e['data'].get('source') == id1 and
                e['data'].get('target') == id2) or\
               (e['data'].get('target') == id2 and
                e['data'].get('source') == id1):
                return i
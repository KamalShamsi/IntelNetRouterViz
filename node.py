import secrets

class Node:
    def __init__(self, name):
        self.name = name
        self.ipv6_address = "2001:db8::" + secrets.token_hex(2)
        self.neighbors = []

    def add_neighbor(self, neighbor: 'Node', cost: int):
        for c, n in self.neighbors:
            if n == neighbor:
                return
        self.neighbors.append((cost, neighbor))
        neighbor.add_neighbor(self, cost)
    
    def remove_neighbor(self, neighbor: 'Node'):
        for i, cn in enumerate(self.neighbors):
            if cn[1].name == neighbor.name:
                self.neighbors.pop(i)


    def __lt__(self, other):
        return self.name < other.name
    
    def __repr__(self) -> str:
        res = '{' + f'{self.name} ('
        for i, n in enumerate(self.neighbors):
            if i != 0: res += ', '
            res += f'{n[1].name}:{n[0]}'
        return res + ')}'

import random
import heapq
import networkx as nx

class Node:
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
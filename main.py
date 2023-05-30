import random
import heapq

class Router:
    def __init__(self, name):
        self.name = name
        self.ipv6_address = "2001:db8::" + str(random.randint(0, 65535))
        self.neighbors = []

    def add_neighbor(self, neighbor, cost):
        for c, n in self.neighbors:
            if n == neighbor or (self, neighbor) in n.neighbors:
                raise ValueError("Router already has a connection to this neighbor.")
            if c == cost:
                neighbor.add_neighbor(self, cost)
                break
        else:
            self.neighbors.append((cost, neighbor))
            neighbor.add_neighbor(self, cost)


    def dijkstra(self, dest):
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
                    prev_nodes[neighbor] = curr_router  # Update previous node for neighbor
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


# Create routers
num_routers = int(input("Enter number of routers: "))
routers = [Router(f"R{i}") for i in range(1, num_routers+1)]

# Add random neighbors to routers
for i, router in enumerate(routers):
    for j, neighbor in enumerate(routers):
        if i != j:
            cost = random.randint(1, 100)
            try:
                router.add_neighbor(neighbor, cost)
            except ValueError:
                pass

# Keep prompting user to calculate shortest path until they input "exit"
while True:
    # Ask user which router to start from and which router to find shortest path to
    start_router = input(f"Enter router name to start from ({', '.join([router.name for router in routers])}) or type 'exit' to quit: ")
    if start_router == 'exit':
        break
    dest_router = input(f"Enter router name to find shortest path to ({', '.join([router.name for router in routers])}): ")
    try:
        start_router = next(filter(lambda r: r.name == start_router, routers))
        dest_router = next(filter(lambda r: r.name == dest_router, routers))
    except StopIteration:
        print("Invalid input. Try again.")
        continue

    # Calculate the shortest path between routers using Dijkstra's algorithm
    shortest_path, total_cost = start_router.dijkstra(dest_router)
    router_names_and_addresses = [(router.name, router.ipv6_address) for router in shortest_path]
    print("Shortest path:", router_names_and_addresses)
    print("Total cost:", total_cost)
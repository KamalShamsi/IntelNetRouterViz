# IntelNetRouterViz: Network Graph Visualization and Analysis

IntelNetRouterViz is a sophisticated tool designed for network graph visualization and shortest path computation. It employs the Dash framework in conjunction with Dijkstra's algorithm to facilitate the creation and analysis of network topologies, offering a user-friendly interface for network simulation.

## Features:

- **Node Management**: The tool enables users to add or remove nodes (hosts and routers), allowing for dynamic modification of the network topology.
- **Connection Handling**: Users can establish or sever connections between nodes, providing a granular level of control over network structure.
- **Shortest Path Calculation**: Users can select two nodes and utilize Dijkstra's algorithm to compute the shortest path between them. The identified path is then highlighted within the network graph, offering clear and immediate visual feedback.

## Usage Instructions:

1. **Adding Nodes**: Enter the host or router's name in the respective field and select 'Add Host' or 'Add Router'.
2. **Removing Nodes**: Select the node to be removed (using Shift+Click) and click 'Remove'.
3. **Establishing Connections**: Select two nodes (using Shift+Click), input the cost of the connection, and click 'Add Connection'.
4. **Severing Connections**: Select the connection to be removed and click 'Remove'.
5. **Calculating Shortest Paths**: Select a source and a destination node (using Shift+Click), and click 'Shortest Path' to display the shortest path, highlighted within the graph.
6. **Resetting the Network**: Click 'Reset Network' to clear all nodes and connections, enabling the creation of a new network from scratch.

## Constraints:

- Connections can only be established from hosts to routers.
- Each host can connect to a single router only.

## Project Description:

IntelNetRouterViz is an advanced network graph visualization and analysis tool. It blends robust algorithms with intuitive user interactions to offer a comprehensive solution for network topology simulation and analysis. Through this tool, users gain the ability to create, manipulate, and study network graphs, significantly simplifying the process of understanding complex network structures and relationships.

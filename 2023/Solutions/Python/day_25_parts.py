import networkx as nx
import matplotlib.pyplot as plt
import aoc_utils
from pathlib import Path


class Graph:
    def __init__(self, lines):
        self.graph = dict()
        for line in lines:
            for l in line[1].split(" "):
                self.graph.setdefault(line[0], []).append(l)
                self.graph.setdefault(l, []).append(line[0])


    def Make_two_subgraphs(self, test):
        G = nx.Graph()

        for key, value in self.graph.items():
            G.add_node(key)
            for item in value:
                G.add_edge(key, item)

        edge_connectivity = nx.edge_connectivity(G)

        # Find the edges forming the minimum edge cut
        min_edge_cut = nx.minimum_edge_cut(G)

        print(f"\tEdge Connectivity: {edge_connectivity}")
        print("\tEdges in the minimum edge cut:")
        for edge in min_edge_cut:
            print("\t\t",edge)

        # Draw the graph
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=2, node_color='skyblue',
                font_size=1,width=0.1)
        dpi = 1000
        file_name = aoc_utils.save_path(25) / f"{'test_' if test else ''}network.png"
        plt.savefig(file_name, dpi=dpi)
        # pos = nx.spring_layout(G)
        # nx.draw(G, pos, with_labels=True, font_weight='bold', arrowsize=20, node_size=700, node_color='skyblue',
        #         font_size=8)
        # plt.show()

        # Create a copy of the original graph
        graph_copy = G.copy()

        # Remove the edges forming the minimum edge cut
        graph_copy.remove_edges_from(min_edge_cut)

        # Find connected components in the modified graph
        subgraphs = list(nx.connected_components(graph_copy))

        # Print sizes of the two subgraphs
        print("\tSize of Subgraph 1:", len(subgraphs[0]))
        print("\tSize of Subgraph 2:", len(subgraphs[1]))

        return len(subgraphs[0]) * len(subgraphs[1])

if __name__ == "__main__":

    day = int(Path(__file__).name.split('_')[1])
    test = False
    tf = aoc_utils.get_day_input(day, test) 
    lines = [line.split(": ") for line in tf]

    Network = Graph(lines)
    print("Part 1, the multiplication is:", Network.Make_two_subgraphs(test))
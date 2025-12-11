from collections import defaultdict, deque
from aoc_helper import *
import networkx as nx
import matplotlib.pyplot as plt

def bfs3(nodes, start, end):
    Q = deque()
    for n in nodes[start]:
        Q.append((n, False, False))

    visited = set()
    #visited.add("svr")
    count = 0
    while Q:
        dest, sawDac, sawFft = Q.popleft()
        #print(len(Q), len(path))
        if dest == end:
            print(end,sawDac, sawFft)
            #if "dac" in path and "fft" in path:
            #if sawDac and sawFft:
            count += 1
            continue

        visited.add(dest)
        for n in nodes[dest]:
            if n not in visited:
                Q.append((n, sawDac or (n == "dac"), sawFft or (n == "fft")))
        
    return count

def bfs2(nodes, start, end):
    Q = []
    for n in nodes[start]:
        Q.append((n, set([end])))

    visited = set()
    #visited.add("svr")
    count = 0
    while Q:
        dest, path = Q.pop(0)
        #print(len(Q), len(path))
        if dest == end:
            print(path)
            #if "dac" in path and "fft" in path:
            count += 1
            continue

        visited.add(dest)
        for n in nodes[dest]:
            if n not in visited and n not in path:
                npath = set(path)
                npath.add(n)
                Q.append((n, npath))
        
    return count

def bfs(nodes, start="you", end="out"):
    Q = []
    for n in nodes[start]:
        Q.append(n)

    visited = set()
    count = 0
    
    while Q:
        dest = Q.pop(0)

        if dest == end:
            count += 1
            continue

        visited.add(dest)
        for n in nodes[dest]:
            if n not in visited:
                Q.append(n)

    return count

#with open("test.txt") as file:
#with open("test2.txt") as file:
with open("day11.txt") as file:
    lines = file.read().strip().splitlines()

    nodes = defaultdict(list)
    for l in lines:
        p = l.split(" ")
        for dest in p[1:]:
            nodes[p[0][:-1]].append(dest)

    answer(bfs(nodes))

    #invert
    inverted = defaultdict(set)
    for n in nodes:
        for dest in nodes[n]:
            inverted[dest].add(n)

    def visualize_dag(nodes):
        """
        Visualizes a Directed Acyclic Graph (DAG) from a list of edges.

        Parameters:
            edges (list of tuple): List of (source, target) edges.
        """
        try:
            # Create a directed graph
            G = nx.DiGraph()
            for n in nodes.keys():
                for d in nodes[n]:
                    G.add_edge(n, d)

            # Check if the graph is acyclic
            if not nx.is_directed_acyclic_graph(G):
                raise ValueError("The provided edges do not form a DAG.")

            # Layout for better visualization
            pos = nx.spring_layout(G, seed=42)  # deterministic layout

            # Draw nodes and edges
            plt.figure(figsize=(8, 6))
            nx.draw_networkx_nodes(G, pos, node_size=1000, node_color="skyblue")
            nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, edge_color="gray")
            nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

            plt.title("Directed Acyclic Graph (DAG)", fontsize=14)
            plt.axis("off")
            plt.show()

        except Exception as e:
            print(f"Error: {e}")

    # prune cycles
    # depth 20
    # for n in nodes:
    #     visited = set()
    #     Q = [n]
    #     depth = 1
    #     while Q and depth < 20:
    #         next_ = Q.pop(0)
    #         if next_ in visited:
    #             print("cycle")
    #             #Q = []
    #             break
    #         depth += 1
    #         for d in nodes[next_]:
    #             if d not in visited:
    #                 Q.append(d)

    # has to go svr -> fft -> dac -> out
    #answer(bfs2(inverted))
    answer(bfs3(nodes, "svr", "out"))
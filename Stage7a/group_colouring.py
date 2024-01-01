from collections import deque # Import double ended queue from collections library
from data_structures import PriorityQueue # Import priority queue from data structures file

def __are_adjacent(group1, group2):
    coords = set(group1 + group2)
    queue = deque([list(coords)[0]])
    visited = set()
    while queue:
        r, c = queue.popleft()
        visited.add((r, c))
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if (nr, nc) in coords and (nr, nc) not in visited:
                queue.append((nr, nc))
    return len(coords) == len(visited)

def group_colours(groups):
    graph = {head : [] for head in groups.keys()} # Initialise adjacency list to represent the graph

    seen_conns = set()

    # Double for loop to loop through all pairs of groups
    for gp1, _ in groups.values():
        for gp2, _ in groups.values():
            h1, h2 = gp1[0], gp2[0]
            if gp1 != gp2 and tuple(sorted((h1, h2))) not in seen_conns:
                if __are_adjacent(gp1, gp2): # Check if two groups are adjacent
                    graph[h1].append(h2)
                    graph[h2].append(h1) # Add edge between two nodes in graph
                    seen_conns.add(tuple(sorted((h1, h2))))
    
    # Breadth first search with priority queue
    colours = {}
    visited = set()
    queue = PriorityQueue((0, list(graph.keys())[0]))
    while not queue.is_empty():
        _, v = queue.dequeue()
        visited.add(v)
        available_colours = [0, 1, 2, 3, 4]
        for w in graph[v]:
            if w in colours and colours[w] in available_colours:
                available_colours.remove(colours[w])
            if w not in visited:
                queue.enqueue((-sum([1 if u in colours else 0 for u in graph[w]]), w))
        colours[v] = available_colours[0]
    
    # Assign each square in each group their colour
    output = {}
    for head, colour in colours.items():
        squares = groups[head][0]
        for sq in squares:
            output[sq] = colour

    return output # return the output dictionary
from itertools import combinations # Import combinations function from itertools library
from collections import deque # Import double ended queue from collections library
from data_structures import PriorityQueue # Import priority queue from data structures file

def __are_adjacent(group1, group2): # Function to check if two groups are adjacent
    coords = set(group1 + group2) # Set of squares in both groups
    queue = deque([list(coords)[0]]) # Initialise queue with first square
    visited = set() # Set of visited squares
    while queue: # Breadth first search
        r, c = queue.popleft() # Get the current square
        visited.add((r, c)) # Mark it as visited
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc # Find all adjacent squares
            if (nr, nc) in coords and (nr, nc) not in visited: # Check if it is in the set of squares in both groups
                queue.append((nr, nc)) # Push back onto queue
    return len(coords) == len(visited) # Check if number of visited squares is the same as the number of squares in both groups

def group_colours(groups):

    graph = {head : [] for head in groups.keys()} # Initialise adjacency list to represent the graph

    seen_conns = set()

    # Iterate through all combinations of pairs of groups
    for item1, item2 in combinations(tuple(groups.values()), 2):
        gp1, gp2 = item1[0], item2[0]
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
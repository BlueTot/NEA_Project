from itertools import combinations  # Import combinations function from itertools library
from collections import deque  # Import double ended queue from collections library
from data_structures import PriorityQueue  # Import priority queue from data structures file


def __are_adjacent(group1, group2):  # Function to check if two groups are adjacent
    coords = set(group1 + group2)  # Set of squares in both groups
    queue = deque([list(coords)[0]])  # Initialise queue with first square
    visited = set()  # Set of visited squares
    while queue:  # Breadth first search
        r, c = queue.popleft()  # Get the current square
        visited.add((r, c))  # Mark it as visited
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc  # Find all adjacent squares
            if (nr, nc) in coords and (nr, nc) not in visited:  # Check if it is in the set of squares in both groups
                queue.append((nr, nc))  # Push back onto queue
    return len(coords) == len(
        visited)  # Check if number of visited squares is the same as the number of squares in both groups


'''
GROUP A Skill: Graph / Tree Traversal - Group colouring algorithm used to colour in groups on the Killer Sudoku board
'''
def group_colours(groups):  # Group colouring function, takes a dictionary and returns a dictionary

    graph = {head: [] for head in groups.keys()}  # Initialise adjacency list to represent the graph

    seen_conns = set()  # Initialise set of seen edges so edge is only visited once

    # Iterate through all combinations of pairs of groups
    for item1, item2 in combinations(tuple(groups.values()), 2):
        gp1, gp2 = item1[0], item2[0]
        h1, h2 = gp1[0], gp2[0]
        if gp1 != gp2 and tuple(sorted((h1, h2))) not in seen_conns:
            if __are_adjacent(gp1, gp2):  # Check if two groups are adjacent
                graph[h1].append(h2)
                graph[h2].append(h1)  # Add edge between two nodes in graph
                seen_conns.add(tuple(sorted((h1, h2))))

    # Breadth first search with priority queue
    colours = {}  # Initialise colours dictionary
    visited = set()  # Setup set of visited nodes
    queue = PriorityQueue((0, list(graph.keys())[0]))  # Initialise the priority queue

    while not queue.is_empty():  # Loop while the queue is not empty
        _, v = queue.dequeue()  # Dequeue the node with the lowest priority
        visited.add(v)  # Add to set of visited nodes
        available_colours = [0, 1, 2, 3, 4]  # Initialise list of available colours
        for w in graph[v]:  # Iterate through neighbours of v
            if w in colours and colours[w] in available_colours:  # Check if neighbour has been assigned a colour
                available_colours.remove(colours[w])  # Remove the colour from the list of available colours for v
            if w not in visited:  # Check if neighbour has not been visited yet
                queue.enqueue((-sum([1 if u in colours else 0 for u in graph[w]]),
                               w))  # Enqueue  neighbour w with priority = -1 * number of coloured neighbours (-1 is to pull out the node with the most coloured neighbours from the priority queue)
        colours[v] = available_colours[
            0]  # Get the first colour in the list of available colours that hasn't been used yet

    # Assign each square in each group their colour
    output = {}
    for head, colour in colours.items():  # Loop through all groups with a colour
        squares = groups[head][0]  # Get list of squares
        for sq in squares:  # Loop through list of squares in the group
            output[sq] = colour  # Assign the colour of the head square

    return output  # return the output dictionary

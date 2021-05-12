import rubik
from collections import deque

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """
    if start == end: return []

    forward_parents = {start:None}
    backward_parents = {end:None}
    forward_moves = {}
    backward_moves = {}
    for move in rubik.quarter_twists:
        forward_moves[move] = move
        backward_moves[rubik.perm_inverse(move)] = move
    forward = (forward_moves, forward_parents, backward_parents)
    backward = (backward_moves, backward_parents, forward_parents)
    queue = deque([(start, forward), (end, backward), None])

    for i in range(7):
        while True:
            vertex = queue.popleft()
            if vertex is None:
                queue.append(None)
                break
            position = vertex[0]
            moves, parents, other_parents = vertex[1]
            for move in moves:
                next_position = rubik.perm_apply(move, position)
                if next_position in parents: continue
                parents[next_position] = (moves[move], position)
                queue.append((next_position, vertex[1]))
                if next_position in other_parents:
                    forward_path = path(next_position, forward_parents)
                    backward_path = path(next_position, backward_parents)
                    backward_path.reverse()
                    return forward_path + backward_path
    return None

def path(position, parents):
    path = []
    while True:
        move_position = parents[position]
        if move_position == None:
            break
        path.append(move_position[0])
        position = move_position[1]
    path.reverse()
    return path

def BFS(V, Adj, s):
    level = {s:0}
    parent = {s:None}
    i = 1
    frontier = [s]
    while frontier:
        next = []
        for u in frontier:
            for v in Adj[u]:
                if v not in level:
                    level[v] = i
                    parent[v] = u
                    next.append(v)
        frontier = next
        i += 1

from model import TreeNode, GameState, Game
from collections import deque
from heapq import heappush, heappop

# ----------------- HELPER FUNCTIONS -----------------
def initSearch(pieces):
    for piece in pieces:
        piece.visited = False
    return

def depth_search(piece):
    piece.visited = True
    for connectedPiece in piece.connections:
        if not connectedPiece.visited:
            depth_search(connectedPiece)
    return

def breadth_search(piece):
    queue = deque([piece])
    electrons = piece.avElectrons
    while queue:
        node = queue.popleft()
        node.visited = True
        for connectedPiece in node.connections:
            if not connectedPiece.visited:
                electrons += connectedPiece.avElectrons
                queue.append(connectedPiece)
    return electrons
            

# ----------------- HEURISTICS -----------------
def manhattanDistance(piece1, piece2):
    return abs(piece1.position[0] - piece2.position[0]) + abs(piece1.position[1] - piece2.position[1])

# This function will return the sum of minimum distance between the molecule and the nearst atom
def heuristic1(pieces):
    totalDistance = 0
    for index, piece in enumerate(pieces):
        if index == 0 or len(piece.connections) > 0:
            continue
        dist = manhattanDistance(pieces[0], piece)
        totalDistance += dist
    return totalDistance

# This function will return the sum of minimum distance between the molecule and the nearst atom with highest number of available electrons
def heuristic2(pieces):
    totalDistance = 0
    for index, piece in enumerate(pieces):
        if index == 0 or len(piece.connections) > 0:
            continue
        totalDistance += manhattanDistance(pieces[0], piece) * (piece.avElectrons + 1)
    return totalDistance
        


# ----------------- UNIFORMED SEARCH ALGORITHMS -----------------
def BFS(game: Game):
    visited = []
    root = TreeNode(GameState(game.pieces, game.arena))
    queue = deque([root])

    while queue:
        node = queue.popleft()  
        node.treeDepth()
        if node.state.check_win():
            return node
        
        if node not in visited:
            visited.append(node)
            for state in node.state.childrenStates():
                leaf = TreeNode(state[1])
                leaf.prev_move = state[0]
                node.add_child(leaf)
                queue.append(leaf)
    return None

def DFS(game: Game):
    visited = []
    root = TreeNode(GameState(game.pieces, game.arena))
    stack = [root]

    while stack:
        node = stack.pop()  
        node.treeDepth()
        if node.state.check_win():
            return node
        
        if node not in visited:
            visited.append(node)
            for state in node.state.childrenStates():
                leaf = TreeNode(state[1])
                leaf.prev_move = state[0]
                node.add_child(leaf)
                stack.append(leaf)
    return None

def depth_limited_search(game: Game, depth: int):
    visited = []
    root = TreeNode(GameState(game.pieces, game.arena))
    stack = [root]

    while stack:
        node = stack.pop()  
        node.treeDepth()
        if node.state.check_win():
            return node
        
        if node not in visited and node.depth < depth:
            visited.append(node)
            for state in node.state.childrenStates():
                leaf = TreeNode(state[1])
                leaf.prev_move = state[0]
                node.add_child(leaf)
                stack.append(leaf)
    return None

def iterative_deepening_search(game: Game):
    depth = 1
    while True:
        result = depth_limited_search(game, depth)
        if result:
            return result
        depth += 1




# ----------------- INFORMED SEARCH ALGORITHMS -----------------
def greedy_search(game: Game, heuristic):
        root = TreeNode(GameState(game.pieces, game.arena))
        root.heuristicVal = heuristic(root.state.pieces)
        priorityQueue = [] 
        heappush(priorityQueue, (root.heuristicVal, root))
        filtered_states = []

        while priorityQueue:
            _, node = heappop(priorityQueue)
            node.treeDepth()
            if node.state.check_win():
                return node

            children = node.state.childrenStates()
            evaluated_children = [(heuristic(child[1].pieces), child) for child in children]

            for (value, child) in evaluated_children:
                if child in filtered_states:
                    continue
                
                filtered_states.append(child)

                child_tree = TreeNode(child[1])
                child_tree.prev_move = child[0]
                node.add_child(child_tree)
                
                child_tree.heuristicVal = value
                heappush(priorityQueue, (value, child_tree))

        return None


def a_star_search(game: Game, heuristic):
        root = TreeNode(GameState(game.pieces, game.arena))
        root.heuristicVal = heuristic(root.state.pieces)
        priorityQueue = [] 
        heappush(priorityQueue, (root.heuristicVal, root))
        filtered_states = []

        while priorityQueue:
            _, node = heappop(priorityQueue)
            node.treeDepth()
            if node.state.check_win():
                return node

            children = node.state.childrenStates()
            evaluated_children = [(heuristic(child[1].pieces) + node.depth, child) for child in children]

            for (value, child) in evaluated_children:
                if child in filtered_states:
                    continue
                
                filtered_states.append(child)

                child_tree = TreeNode(child[1])
                child_tree.prev_move = child[0]
                node.add_child(child_tree)
                
                child_tree.heuristicVal = value
                heappush(priorityQueue, (value, child_tree))

        return None


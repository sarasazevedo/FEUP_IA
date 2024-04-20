import controller
import copy



valenceElectrons = {"H":1,"O":2,"N":3,"C":4}
atoms = ("H","O","N","C")


# ----------------- MAIN ENTITIES -----------------
class Piece:

    def __init__(self, atom, position, avElectrons):
            self.atom = atom
            self.position = position
            self.avElectrons = avElectrons
            self.connections = []
            self.visited = False
            
# Keep the game board information   
class Arena:
    def __init__(self, level):
        self.board = level["board"]
        self.player_pos = level["player_pos"]
        self.walls = self.listWalls()
        self.cut_pieces = level["cut_pieces"]
    
    def listWalls(self):
        walls = []
        for rindex, row in enumerate(self.board):
            for colindex, cell in enumerate(row):
                if cell not in atoms and cell is not None:
                    walls.append((rindex, colindex))
        return walls

# Keep the game information
class Game:
    def __init__(self, arena: Arena):
        self.arena = arena
        self.pieces = self.listPieces()
        self.Connections()

# Initiaçize all pieces in the game
    def listPieces(self):
        pieces = []
        for rowIndex, row in enumerate(self.arena.board):
            for colIndex, cell in enumerate(row):
                if cell in atoms:
                    piece = Piece(cell, (rowIndex, colIndex), valenceElectrons[cell])
                    if piece.position != self.arena.player_pos:
                        pieces.append(piece)
                    else:
                        pieces.insert(0, piece)
        return pieces

# Create the connections between the atoms
    def Connections(self):
        for i in range(len(self.pieces)):
            for j in range(i+1, len(self.pieces)):
                if controller.nearPieces(self.pieces[i], self.pieces[j]) != "":
                    if self.pieces[i].avElectrons > 0 and self.pieces[j].avElectrons > 0:
                        self.pieces[i].connections.append(self.pieces[j])
                        self.pieces[i].avElectrons -= 1
                        self.pieces[j].connections.append(self.pieces[i])
                        self.pieces[j].avElectrons -= 1
                

# ----------------- SEARCH ALGORITHM ENTITIES -----------------
# Keep the game state information
class GameState:
    def __init__(self, pieces, arena):
        self.pieces = pieces
        self.arena = arena

    def __eq__(self, other):
        return isinstance(other, GameState) and self.comparePieces(other)

    def comparePieces(self, other):
        for i in range(len(self.pieces)):
            if self.pieces[i].atom != other.pieces[i].atom or self.pieces[i].position != other.pieces[i].position or self.pieces[i].avElectrons != other.pieces[i].avElectrons:
                return False
            if len(self.pieces[i].connections) != len(other.pieces[i].connections):
                return False
            for j in range(len(self.pieces[i].connections)):
                if self.pieces[i].connections[j].position != other.pieces[i].connections[j].position:
                    return False
        return True

    def __hash__(self):
        return hash(str(self.pieces))

    def __str__(self):
        return "GameState(" + str(self.pieces) + ")"

    def __repr__(self):
        return str(self)
    
    def valid_gamestate(self, direction):
        return controller.validateMove(self.pieces, direction, self.arena)
    
    def move_left(self):
        if self.valid_gamestate("left"):
            state = GameState(controller.changeState(copy.deepcopy(self.pieces), "left", self.arena), self.arena)
            if not controller.impossible_solution(state.pieces, state.arena):
                return state
    
    def move_right(self):
        if self.valid_gamestate("right"):
            state = GameState(controller.changeState(copy.deepcopy(self.pieces), "right", self.arena), self.arena)
            if not controller.impossible_solution(state.pieces, state.arena):
                return state
    
    def move_up(self):
        if self.valid_gamestate("up"):
            state = GameState(controller.changeState(copy.deepcopy(self.pieces), "up", self.arena), self.arena)
            if not controller.impossible_solution(state.pieces, state.arena):
                return state
    
    def move_down(self):
        if self.valid_gamestate("down"):
            state = GameState(controller.changeState(copy.deepcopy(self.pieces), "down", self.arena), self.arena)
            if not controller.impossible_solution(state.pieces, state.arena):
                return state
    
    def childrenStates(self):
        children = []
        movement_methods = [("left", self.move_left), ("right", self.move_right), ("up", self.move_up), ("down", self.move_down)]
        for move in movement_methods:
            childState = (move[1])()
            if childState is not None:
                children.append((move[0],childState))
        return children

    def check_win(self):
        return controller.endGame(self.pieces)
    
# Keep the tree node information to be used in the search algorithm helping to have a tree structure
class TreeNode:
    def __init__(self, state, prev_move=None, parent=None, heuristicVal=0):
        self.state = state
        self.prev_move = prev_move
        self.parent = parent
        self.heuristicVal = heuristicVal
        self.treeDepth()
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self
        self.treeDepth()

    def treeDepth(self):
        if self.parent is None:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1
    
    def __eq__(self, other):
        return isinstance(other, TreeNode) and self.state == other.state

    def __hash__(self):
        return hash(str(self.state) + str(self.depth))

    def __str__(self):
        return "TreeNode(" + str(self.state) + ", " + str(self.depth) + ")"

    def __repr__(self):
        return str(self)
    
    def __lt__(self, other):
        return self.heuristicVal < other.heuristicVal
    
    def print_solution(self):
        stack = []
        current = self
        while current is not None:
            stack.append(current.prev_move)
            current = current.parent
        stack.pop() # First element of stack is None (root)
        while len(stack)>1:
            print(stack.pop(), " -> ", end="")
        print(stack.pop())
        return
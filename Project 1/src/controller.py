import algorythms
import copy


# ATENTION: The y axis is turned upside down, so to go up you have to subtract 1, and add 1 to go down!!!
moves = {"right": (0,1), "left": (0,-1), "up": (-1,0), "down": (1,0)}

# ----------------- MOVE PIECES FUNCTIONS ----------------- 
def movePiece(game, direction, prev_states):
    if direction not in moves.keys():
        raise ValueError("Invalid direction")
    
    if validateMove(game.pieces, direction, game.arena) == False:
        return
    
    prev_states.append(copy.deepcopy(game.pieces))
    
    changeState(game.pieces, direction, game.arena)
    

def changeState(pieces, direction, arena):
    algorythms.initSearch(pieces)
    for piece in pieces:
        if not piece.visited:
            piece.visited = True
            cutConnections(piece, direction, arena)
    
    algorythms.initSearch(pieces)
    
    pivot = pieces[0]
    new_poss = [(pivot.position[0] + moves[direction][0], pivot.position[1] + moves[direction][1])]
    pivot.position = (pivot.position[0] + moves[direction][0], pivot.position[1] + moves[direction][1])
    pivot.visited = True
    moveAjacentPiece(pieces, direction, pivot, new_poss)
    
    newConnections(pieces)

    return pieces

# ----------------- HELPER TO MOVE PIECES -----------------
# See new connections
def newConnections(pieces):
    for piece in pieces:
        for possibleConnection in pieces:
            if piece != possibleConnection and possibleConnection not in piece.connections and (nearPieces(piece, possibleConnection) != "") and piece.avElectrons > 0 and possibleConnection.avElectrons > 0:
                piece.connections.append(possibleConnection)
                piece.avElectrons -= 1
                possibleConnection.connections.append(piece)
                possibleConnection.avElectrons -= 1
    return

# Move adjacent pieces in order to keep the molecule together
def moveAjacentPiece(pieces, direction, pivot, new_poss):
    for piece in pivot.connections:
        if not piece.visited:
            new_poss.append((piece.position[0] + moves[direction][0], piece.position[1] + moves[direction][1]))
            piece.position = (piece.position[0] + moves[direction][0], piece.position[1] + moves[direction][1])
            piece.visited = True
            moveAjacentPiece(pieces, direction, piece, new_poss)
    
    for piece in pieces:
        if piece.position in new_poss and piece != pivot and piece not in pivot.connections and not piece.visited:
            new_poss.append((piece.position[0] + moves[direction][0], piece.position[1] + moves[direction][1]))
            piece.position = (piece.position[0] + moves[direction][0], piece.position[1] + moves[direction][1])
            piece.visited = True
            moveAjacentPiece(pieces, direction, piece, new_poss)
    return

# remove connections
def cutConnections(pivot, direction, arena):
    cutCrossing = []
    for connectedPiece in pivot.connections:
        if not connectedPiece.visited:
            if not checkDotCrossing(pivot, connectedPiece, direction, arena.cut_pieces):
                connectedPiece.visited = True
                cutConnections(connectedPiece, direction, arena)
            else:
                cutCrossing.append(connectedPiece)
    for cuttedPiece in cutCrossing:
        pivot.connections.remove(cuttedPiece)
        pivot.avElectrons += 1
        cuttedPiece.connections.remove(pivot)
        cuttedPiece.avElectrons += 1


# ----------------- VALIDATE MOVE FUNCTIONS -----------------
def validateMove(pieces, direction, arena):
    pivot = pieces[0]
    algorythms.initSearch(pieces)
    pieces[0].visited = True
    return checkMovePiece(pivot, pieces, direction, arena)

def checkMovePiece(pivot, pieces, direction, arena):
    if(wallCollision(pivot, arena, direction)):
        return False
    for otherPiece in pieces:
        if (nearPieces(pivot, otherPiece) == direction and otherPiece not in pivot.connections):
            result = checkMovePiece(otherPiece, pieces, direction, arena)
            if result == False:
                return False

    for connectedPiece in pivot.connections:
        if not connectedPiece.visited:
            if not checkDotCrossing(pivot, connectedPiece, direction, arena.cut_pieces):
                connectedPiece.visited = True
                result = checkMovePiece(connectedPiece, pieces, direction, arena)
                if result == False:
                    return False

    return True

def wallCollision(pivot, arena, direction):
    new_move = (pivot.position[0] + moves[direction][0], pivot.position[1] + moves[direction][1])
    if(new_move in arena.walls):
        return True
    return False

def nearPieces(piece1, piece2):
    if piece1.position[1] == piece2.position[1]:
        if (piece1.position[0] + 1 == piece2.position[0]):
            return "down"
        if (piece1.position[0] - 1 == piece2.position[0]):
            return "up"
    if piece1.position[0] == piece2.position[0]:
        if (piece1.position[1] + 1 == piece2.position[1]):
            return "right"
        if (piece1.position[1] - 1 == piece2.position[1]):
            return "left"
    return ""

def checkDotCrossing(pivot, connectPiece, direction, dotsArray):
    connectedDir = nearPieces(pivot, connectPiece)

    # Tuple with the expected direction of the dot
    # The first element is the direction of the connected piece relative to the pivot
    # The second element is the direction chosen by the player
    directions = {
        ("right", "up"): (0, 1),
        ("right", "down"): (1, 1),
        ("left", "up"): (0, 0),
        ("left", "down"): (1, 0),
        ("up", "right"): (0, 1),
        ("up", "left"): (0, 0),
        ("down", "right"): (1, 1),
        ("down", "left"): (1, 0),
    }

    for dot in dotsArray:
        maxDotDist = max(abs(dot[0] - pivot.position[0]), abs(dot[1] - pivot.position[1]))
        if maxDotDist > 1 or (connectedDir, direction) not in directions.keys():
            continue
        expected_position = (pivot.position[0] + directions[(connectedDir, direction)][0], pivot.position[1] + directions[(connectedDir, direction)][1])
        if dot == expected_position:
            return True

    return False


# ----------------- WINNING VERIFICATION FUNCTION -----------------
def endGame(pieces):
    algorythms.initSearch(pieces)
    algorythms.depth_search(pieces[0])
    for piece in pieces:
        if not piece.visited or piece.avElectrons > 0:
            return False
    return True

# ----------------- IMPOSSIBLE SOLUTION FUNCTION -----------------
# This function will return True if from this stage onwards it will not be possible to reach a solution, discarding these branches will help the search algorithms
def impossible_solution(pieces, arena):
    if arena.cut_pieces:
        return False
    algorythms.initSearch(pieces)
    molecules = []
    for piece in pieces:
        if not piece.visited:
            electrons = algorythms.breadth_search(piece)
            molecules.append(electrons)
    for electrons in molecules:
        if electrons == 0 and len(molecules) > 1:
            return True
    return False


    

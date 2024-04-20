import pygame
import controller
from levels import levels
import view
from model import Game, Arena
from algorythms import DFS, BFS, greedy_search, a_star_search, iterative_deepening_search, heuristic1, heuristic2
import copy
import time

# ATENTION: The y axis is turned upside down, so to go up you have to subtract 1, and add 1 to go down!!!

# pygame setup
pygame.init()
view.init()
clock = pygame.time.Clock()
running = True
dt = 0

# The options in the menu
menu_options = ["start game", "about", "quit"]
menu_option_selected = 0
about = False

#Level Options
level_option = ["","Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", "Level 8", "Level 9", "Level 10"]
level_option_selected = 0
level_menu = False

#IA Options
menu_ia_options = ["Play", "IA Play"]
menu_ia_selected = 0
menu_ia = False

#Algorithm Options
algorithm_options = ["DFS", "BFS", "Greedy", "A*", "Iterative Deepening"]
algorithm_selected = 5
algorithm_menu = False

#Heuristics Options
heuristics_options = ["","1", "2"]
ai_heuristics = [None, heuristic1, heuristic2]
heuristics_selected = 0
heuristics_menu = False

# Variable to track if the game has started
game_started = False
victory = False

# Player position
game = None
arena = None
prev_states = []
ai_result = 0
ai_done = False
ai_moves = []

# Game Stats
time_elapsed = 0
time_start = 0
total_moves = 0

def initializeVariables():
    global menu_option_selected, about, level_option_selected, level_menu, menu_ia_selected
    global menu_ia, algorithm_selected, algorithm_menu, heuristics_selected, heuristics_menu, game_started, victory
    global game, arena, prev_states, ai_result, ai_done, ai_moves, time_elapsed, time_start, total_moves

    menu_option_selected = 0
    about = False

    level_option_selected = 0
    level_menu = False

    menu_ia_selected = 0
    menu_ia = False

    algorithm_selected = 5
    algorithm_menu = False

    heuristics_selected = 0
    heuristics_menu = False

    game_started = False
    victory = False

    game = None
    arena = None
    prev_states = []
    ai_result = 0
    ai_done = False
    ai_moves = []

    time_elapsed = 0
    time_start = 0
    total_moves = 0


# AI: get the moves from the AI
def getMoves(state):
    moves = []
    while state.parent != None:
        moves.append(state)
        state = state.parent
    return moves
    

# ----------------- MAIN LOOP -----------------
while running:
    # AI: run the AI
    if menu_ia_selected == 1 and game_started and not ai_done: 
        ai_done = True
        view.displayLoading()
        time_start = time.time()
        if algorithm_selected == 0:
            ai_result = DFS(game)
        elif algorithm_selected == 1:
            ai_result = BFS(game)
        elif algorithm_selected == 2:
            ai_result = greedy_search(game, ai_heuristics[heuristics_selected])
        elif algorithm_selected == 3:
            ai_result = a_star_search(game, ai_heuristics[heuristics_selected])
        elif algorithm_selected == 4:
            ai_result = iterative_deepening_search(game)
        ai_moves = getMoves(ai_result)
        time_elapsed = time.time() - time_start
        total_moves = len(ai_moves)
    # AI: handle the AI moves
    if menu_ia_selected == 1 and game_started and ai_done:
        if len(ai_moves) > 0:
            game = ai_moves.pop().state
            pygame.time.delay(700)
            
    # CONTROLLER: handle the events
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    initializeVariables()
                if victory:
                    if event.key == pygame.K_RETURN: 
                        initializeVariables()
                elif not game_started and not level_menu and not menu_ia and not algorithm_menu and not about and not heuristics_menu:
                    if event.key in (pygame.K_w, pygame.K_UP):
                        menu_option_selected = (menu_option_selected - 1) % len(menu_options)
                    if event.key in (pygame.K_s, pygame.K_DOWN):
                        menu_option_selected = (menu_option_selected + 1) % len(menu_options)
                    if event.key == pygame.K_RETURN:  
                        if menu_options[menu_option_selected] == "start game":
                            menu_ia = True
                        elif menu_options[menu_option_selected] == "about":
                            print("about")
                            about = True
                        elif menu_options[menu_option_selected] == "quit":
                            running = False
                elif about:
                    if event.key == pygame.K_RETURN: 
                        about = False
                elif menu_ia:
                    if event.key in (pygame.K_w, pygame.K_UP):
                        menu_ia_selected = (menu_ia_selected - 1) % len(menu_ia_options)
                    if event.key in (pygame.K_s, pygame.K_DOWN):
                        menu_ia_selected = (menu_ia_selected + 1) % len(menu_ia_options)
                    if event.key == pygame.K_RETURN: 
                        if menu_ia_options[menu_ia_selected] == "Play":
                            level_menu = True
                        elif menu_ia_options[menu_ia_selected] == "IA Play":
                            algorithm_menu = True
                        menu_ia = False
                elif algorithm_menu:
                    if event.key in (pygame.K_w, pygame.K_UP):
                        algorithm_selected = (algorithm_selected - 1) % (len(algorithm_options)+1)
                    if event.key in (pygame.K_s, pygame.K_DOWN):
                        algorithm_selected = (algorithm_selected + 1) % (len(algorithm_options)+1)
                    if event.key == pygame.K_RETURN: 
                        if algorithm_selected in [0,1,4]: 
                            algorithm_menu = False
                            level_menu = True
                        if algorithm_selected in [2,3]:
                            algorithm_menu = False
                            heuristics_menu = True      
                elif heuristics_menu:
                    if event.key in (pygame.K_w, pygame.K_UP):
                        heuristics_selected = (heuristics_selected - 1) % 3
                    if event.key in (pygame.K_s, pygame.K_DOWN):
                        heuristics_selected = (heuristics_selected + 1) % 3
                    if event.key == pygame.K_RETURN: 
                        if heuristics_selected in [1,2]:
                            level_menu = True
                            heuristics_menu = False
                elif level_menu:
                    if event.key in (pygame.K_w, pygame.K_UP):
                        level_option_selected = (level_option_selected - 1) % len(level_option)
                    if event.key in (pygame.K_s, pygame.K_DOWN):
                        level_option_selected = (level_option_selected + 1) % len(level_option)
                    if event.key == pygame.K_RETURN and level_option_selected != 0 and level_option_selected < len(level_option): 
                        arena = Arena(levels[level_option_selected])
                        game = Game(arena)
                        level_menu = False
                        game_started = True
                        time_start = time.time()
                        prev_states.append(copy.deepcopy(game.pieces))
                else:
                    if event.key in (pygame.K_s, pygame.K_DOWN):
                        controller.movePiece(game, "down", prev_states)
                    if event.key in (pygame.K_w, pygame.K_UP):
                        controller.movePiece(game, "up", prev_states)
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        controller.movePiece(game, "left", prev_states)
                    if event.key in (pygame.K_d, pygame.K_RIGHT):
                        controller.movePiece(game, "right", prev_states)
                    
                    if event.key == pygame.K_r:
                        game = Game(arena)
                        prev_states = []
                        time_start = time.time()
                    if event.key == pygame.K_z:
                        if len(prev_states) > 0:
                            last_state = prev_states.pop()
                            game.pieces = last_state

    # VIEW: display the game
    view.display(game, menu_options, menu_option_selected, game_started, level_option, level_option_selected, level_menu, menu_ia, menu_ia_selected, menu_ia_options, algorithm_menu, algorithm_options, algorithm_selected, about, victory, time_elapsed, total_moves, heuristics_selected, heuristics_menu)
    dt = clock.tick(60) / 1000

    # VICTORY: handle the end of the game
    if game_started and controller.endGame(game.pieces) and not victory:
        if not (menu_ia_selected == 1):
            time_elapsed = time.time() - time_start
            total_moves = len(prev_states) - 1
        pygame.time.delay(1000)
        victory = True

        
pygame.quit()



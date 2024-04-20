#Blue is the piece that moves 
#Red the other symbols
#yellow is the wall


levels = {
    #Level 1 - Cell
    1: {"board" : [
    ['y', 'y', 'y', 'y', 'y', 'y'],
    ['y', 'H', None, None, 'O', 'y'],
    ['y', None, None, None, None, 'y'],
    ['y', None, 'H', 'y', 'y', 'y'],
    ['y', 'y', 'y', 'y', None, None]],
    "player_pos" : (1,1),
    "cut_pieces" : []
    },

    #Level 2 - Loop
    2: {"board" : [
    ['y', 'y', 'y', 'y', 'y', 'y', 'y'],
    ['y', None, None, 'O', None, None, 'y'],
    ['y', None, None, 'y', None, None, 'y'],
    ['y', None, 'H', 'y', 'H', None, 'y'],
    ['y', None, None, 'y', None, None, 'y'],
    ['y', None, None, 'O', None, None, 'y'],
    ['y', 'y', 'y', 'y', 'y', 'y', 'y']],
    "player_pos" : (3,2),
    "cut_pieces" : []
    },

    
    #Level 3 - Split
    3: {"board" : [
        [None,None,'y','y','y','y','y','y',None,None],
        [None,None,'y',None,None,None,None,'y',None,None],
        [None,None,'y',None,None,None,None,'y',None,None],
        ['y','y','y',None,None,None,None,'y','y','y'],
        ['y','H','H',None,None,None,None,None,'O','y'],
        ['y','y','y','y','y','y','y','y','y','y']],
        "player_pos" : (4,1),
        "cut_pieces" : [(3,5)]
    },

    #Level 4 - Around
    4: {"board" : [
        [None,'y','y','y','y','y',None],
        ['y','y',None,None,None,'y','y'],
        ['y',None,None,'H',None,None,'y'],
        ['y',None,'H','y','H',None,'y'],
        ['y',None,None,'H',None,None,'y'],
        ['y','y',None,'C',None,'y','y'],
        [None,'y','y','y','y','y',None]],
        "player_pos" : (2,3),
        "cut_pieces" : [(3,3),(4,3),(3,4),(4,4)]
    },
    
    #Level 5 - RoadRunner
    5: {"board" : [
    ['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y'],
    ['y', None, None, None, None, None, None, None, 'y'],
    ['y', None, None, 'H', None, 'H', None, None, 'y'],
    ['y', None, 'O', None, None, None, 'C', None, 'y'],
    ['y', None, None, 'H', None, 'H', None, None, 'y'],
    ['y', None, None, None, None, None, None, None, 'y'],
    ['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y']],
    "player_pos" : (3,2),
    "cut_pieces" : []
    },

    #Level 6 - Infinity
    6: {"board" : [
        [None,'y','y','y',None,'y','y','y',None],
        ['y','y','H','y','y','y','H','y','y'],
        ['y',None,None,None,'y',None,None,None,'y'],
        ['y',None,None,None,'C',None,None,None,'y'],
        ['y',None,None,None,'y',None,None,None,'y'],
        ['y','y','H','y','y','y','H','y','y'],
        [None,'y','y','y',None,'y','y','y',None]],
        "player_pos" : (1,2),
        "cut_pieces" : [(2,2),(2,3),(2,6),(2,7),(3,4),(4,4),(3,5),(4,5),(5,2),(5,3),(5,6),(5,7)]
    },

    #Level 7 - Chandelier
    7: {"board" : [
        [None, 'y','y','y','y','y',None],
        ['y', 'y',None,'H',None,'y','y'],
        ['y', None,None,None,None,None,'y'],
        ['y', 'H',None,'O',None,'H','y'],
        ['y', None,None,None,None,None,'y'],
        ['y', 'H','C',None,'C','H','y'],
        ['y', None,None,None,None,None,'y'],
        ['y', None,None,'H',None,None,'y'],
        ['y', 'y','y','y','y','y','y']],
        "player_pos" : (1,3),
        "cut_pieces" : []
    },

    #Level 8 - Kruskal
    8: {"board" : [
        ['y','y','y','y','y','y','y'],
        ['y',None,None,'y',None,None,'y'],
        ['y','H',None,'O',None,'H','y'],
        ['y',None,None,None,None,None,'y'],
        ['y',None,None,'C',None,None,'y'],
        ['y',None,None,None,None,None,'y'],
        ['y','H',None,'O',None,'H','y'],
        ['y',None,None,'y',None,None,'y'],
        ['y','y','y','y','y','y','y']],
        "player_pos" : (4,3),
        "cut_pieces" : []
    },
    
    #Level 9 - Plunge (Unfeasible)
    9: {"board" : [
        ['y','y','y','y','y',None,None,None,None,None],
        ['y','C',None,'H','y','y','y','y','y',None],
        ['y',None,None,None,'y','H','y','H','y','y'],
        ['y',None,'O',None,None,None,None,None,None,'y'],
        ['y',None,None,None,'y','H','y','H','y','y'],
        ['y','C',None,'H','y','y','y','y','y',None],
        ['y','y','y','y','y',None,None,None,None,None]],
        "player_pos" : (3,2),
        "cut_pieces" : [(2,2),(3,2),(2,3),(3,3),(4,2),(4,3),(5,2),(5,3),(3,4),(4,4),(4,6),(3,6)]
    },
    
    #Level 10 - Grand Slam (Unfeasible)
    10: {"board" : [
        [None, 'y','y','y','y','y','y','y','y','y'],
        [None, 'y',None,None,'H',None,None,None,None,'y'],
        ['y', 'y','H',None,'C',None,'H',None,None,'y'],
        ['y', None,None,None,None,None,None,'H',None,'y'],
        ['y', 'O',None,None,'C',None,None,None,None,'y'],
        ['y', None,None,None,None,None,None,'H',None,'y'],
        ['y', 'y','H',None,'C',None,'H',None,None,'y'],
        [None, 'y',None,None,'H',None,None,None,None,'y'],
        [None, 'y','y','y','y','y','y','y','y','y']],
        "player_pos" : (4,1),
        "cut_pieces" : []
    }
        
}
    

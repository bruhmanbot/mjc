# How to optimally discard?

from usefulTiles import usefulness_ps, usefulness_ss
from hand_situation import *
# from drawing_game import *

import random
import sys
sys.path.append('../mjcpy')

from listUtils import * # type: ignore

def getRandomUselessTile(tileDict: dict) -> any:
    # Matches the tile info against the min and see if it is the most useless one
    # gets all the useless tiles and outputs a random one : Simulate human behaviour
    worst = []
    try: 
        minT = min(tileDict.values())
    except ValueError:
        print(f'tileDict: {tileDict}')
        print('Program exited in getRandomUselessTile')
        quit()
    for t in tileDict:
        # tileDict[t] -> float e.g. 3.0
        if tileDict[t] == minT:
            worst.append(t)
    
    return random.choice(worst)
    

    

def findOptimalDiscard(inner_hand:list, knownPile:list, full_eval_mode=False, priority='str') -> int:
    # Uses functions to see which tile is the least useful
    # Flow -> Identify sets and partial sets
    # Runs functions to see amt of useful tiles for partial sets
    # Runs functiopn to see amy of useful tiles for singles
    # Priority: Useless partial sets < Singles < Partial sets
    # Rationale:
    # Useless partial sets --> 0% to make full set
    # singles --> Slight chance to make full set (but not quick)
    # Partial sets --> Almost complete (high chance to reach complete set)
    
    # Run the recursion (deeper analysis version) if specified
    if full_eval_mode:
        hScore, partialSets, singleTiles = hand_eval_adv(inner_hand, [])
    else:
        hScore, partialSets, singleTiles = hand_eval(inner_hand, [], priority=priority)

    # Running the usefulness function
    psInfo = usefulness_ps(partialSets, knownPile)

    # Here as well
    ssInfo = usefulness_ss(singleTiles, knownPile)

    # if no ps (handle exception)
    if len(psInfo.keys()) == 0:
        # no ps so should only be singles
        # if no ps and no singles --> already won
        if type(getRandomUselessTile(ssInfo)) is int:
            return getRandomUselessTile(ssInfo)
        else:
            return 'win??'
        # directly returns least useful tile

    # Following code executed if no errors
    if min(psInfo.values()) == 0:
        # See if we have a useless partial set
        uselessSetTiles = []

        # Add tiles to uselessSetTiles if the ps is useless
        for q in psInfo:
            if psInfo[q] == 0:
                uselessSetTiles = uselessSetTiles + list(q)

        uselessSet_indTileInfo = usefulness_ss(uselessSetTiles, knownPile)


        # return the less useful tile (when considered single)
        return getRandomUselessTile(uselessSet_indTileInfo)
    
    # If no useless partial sets
    if len(ssInfo.keys()) == 0:
        # No singled tiles

        ## Runs the same function on the least useful partial set
        uselessSetTiles = []
        for q in psInfo:
            if psInfo[q] == min(psInfo.values()):
                uselessSetTiles = uselessSetTiles + list(q)

        uselessSet_indTileInfo = usefulness_ss(uselessSetTiles, knownPile)

        # return the less useful tile (when considered single)
        return getRandomUselessTile(uselessSet_indTileInfo)
    
    else:
        # have singled out tiles
        return getRandomUselessTile(ssInfo)

if __name__ == '__main__':
    known = [11, 12, 13, 14, 14, 15, 17, 18, 22, 25, 25, 26, 27, 36, 37, 43, 45]

    hand = [11, 12, 13, 14, 15, 18, 18, 33, 33, 33, 35, 36, 37, 23]

    print(findOptimalDiscard(hand, known))
        
    



    

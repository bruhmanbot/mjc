# How to optimally discard?

from usefulTiles import usefulness_ps, usefulness_ss, sortdict
from hand_situation import *
from drawing_game import *

import random
import sys
sys.path.append('P:/mjc-main/mjcpy')

from listUtils import * # type: ignore

def getRandomUselessTile(tileDict: dict) -> int:
    # Matches the tile info against the min and see if it is the most useless one
    # gets all the useless tiles and outputs a random one : Simulate human behaviour
    worst = []
    minT = min(tileDict.values())
    for t in tileDict:
        # tileDict[t] -> float e.g. 3.0
        if tileDict[t] == minT:
            worst.append(t)
    
    return random.choice(worst)
    

    

def findOptimalDiscard(inner_hand:list, knownPile:list) -> int:
    # Uses functions to see which tile is the least useful
    # Flow -> Identify sets and partial sets
    # Runs functions to see amt of useful tiles for partial sets
    # Runs functiopn to see amy of useful tiles for singles
    # Priority: Useless partial sets < Singles < Partial sets
    # Rationale:
    # Useless partial sets --> 0% to make full set
    # singles --> Slight chance to make full set (but not quick)
    # Partial sets --> Almost complete (high chance to reach complete set)
    hScore, partialSets, singleTiles = hand_eval(inner_hand, 'str')

    # Running the usefulness function
    psInfo = usefulness_ps(partialSets, knownPile)

    # Here as well
    ssInfo = usefulness_ss(singleTiles, knownPile)

    # if no ps (handle exception)
    if len(psInfo.keys()) == 0:
        # no ps so should only be singles
        # if no ps and no singles --> already won
        return getRandomUselessTile(ssInfo)
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

    hand = [11, 12, 13, 14, 14, 15, 17, 18, 22, 25, 25, 26, 27, 36, 37, 43, 45]

    print(findOptimalDiscard(hand, known))
        
    



    

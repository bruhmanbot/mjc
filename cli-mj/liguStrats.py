from usefulTiles import sortdict
import sys
import random
sys.path.append('../mjcpy')

from listUtils import * # type: ignore

def findOptimalDiscardLigu(inner_hand: list, knownPile: list):
    # Finds the optimal discard tile for a ligu hand
    # Goal: 1x Triplet + 7x Pairs
    # General flow:
    # Find the pairs
    # Find the triplet --> Remaining singles
    # Discard least probable single using info from known pile
    inner_hand_wk = inner_hand.copy()
    # Non destructive function
    singles = find_occurence(inner_hand, 1) # type:ignore

    trips = find_occurence(inner_hand_wk, 3) # type: ignore
    tripInfo = {}
    uselessTrips = []
    # 1 == possible, 0 == impossible
    # If the hand survives the loop --> all trips are possible
    # Statisically equal chance for discarding any of them
    for i in trips:
        tripInfo[i] = 4 - knownPile.count(i)
        if tripInfo[i] == 0:
            uselessTrips.append(i)

    if len(singles):
        # have remaining singles
        singleInfo = {}
        for t in singles:
            singleInfo[t] = 4 - knownPile.count(t)
        
        # Sort singleInfo to find least likely tile to draw
        worst = min(singleInfo.values())
        worstTiles = []
        for t in singleInfo:
            if singleInfo[t] == worst:
                worstTiles.append(t)

        # Returns a random choice from the worst possible options
        # Consider useless trips if there are too many triplets
        if len(trips) > 1:
            worstTiles = worstTiles + uselessTrips

        return int(random.choice(worstTiles))

    # 2 and 4 are perfect
    # Mainly only happen in the case of 3 triplets + 4 pairs
    # In which case discarding the least likely triplet is ideal
    
    else:
        return int(random.choice(trips))

if __name__ == '__main__':
    from drawing_game import *
    from ligu_check import ligu_hand_validity_check # type: ignore

    tileDeck = deckInit()
    discard = []

    # original draw of 16 tiles (NO FLOWERS!!)
    player1_hand, tileDeck = draw(1, 16, tileDeck)
    player1_flowers = []


    while True:
        if (len(tileDeck) == 0):
            break
        # Draw tiles for player 1
        player1_hand, player1_flowers, tileDeck = playerdraw(player1_hand, player1_flowers, tileDeck)

        if ligu_hand_validity_check(player1_hand[:-1], [], player1_hand[-1:]):
            print (f'{120 - len(tileDeck)}')
            break
            
            
        optimalDiscard = findOptimalDiscardLigu(player1_hand, (discard+player1_hand))

        # Ask discard tile
        player1_hand.remove(optimalDiscard)
        discard.append(optimalDiscard)
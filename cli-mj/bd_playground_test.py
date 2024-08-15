# the playground for calling
# Only analysis up to the calling point

from drawing_game import *
from buddhastrats import buddha_findBestDiscard
from check_calling import check_calling_tiles_bd
from hand_situation import hand_eval

import pandas as pd
from multiprocessing import Pool

import sys
sys.path.append('../mjcpy')
from buddha_check import buddha_hand_validity_check # type:ignore



def simulate_game_bd(threshold=0, mode='large'):
    tileDeck = deckInit()
    discard = []

# original draw of 16 tiles
    player1_hand, tileDeck = draw(1, 16, tileDeck)
    player1_flowers = []
# Clear the list
    player1_hand.sort()

    handScore, partial, singles = hand_eval(player1_hand, [],priority='str')

    if mode == 'large':
        if handScore <= threshold:
            return (0), 0
    else:
        if handScore > threshold:
            return (0), 0
        
    startingLT = list(filter(lambda x: x>40, player1_hand))
    numStartingLT = len(set(startingLT))

    while True:
    # Print tiles remaining in the sea
    # print (f'Tiles remaining at the sea: {len(tileDeck)}')
    # Draw tiles for player 1
        if len(tileDeck) == 0:
            return (handScore, 128, [])
        

        player1_hand, player1_flowers, tileDeck = playerdraw(player1_hand, player1_flowers, tileDeck)


        
    # print (f'Hand score: {handScore}')

    # print(countUsefulTiles(partial, singles, discard))
        bestDiscard: int = buddha_findBestDiscard(player1_hand, (discard+player1_hand))
        # print(f'Suggested discard: {bestDiscard}')
    # Ask discard tile
        discard.append(bestDiscard)
        player1_hand.remove(bestDiscard)

        player1_hand.sort()

    # check hand - calling analysis
        bdvalid_calling:dict = check_calling_tiles_bd(player1_hand, [], output_score=False)

        if len(bdvalid_calling.keys()) > 0:
            outputTuple = (handScore, 120 - len(tileDeck), numStartingLT, tuple(bdvalid_calling.keys()))
            return outputTuple

if __name__ == '__main__':
    import time
    
    epochs = 22

    
    data = [0] * epochs
    start = time.time()
    
    print('Multi starting~')    
    poo = Pool(processes=4)
    results = poo.imap_unordered(simulate_game_bd, data)

    df = pd.DataFrame(results, columns=['openingScore', 'tileUsed', 'startingLT', 'keys'])

    end2 = time.time()
    delta2 = end2-start
    print(f'Multi mode finished in {delta2}s')

    # df.to_csv(r'P:/mjc-main/cli-mj/analysis_files/bd_calling.csv')

# the playground for calling
# Only analysis up to the calling point

from hand_situation import *
from usefulTiles import *
from drawing_game import *
from optimalDiscard import *
from check_calling import check_calling_tiles

import pandas as pd
from multiprocessing import Pool


def simulate_game(threshold=0, mode='large'):
    tileDeck = deckInit()
    discard = []

# original draw of 16 tiles
    player1_hand, tileDeck = draw(1, 16, tileDeck)
    player1_flowers = []
# Clear the list
    player1_hand.sort()

    handScore, partial, singles = hand_eval(player1_hand, [])

    if mode == 'large':
        if handScore <= threshold:
            return (0), 0
    else:
        if handScore > threshold:
            return (0), 0

    while True:
    # Print tiles remaining in the sea
    # print (f'Tiles remaining at the sea: {len(tileDeck)}')
    # Draw tiles for player 1
        if len(tileDeck) == 0:
            return (handScore, 128, [])
        

        player1_hand, player1_flowers, tileDeck = playerdraw(player1_hand, player1_flowers, tileDeck)

    # print (f'Current hand: {player1_hand}')
    # # print (f'Flowers obtained: {player1_flowers}')
    
        
    # print (f'Hand score: {handScore}')

    # print(countUsefulTiles(partial, singles, discard))
        bestDiscard = findOptimalDiscard(player1_hand, (discard+player1_hand), full_eval_mode=True)

    # Ask discard tile
    # dcTile = askdiscard(player1_hand)
        discard.append(bestDiscard)
        player1_hand.remove(int(bestDiscard))

    # callers
    # see if we can win on the next go (potentially)
        callers = check_calling_tiles(inner_hand=player1_hand, outer_hand=[])
        if len(callers.keys()):
            # WE HAVE WINNING TILES
            tilesUsed = 120 - len(tileDeck)
            return (handScore, tilesUsed, list(callers.keys()))

if __name__ == '__main__':
    import time
    
    epochs = 30000
    data = []

    print('multi starting~')    
    data = [0] * epochs
    start = time.time()
    
    poo = Pool(processes=4)
    results = poo.map(simulate_game, data)

    end2 = time.time()
    delta2 = end2-start

    print(f'Multi mode finished in {delta2}s')


    # end = time.time()
    # delta = end-start
    # print(f'done simulation in {delta}s')

    df = pd.DataFrame(results)

    df.to_csv(r'P:/mjc-main/cli-mj/analysis_files/calling/gameplay_calling_mk3-lib2.csv')

    print ('results added to csv file')

from drawing_game import *
from liguStrats import *
from hand_situation import *
sys.path.append('P:/mjc-main/mjcpy')
from ligu_check import ligu_hand_validity_check # type: ignore  
from listUtils import find_occurence # type: ignore
import pandas as pd
import time
from multiprocessing import Pool

def ligu_loop(callingMode=False) -> int:
    tileDeck = deckInit()
    discard = []

    # original draw of 16 tiles (NO FLOWERS!!)
    player1_hand, tileDeck = draw(1, 16, tileDeck)
    player1_flowers = []

    init_pairs = find_occurence(player1_hand, 2)
    init_trips = find_occurence(player1_hand, 3)
    init_quads = find_occurence(player1_hand, 4)
    init_pc = len(init_pairs) + len(init_trips) + 2*len(init_quads)

    init_score = hand_eval(player1_hand)[0]


    while True:
        if (len(tileDeck) == 0):
            return
        player1_hand.sort()
        # Draw tiles for player 1
        player1_hand, player1_flowers, tileDeck = playerdraw(player1_hand, player1_flowers, tileDeck)

        if not callingMode:
            # Run the hand winning evaluation and only returns at a winning hand
            if ligu_hand_validity_check(player1_hand[:-1], [], player1_hand[-1:]):
                return init_pc, init_score, int(120-len(tileDeck))
  
            
            
        optimalDiscard = findOptimalDiscardLigu(player1_hand, (discard+player1_hand))
        
        # Ask discard tile
        player1_hand.remove(optimalDiscard)
        discard.append(optimalDiscard)

        # Check if calling
        if callingMode:
            pairs = find_occurence(player1_hand, 2)
            quads = find_occurence(player1_hand, 4)
            trips = find_occurence(player1_hand, 3)
            hScore = len(pairs) + 2 * len(quads) + 1.5 * len(trips)

            if hScore >= 7.5:
                # Calling!
                player1_hand.sort()
                return init_pc, init_score, int(120-len(tileDeck))
            

if __name__ == '__main__':
    epochs = 20000
    output_db = [True] * epochs
    # Metrics
    start = time.time()
    
    # Using multiprocess pool for large dataset
    poo = Pool(processes=4)
    results_db = poo.imap_unordered(ligu_loop, output_db)    

    # Loop completed, turn output list into df
    output_df = pd.DataFrame(results_db, columns=['initPairs', 'initScore', 'tilesUsed'])

    # Process end
    end = time.time()

    delta = end-start
    
    output_df.to_csv(r'P:/mjc-main/cli-mj/analysis_files/pc_LData.csv')

    print(f'Loop completed with {epochs} epochs in {round(delta, 2)}s ({round(delta/epochs * 1000, 2)}ms per epoch)')

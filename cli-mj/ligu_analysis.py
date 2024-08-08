from drawing_game import *
from liguStrats import *
from hand_situation import *
sys.path.append('P:/mjc-main/mjcpy')
from ligu_check import ligu_hand_validity_check # type: ignore  
from listUtils import find_occurence # type: ignore
import pandas as pd

def ligu_loop() -> int:
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
        # Draw tiles for player 1
        player1_hand, player1_flowers, tileDeck = playerdraw(player1_hand, player1_flowers, tileDeck)

        if ligu_hand_validity_check(player1_hand[:-1], [], player1_hand[-1:]):
            return init_pc, init_score, int(120-len(tileDeck))
  
            
            
        optimalDiscard = findOptimalDiscardLigu(player1_hand, (discard+player1_hand))

        # Ask discard tile
        player1_hand.remove(optimalDiscard)
        discard.append(optimalDiscard)

if __name__ == '__main__':
    epochs = 20000
    output_db = []
    for i in range(epochs):
        # Passing the output of the loop function into the output list
        output_db.append(ligu_loop())

    # Loop completed, turn output list into df
    output_df = pd.DataFrame(output_db, columns=['initPairs', 'initScore', 'tilesUsed'])

    output_df.to_csv('./analysis_files/pc_LData.csv')
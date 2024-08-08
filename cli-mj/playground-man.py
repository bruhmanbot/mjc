# the playground for testing

from hand_situation import *
from usefulTiles import *
from drawing_game import *
from optimalDiscard import *

import pandas as pd


def simulate_game(threshold=0, mode='large'):
    tileDeck = deckInit()
    discard = []

# original draw of 16 tiles
    player1_hand, tileDeck = draw(1, 16, tileDeck)
    player1_flowers = []
# Clear the list
    player1_hand.sort()

    handScore, partial, singles = hand_eval(player1_hand)

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
            return (handScore, 120), 1
        

        player1_hand, player1_flowers, tileDeck = playerdraw(player1_hand, player1_flowers, tileDeck)

        print (f'Current hand: {player1_hand}')
    # # print (f'Flowers obtained: {player1_flowers}')


    # Run validity check to see if winners?
        validityRes = hand_validity_check(player1_hand[:-1], [], player1_hand[-1:]) # type: ignore

        if validityRes[0] == 1:
            # print ('we did it!' + f' with {120 - len(tileDeck)} tiles')
            # print (validityRes)
            return (handScore, 120-len(tileDeck))

    # print (f'Hand score: {handScore}')

    # print(countUsefulTiles(partial, singles, discard))
        bestDiscard = findOptimalDiscard(player1_hand, (discard+player1_hand))
        print(bestDiscard)
        # Ask discard tile
        dcTile = askdiscard(player1_hand)
        discard.append(dcTile)
        player1_hand.remove(int(dcTile))

        player1_hand.sort()


if __name__ == '__main__':
    epochs = 10000
    data = []
    i = 0
    while i < epochs:
        game = simulate_game()
        if game[1]:
            data.append(game[0])
            i = i + 1
        else:
            continue


    print ('done simulation')

    df = pd.DataFrame(data)

    df.to_csv('./cli-mj/gameplay.csv')

    print ('results added to csv file')

import pandas as pd
from drawing_game import *
from hand_situation import * 
from matplotlib import pyplot as plt

epochs = 100000
openingScoreTable = [];
counter = 0
old_underest = 0
for i in range(epochs):
    tileDeck = deckInit()
    # original draw of 16 tiles
    player1_hand, tileDeck = draw(1, 16, tileDeck)
    result_hand = filter(lambda x: x > 10, player1_hand)
    result_flowers = filter(lambda x: x < 10, player1_hand)

    player1_hand = list(result_hand)
    player1_flowers = list(result_flowers)

    # Flowers
    while len(player1_hand) != 16:
        player1_drawnTiles, tileDeck = draw(-1, 16-len(player1_hand), tileDeck)
        player1_hand = player1_hand + list(filter(lambda x: x>10, player1_drawnTiles))
        player1_flowers = player1_flowers + list(filter(lambda x: x<10, player1_drawnTiles))
    # Repeatedly gets flowers until main hand == 16 tiles
    # Clear the list
    player1_drawnTiles = []
    player1_hand.sort()

    openingScore = hand_eval(player1_hand, [])
    openingScore2 = hand_eval_adv(player1_hand, [])
    if openingScore[0] != openingScore2[0]:
        counter += 1
    if openingScore[0] < openingScore2[0]:
        old_underest += openingScore2[0] - openingScore[0]

print(f'times diff: {counter}')
print(f'avg underest: {old_underest/counter}')

# openingScoreTable.sort()
# openingScoreSet = set(openingScoreTable)

# openingScoreDist = {}

# for i in openingScoreSet:
#     openingScoreDist[i] = openingScoreTable.count(i)

# print (openingScoreDist)

# data_df = pd.DataFrame.from_dict(openingScoreDist, orient='index')
# data_df.sort_index(axis=0, ascending=True, inplace=False, kind='quicksort')

# data_df.to_csv('opening.csv')

# x = data_df.index
# y = data_df[0]

# fig = plt.figure(figsize=(5,4))
# plt.grid(visible=True)

# plt.hist(x,y)

# plt.show()




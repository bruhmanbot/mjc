import sys
sys.path.append('../mjcpy')
import random

from validityCheck import * # type: ignore

def deckInit(flowers=False):
    # Create a deck of the 144 tiles
    deck = []

    for i in range(38):
        if i % 10 == 0:
            continue
        deck.append(10+i)
    # Multiply by 4 (4 tiles each)
    deck = deck * 4

    # # Add the flowers
    if flowers:
        flower = [(i+1) for i in range(8)]
        # + flower
        deck = deck + flower

    # shuffle
    random.shuffle(deck)

    return deck

def draw(pos:int , amount: int, deck: list):
    # tile drawing function
    # removes 1st-xth (or last few) elements from the deck and outputs them in an array
    # use negative number in pos to signify drawing from the end
    if pos > 0:
        # Takes from the beginning
        tilesDrawn = deck[:amount]
        out_deck = deck[amount:]
        return tilesDrawn, out_deck
    else:
        tilesDrawn = deck[-1*amount:]
        out_deck = deck[:-amount]
        return tilesDrawn, out_deck
    
def gamedraw(deck:list) -> list[list]:
    # Main function to draw 1 tile until non flower tile is obtained
    tile, out_deck = draw(1, 1, deck)
    flowers = []
    while tile[0] < 10:
        # runs if tile is a flower
        flowers.append(tile[0])
        tile.pop()
        tile, out_deck = draw(-1, 1, out_deck)

        try:
            tile[0]
        except IndexError:
            # No more tiles
            return ['DRAW'], [], []

    # breaks when obtains non flower tile
    return tile, flowers, out_deck

def playerdraw(dest_hand: list, dest_flowers:list, deck:list) -> None:
    # player drawing

    newTile, newFlowers, out_deck = gamedraw(deck)

    out_hand = dest_hand + newTile 
    # new tiles are placed to RHS
    out_flowers = dest_flowers + newFlowers

    out_flowers.sort()
    return out_hand, out_flowers, out_deck

def askdiscard(playerHand: list) -> int:
    m = input('Discard tile?')

    while True:
        try:
            int(m)
        except NameError or ValueError:
            m = input('again?')
            continue
        # Breaks when m is valid

        if int(m) in playerHand:
            return int(m)
        else:
            m = input('again?')      


def mainloop():
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

    while True:
        # Print tiles remaining in the sea
        print (f'Tiles remaining at the sea: {len(tileDeck)}')
        # Draw tiles for player 1
        player1_hand, player1_flowers, tileDeck = playerdraw(player1_hand, player1_flowers, tileDeck)

        print (f'Current hand: {player1_hand}')
        print (f'Flowers obtained: {player1_flowers}')

        # Run validity check to see if winners?
        validityRes = hand_validity_check(player1_hand[:-1], [], player1_hand[-1:]) # type: ignore

        if validityRes[0] == 1:
            print ('we did it!')
            print (validityRes)
            break
        else:
            print('we are getting there')

        # Ask discard tile
        dcTile = askdiscard(player1_hand)

        player1_hand.remove(int(dcTile))

        player1_hand.sort()

        print('----------------------------------------------------')

if __name__ == '__main__':
    mainloop()
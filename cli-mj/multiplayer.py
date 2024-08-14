from drawing_game import deckInit, askdiscard
from player_class import gambler
import random

def update_public_domain(*gamers: gambler) -> list:
    global discards
    new_domain = discards # + other outer hands

    for g in gamers:
        try:
            g.playerID == 'TEST'
        except AttributeError:
            print ('ERROR @ UPDATE PUBLIC DOMAIN: NOT ALL ARGUMENTS PASSED TO FUNCTION ARE GAMBLERS')
            return
        new_domain = new_domain + g.outer_hand

    return new_domain

def nextplayerindex(current_index:int):
    if current_index == 3:
        return 0
    else:
        return (current_index + 1)


if __name__ == '__main__':
    # gamers
    gamers = [0 ,0, 0, 0]
    gamers[0] = gambler('me', 1)
    gamers[1] = gambler('ai_1', 0)
    gamers[2] = gambler('ai_2', 0)
    gamers[3] = gambler('ai_3', 0)

    # init deck and give everyone tiles in order
    tileDeck = deckInit(flowers=False)
    for g in gamers:
        g.init_draw(tileDeck)
        g.evalhand()
        
    # main body loop of play
    activePlayer:int = 0 # index of the current active player, starting off with 0
    humanIndex: int = 0
    gameDiscards = []
    # public domain should be continuously updated
    publicDomain = []

    # First draw for the dealer has to be handled seperately
    if activePlayer == humanIndex:
        gamers[activePlayer].draw(tileDeck)
        print(gamers[activePlayer])
        playerDiscard:int = askdiscard(gamers[activePlayer].inner_hand)
        gamers[activePlayer].disc(playerDiscard, gameDiscards, publicDomain)
    else:
        # CPU Startng
        gamers[activePlayer].playturn()


    while True:
        lastTile = gameDiscards[-1]
        # Evaluating if anyone wins
        winnerPresent = False
        for g in gamers:
            # that gamer was calling on that tile
            if lastTile in g.calling:
                print(f'{g.playerID} has won on {lastTile} discarded by {gamers[activePlayer].playerID}; with hand:')
                print(f'{g.inner_hand} || {g.outer_hand} || < {lastTile} >')
                winnerPresent = True
        if winnerPresent:
            # More than one winner can win at the same time
            break

        if len(tileDeck) == 0:
            print('Game ended in draw')
            break

        # Evaluate for pongs
        pongPlayerIndex = -1 # later will be changed to positive integer if someone pongs
        for g_index, g in enumerate(gamers):
            # Only 1 person can pong at the same time so i can break prematurely here
            if g.playerID == 'me':
                # human evaluation
                if g.inner_hand.count(lastTile) >= 2:
                    pongPlayerIndex = g_index # == humanIndex
                    break
            else:
                gamerPong: list = g.determine_pong(gameDiscards, publicDomain)
                if len(gamerPong):
                    pongPlayerIndex = g_index
                    break
        
        if (pongPlayerIndex != -1) and (pongPlayerIndex != nextplayerindex(activePlayer)) :
            # indicating a change -- Someone (other than the next player) has ponggered
            # Reason we have to leave the next player is because of ups --> generally would want to up given the choice
            if pongPlayerIndex == humanIndex:
                print(f"You can pong on {lastTile} discarded by {gamers[activePlayer].playerID}." + 
                    "\nDo you want to do so? (input smth if u want, and nothing if you dont)")
                playerFreeChoice = input()
                if bool(playerFreeChoice):
                    activePlayer = pongPlayerIndex # == human index
                    # This will get player to pong and discard a tile
                    pairPong = [lastTile, lastTile]
                    gamers[pongPlayerIndex].pong(pairPong, gameDiscards, publicDomain)
                    continue
                else:
                    # Continue the lower part
                    pass
            else:
                
                # This will get player to pong and discard a tile
                pairPong = [lastTile, lastTile]
                gamers[pongPlayerIndex].pong(pairPong, gameDiscards, publicDomain)
                print(f'{gamers[pongPlayerIndex].playerID} PONGED {lastTile} discarded by {gamers[activePlayer].playerID}')
                print(f'{gamers[pongPlayerIndex].playerID} discarded {gameDiscards[-1]}')

                activePlayer = pongPlayerIndex 

                continue
            
        # If no one pongs/wins --> cycle the player
        activePlayer = nextplayerindex(activePlayer)
        # Evaluate for UPS
        # Returns the partial set (if applicable) to commit the up with
        nextPlayerUpPS: list = list(gamers[activePlayer].determine_up(gameDiscards, publicDomain))
        nextPlayerPONG: list = list(gamers[activePlayer].determine_pong(gameDiscards, publicDomain))
        if len(nextPlayerUpPS):
            if activePlayer != humanIndex:
                # The up function will already ask the user for a discard if applicable
                gamers[activePlayer].up(nextPlayerUpPS, gameDiscards, publicDomain)
                print(f'{gamers[activePlayer].playerID} UPPED {lastTile} discarded by {gamers[activePlayer-1].playerID}')
                print(f'{gamers[activePlayer].playerID} displayed tiles: {gamers[activePlayer].outer_hand}')
                print(f'{gamers[activePlayer].playerID} discarded {gameDiscards[-1]}')
                continue

            if len(nextPlayerPONG):
                print(f'You can UP + PONG on {lastTile} discarded by {gamers[activePlayer-1].playerID}'
                    + '\n Do you want to do so? (input p for PONG, u for UP, and nothing if you dont)')
                playerFreeChoice = input()
                if bool(playerFreeChoice):
                    if playerFreeChoice == 'p':
                        gamers[activePlayer].pong(nextPlayerPONG, gameDiscards, publicDomain)
                    else:
                        gamers[activePlayer].up(nextPlayerUpPS, gameDiscards, publicDomain)
                else:
                    pass
            else:
                print(f'You can UP on {lastTile} discarded by {gamers[activePlayer-1].playerID}'
                    + '\n Do you want to do so? (input smth if u want, and nothing if you dont)')
                
                playerFreeChoice = input()
                if bool(playerFreeChoice):
                    gamers[activePlayer].up(nextPlayerUpPS, gameDiscards, publicDomain)
                    continue
                
        elif len(nextPlayerPONG):
            if nextplayerindex(activePlayer) != humanIndex:
                # The up function will already ask the user for a discard if applicable
                gamers[activePlayer].pong(nextPlayerPONG, gameDiscards, publicDomain)
                print(f'{gamers[activePlayer].playerID} PONGED {lastTile} discarded by {gamers[activePlayer-1].playerID}')
                print(f'{gamers[activePlayer].playerID} displayed tiles: {gamers[activePlayer].outer_hand}')
                print(f'{gamers[activePlayer].playerID} discarded {gameDiscards[-1]}')
                continue

            print(f"You can pong on {lastTile} discarded by {gamers[activePlayer].playerID}." + 
                "\nDo you want to do so? (input smth if u want, and nothing if you dont)")
            playerFreeChoice = input()
            if bool(playerFreeChoice):
                # This will get player to pong and discard a tile
                pairPong = [lastTile, lastTile]
                gamers[activePlayer].pong(pairPong, gameDiscards, publicDomain)
                continue
            else:
                # Continue the lower part
                pass


            ...
            # Need extra code here to tell players exactly how they can UP
                
            
        # Normal drawing
        if activePlayer == humanIndex:
            gamers[humanIndex].draw(tileDeck)
            print(gamers[humanIndex])
            playerDiscard:int = askdiscard(gamers[humanIndex].inner_hand)
            gamers[humanIndex].disc(playerDiscard, gameDiscards, publicDomain)
            # update calling list
            gamers[humanIndex].evalhand()
        else:
            gamers[activePlayer].playturn(tileDeck, gameDiscards, publicDomain)
            print(f'{gamers[activePlayer].playerID} discarded {gameDiscards[-1]}')

        # loop ends here!



        

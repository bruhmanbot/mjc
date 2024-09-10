from drawing_game import deckInit, askdiscard
from player_class import gambler

import pandas as pd
from multiprocessing import Pool

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

def spgame_loop(first_player:int=0, printf=True, **kwargs):
    # gamers
    gamers = [0 ,0, 0, 0]
    gamers[0] = gambler('ai_0')
    gamers[1] = gambler('ai_1', {'skill': 'dynamic'})
    gamers[2] = gambler('ai_2')
    gamers[3] = gambler('ai_3')

    # Background CDF
    try:
        gammaLUT = kwargs['CDF_gamma']
    except KeyError:
        gamma_dist_LUT = pd.read_csv('./script_data/gamma-dist.csv')
        gammaLUT = list(gamma_dist_LUT['CDF']) # Load the LUT manually

    # init deck and give everyone tiles in order
    tileDeck = deckInit(flowers=True)
    for g in gamers:
        g.init_draw(tileDeck)
        g.evalhand(tileDeck)
        g.determine_goal()
        
    # main body loop of play
    activePlayer:int = first_player % 4 # index of the current active player, starting off with 0
    gameDiscards = []
    # public domain should be continuously updated
    publicDomain = []

    # First draw for the dealer has to be handled seperately
    # CPU Startng
    gamers[activePlayer].playturn(tileDeck, gameDiscards, publicDomain, CDF_gamma=gammaLUT)


    while True:
        try:
            lastTile = gameDiscards[-1]
        except IndexError:
            return [0] * 6
        # Evaluating if anyone wins
        winners: list[tuple] = []
        for g in gamers:
            # that gamer was calling on that tile
            if lastTile in g.calling:
                # print(f'{g.playerID} has won on {lastTile} discarded by {gamers[activePlayer].playerID}; with hand:')
                # print(f'{g.inner_hand} || {g.outer_hand} || < {lastTile} >')
                # Run the score count with the last tile
                gResult: list = g.score_count(lastTile)[:2]
                gResult = tuple([g.playerID] + [gamers[activePlayer].playerID] + [80-len(tileDeck)] + gResult + 
                                [f'{g.inner_hand} || {g.outer_hand} || < {lastTile} >'])
                winners.append(gResult)

        # Breaks the whole loop (and function if someone wins) // draw        
        if len(winners):
            # More than one winner can win at the same time
            return winners

        if len(tileDeck) == 0:
            # print('Game ended in draw')
            return [tuple(['draw'] * 6)]

        # Evaluate for pongs
        pongPlayerIndex = -1 # later will be changed to positive integer if someone pongs
        for g_index, g in enumerate(gamers):
            # Only 1 person can pong at the same time so i can break prematurely here
            gamerPong: list = g.determine_pong(gameDiscards, publicDomain)
            if len(gamerPong):
                pongPlayerIndex = g_index
                break
        
        if (pongPlayerIndex != -1) and (pongPlayerIndex != nextplayerindex(activePlayer)) :
            # indicating a change -- Someone (other than the next player) has ponggered
            # Reason we have to leave the next player is because of ups --> generally would want to up given the choice
            # This will get player to pong and discard a tile
            pairPong = [lastTile, lastTile]
            gamers[pongPlayerIndex].pong(pairPong, gameDiscards, publicDomain, deck=tileDeck, CDF_gamma=gammaLUT)
            if printf:
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
            gamers[activePlayer].up(nextPlayerUpPS, gameDiscards, publicDomain, CDF_gamma=gammaLUT)
            if printf:
                print(f'{gamers[activePlayer].playerID} UPPED {lastTile} discarded by {gamers[activePlayer-1].playerID}')
                print(f'{gamers[activePlayer].playerID} displayed tiles: {gamers[activePlayer].outer_hand}')
                print(f'{gamers[activePlayer].playerID} discarded {gameDiscards[-1]}')
            continue
                
        elif len(nextPlayerPONG):
            gamers[activePlayer].pong(nextPlayerPONG, gameDiscards, publicDomain, deck=tileDeck, CDF_gamma=gammaLUT)
            if printf:
                print(f'{gamers[activePlayer].playerID} PONGED {lastTile} discarded by {gamers[activePlayer-1].playerID}')
                print(f'{gamers[activePlayer].playerID} displayed tiles: {gamers[activePlayer].outer_hand}')
                print(f'{gamers[activePlayer].playerID} discarded {gameDiscards[-1]}')
            continue


            
        # Normal drawing

        potentialTile = tileDeck[0]
        winDialog: list = gamers[activePlayer].playturn(tileDeck, gameDiscards, publicDomain, CDF_gamma=gammaLUT)
        if len(winDialog):
            # print(f'{w} from {gamers[activePlayer].playerID}')
            # print(f'{gamers[activePlayer].inner_hand[:-1]} || {gamers[activePlayer].outer_hand} || < {gamers[activePlayer].inner_hand[-1]} >')
            # Standardise the output
            tsumoOutput: tuple = tuple([gamers[activePlayer].playerID, gamers[activePlayer].playerID, 80-len(tileDeck)] + winDialog[:2] + 
                                        [f'{gamers[activePlayer].inner_hand} || {gamers[activePlayer].outer_hand} || < {potentialTile} >'])
            return [tsumoOutput]
        if printf:
            print(f'{gamers[activePlayer].playerID} discarded {gameDiscards[-1]}')


        # loop ends here!

    # print (f'{len(tileDeck)} tiles left in the mountain')


if __name__ == '__main__':
    # import ast
    # with open('winDict.txt') as db:
    #     winnerDict_str = db.read()
    
    # winnerDict: dict = ast.literal_eval(winnerDict_str)
    multiCore = True

    gamma_dist_LUT = pd.read_csv('./script_data/gamma-dist.csv')
    CDF = list(gamma_dist_LUT['CDF'])

    if multiCore:
        games = 6000
        gd_args = [(i, False) for i in range(games)]

        poo = Pool(processes=4)

        print('Multi Processing started ~~')
        gdData = poo.starmap(spgame_loop, gd_args)

        gdData_fixed = []
        for row in gdData:
            for subtuple in row:
                gdData_fixed.append(subtuple)

        gd_df = pd.DataFrame(gdData_fixed, columns=['Winner', 'From', 'TilesUsed', 'Score', 'Accolades', 'Hand'])

        print(gd_df.describe())
        gd_df.to_csv('./analysis_files/dynamicMode-STEP2.csv')
    
    else:
    # Single core
        for q in range(400):

            winners_diag: tuple = spgame_loop(q, printf=False, CDF_gamma=CDF)

            print (winners_diag)        
            

    # rewrite = open('winDict.txt', "w")

    # rewrite.write(str(winnerDict))

    # rewrite.close()
    

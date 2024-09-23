from drawing_game import deckInit, askdiscard
from player_class import gambler

import pandas as pd
from multiprocessing import Pool


def update_public_domain(*gamers: gambler) -> list:
    global discards
    new_domain = discards  # + other outer hands

    for g in gamers:
        try:
            g.playerID == 'TEST'
        except AttributeError:
            print('ERROR @ UPDATE PUBLIC DOMAIN: NOT ALL ARGUMENTS PASSED TO FUNCTION ARE GAMBLERS')
            return []
        new_domain = new_domain + g.outer_hand

    return new_domain


def loadCDF() -> tuple:
    gamma_dist_LUT = pd.read_csv('./script_data/gamma-dist.csv')
    CDF = tuple(gamma_dist_LUT['CDF'])

    return CDF


def nextplayerindex(current_index: int):
    if current_index == 3:
        return 0
    else:
        return current_index + 1


def spgame_loop(first_player: int = 0, printf=True, CDF_gamma=loadCDF()):
    # gamers
    gamers: list[gambler] = [0, 0, 0, 0]  # Temporaily prime a list of len 4.
    gamers[0] = gambler('ai_0')
    # Set player profile to be dynamic for ai_1
    gamers[1] = gambler('ai_1', player_profile={"skill": "dynamic", "weights": (1, -0.28)})
    gamers[2] = gambler('ai_2')
    gamers[3] = gambler('ai_3')

    # init deck and give everyone tiles in order
    tileDeck = deckInit(flowers=True)
    for g in gamers:
        g.init_draw(tileDeck)
        g.evalhand()
        g.determine_goal()

    # main body loop of play
    activePlayer: int = first_player % 4  # index of the current active player, starting off with 0
    humanIndex: int = -1
    gameDiscards = [0]
    # public domain should be continuously updated
    publicDomain = []

    # First draw for the dealer has to be handled seperately
    if activePlayer == humanIndex:
        gamers[activePlayer].draw(tileDeck)
        print(gamers[activePlayer])
        playerDiscard: int = askdiscard(gamers[activePlayer].inner_hand)
        gamers[activePlayer].disc(playerDiscard, gameDiscards, publicDomain)
    else:
        # CPU Starting
        gamers[activePlayer].playturn(tileDeck, gameDiscards, publicDomain, CDF_gamma=CDF_gamma)

    while True:
        lastTile = gameDiscards[-1]
        # Evaluating if anyone wins
        winners: list = []
        for g in gamers:
            # that gamer was calling on that tile
            if lastTile in g.calling:
                # print(f'{g.playerID} has won on {lastTile} discarded by {gamers[activePlayer].playerID}; with hand:')
                # print(f'{g.inner_hand} || {g.outer_hand} || < {lastTile} >')
                # Run the score count with the last tile
                gResult = g.score_count(lastTile)
                gResult = tuple([g.playerID, gamers[activePlayer].playerID] + [80 - len(tileDeck)] + gResult +
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
        pongPlayerIndex = -1  # later will be changed to positive integer if someone pongs
        for g_index, g in enumerate(gamers):
            # Only 1 person can pong at the same time so i can break prematurely here
            if g.playerID == 'me':
                # human evaluation
                if g.inner_hand.count(lastTile) >= 2:
                    pongPlayerIndex = g_index  # == humanIndex
                    break
            else:
                gamerPong: list = g.determine_pong(gameDiscards, publicDomain)
                if len(gamerPong):
                    pongPlayerIndex = g_index
                    break

        if (pongPlayerIndex != -1) and (pongPlayerIndex != nextplayerindex(activePlayer)):
            # indicating a change -- Someone (other than the next player) has ponggered
            # Reason we have to leave the next player is because of ups --> generally would want to up given the choice
            if pongPlayerIndex == humanIndex:
                print(f"You can pong on {lastTile} discarded by {gamers[activePlayer].playerID}." +
                      "\nDo you want to do so? (input smth if u want, and nothing if you dont)")
                playerFreeChoice = input()
                if bool(playerFreeChoice):
                    activePlayer = pongPlayerIndex  # == human index
                    # This will get player to pong and discard a tile
                    pairPong = [lastTile, lastTile]
                    gamers[pongPlayerIndex].pong(pairPong, gameDiscards, publicDomain, tileDeck, CDF_gamma=CDF_gamma)
                    continue
                else:
                    # Continue the lower part
                    pass
            else:

                # This will get player to pong and discard a tile
                pairPong = [lastTile, lastTile]
                gamers[pongPlayerIndex].pong(pairPong, gameDiscards, publicDomain, tileDeck, CDF_gamma=CDF_gamma)
                if printf:
                    print(
                        f'{gamers[pongPlayerIndex].playerID} PONGED {lastTile} discarded by {gamers[activePlayer].playerID}')
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
                gamers[activePlayer].up(nextPlayerUpPS, gameDiscards, publicDomain, tileDeck, CDF_gamma=CDF_gamma)
                if printf:
                    print(
                        f'{gamers[activePlayer].playerID} UPPED {lastTile} discarded by {gamers[activePlayer - 1].playerID}')
                    print(f'{gamers[activePlayer].playerID} displayed tiles: {gamers[activePlayer].outer_hand}')
                    print(f'{gamers[activePlayer].playerID} discarded {gameDiscards[-1]}')
                continue

            if len(nextPlayerPONG):
                print(f'You can UP + PONG on {lastTile} discarded by {gamers[activePlayer - 1].playerID}'
                      + '\n Do you want to do so? (input p for PONG, u for UP, and nothing if you dont)')
                playerFreeChoice = input()
                if bool(playerFreeChoice):
                    if playerFreeChoice == 'p':
                        gamers[activePlayer].pong(nextPlayerPONG, gameDiscards, publicDomain, tileDeck,
                                                  CDF_gamma=CDF_gamma)
                    else:
                        gamers[activePlayer].up(nextPlayerUpPS, gameDiscards, publicDomain, tileDeck,
                                                CDF_gamma=CDF_gamma)

                    continue
                else:
                    pass
            else:
                print(f'You can UP on {lastTile} discarded by {gamers[activePlayer - 1].playerID}'
                      + '\n Do you want to do so? (input smth if u want, and nothing if you dont)')

                playerFreeChoice = input()
                if bool(playerFreeChoice):
                    gamers[activePlayer].up(nextPlayerUpPS, gameDiscards, publicDomain, tileDeck, CDF_gamma=CDF_gamma)
                    continue

            ...
            # Need extra code here to tell players exactly how they can UP
        elif len(nextPlayerPONG):
            if activePlayer != humanIndex:
                # The up function will already ask the user for a discard if applicable
                gamers[activePlayer].pong(nextPlayerPONG, gameDiscards, publicDomain, tileDeck, CDF_gamma=CDF_gamma)
                if printf:
                    print(
                        f'{gamers[activePlayer].playerID} PONGED {lastTile} discarded by {gamers[activePlayer - 1].playerID}')
                    print(f'{gamers[activePlayer].playerID} displayed tiles: {gamers[activePlayer].outer_hand}')
                    print(f'{gamers[activePlayer].playerID} discarded {gameDiscards[-1]}')
                continue

            # ELSE
            print(f"You can pong on {lastTile} discarded by {gamers[activePlayer - 1].playerID}." +
                  "\nDo you want to do so? (input smth if u want, and nothing if you dont)")
            playerFreeChoice = input()
            if bool(playerFreeChoice):
                # This will get player to pong and discard a tile
                pairPong = [lastTile, lastTile]
                gamers[activePlayer].pong(pairPong, gameDiscards, publicDomain, tileDeck, CDF_gamma=CDF_gamma)
                continue
            else:
                # Continue the lower part
                pass

        # Normal drawing
        if activePlayer == humanIndex:
            potentialTile = tileDeck[0]
            gamers[humanIndex].draw(tileDeck)
            # Check for win by sumo
            if gamers[humanIndex].inner_hand[-1] in gamers[humanIndex].calling:
                print(f'Win by sumo from {gamers[humanIndex].playerID}')
                print(
                    f'{gamers[humanIndex].inner_hand[:-1]} || {gamers[humanIndex].outer_hand} || < {gamers[humanIndex].inner_hand[-1]} >')
                tsumoOutput: tuple = tuple(
                    [gamers[humanIndex].playerID, gamers[humanIndex].playerID, 80 - len(tileDeck)] + ['winners!'] +
                    [f'{gamers[humanIndex].inner_hand[:-1]} || {gamers[humanIndex].outer_hand} || < {potentialTile} >'])
                return [tsumoOutput]

            # Normal discard procedures
            print(gamers[humanIndex])
            playerDiscard: int = askdiscard(gamers[humanIndex].inner_hand)
            gamers[humanIndex].disc(playerDiscard, gameDiscards, publicDomain)

            # update calling list
            gamers[humanIndex].evalhand()
        else:
            potentialTile = tileDeck[0]
            count_fromEnd = 1
            # Handles the exception with the first tile being a flower
            while potentialTile < 10 and count_fromEnd < len(tileDeck):
                potentialTile = tileDeck[-1 * count_fromEnd]
                count_fromEnd = count_fromEnd + 1

            winDialog: list = gamers[activePlayer].playturn(tileDeck, gameDiscards, publicDomain, CDF_gamma=CDF_gamma)
            if len(winDialog):
                # print(f'{w} from {gamers[activePlayer].playerID}')
                # print(f'{gamers[activePlayer].inner_hand[:-1]} || {gamers[activePlayer].outer_hand} || < {gamers[activePlayer].inner_hand[-1]} >')
                # Standardise the output
                tsumoOutput: tuple = tuple(
                    [gamers[activePlayer].playerID, gamers[activePlayer].playerID, 80 - len(tileDeck)] + winDialog +
                    [f'{gamers[activePlayer].inner_hand} || {gamers[activePlayer].outer_hand} || < {potentialTile} >'])
                return [tsumoOutput]
            if printf:
                print(f'{gamers[activePlayer].playerID} discarded {gameDiscards[-1]}')

        # loop ends here!

    # print (f'{len(tileDeck)} tiles left in the mountain')


def game_end(gd_tuple: tuple) -> list[str]:
    ## Displays how the game ended, either by tsumo or by discard
    # Format for our output list, will be overwritten by the actual values later
    outputList = ['tsumo/discard', 'winner_num_in_str', 'loser_num_in_str']

    if gd_tuple[0] == gd_tuple[1]:
        # gd_tuple[0][-1:] is the number of the player
        outputList = ['tsumo', gd_tuple[0], gd_tuple[0]]
        return outputList

    # Else (Discard wins)
    outputList = ['discard', gd_tuple[0], gd_tuple[1]]
    return outputList


def compileStats(Wins: dict, DiscardLosses: dict, Tsumos: dict) -> dict[str, tuple]:
    allPlayerStats = {}

    for player in Wins.keys():
        totalWins = Wins[player] + Tsumos[player] * 3
        totalLosses = DiscardLosses[player]
        for q in Tsumos:
            # Skip the tsumos made by the player or draws
            if q == player or q == 'draw':
                continue

            totalLosses += Tsumos[q]

        # Player stats: Wins, losses, W/L Ratio
        try:
            playerStats: tuple = (totalWins, totalLosses, totalWins / totalLosses)
        except ZeroDivisionError:
            playerStats: tuple = (totalWins, totalLosses, totalWins)

        allPlayerStats[player] = playerStats

    # Sort our output dictionary and output it (Aesthetics!)    
    playerList: list[str] = list(allPlayerStats.keys())
    playerList.sort()

    outputPlayerStats = {}
    for player in playerList:
        outputPlayerStats[player] = allPlayerStats[player]

    return outputPlayerStats


if __name__ == '__main__':
    import time


    # winnerDict: dict = ast.literal_eval(winnerDict_str)
    games = 6000
    CDF = loadCDF()
    gd_args = [(i, False, CDF) for i in range(games)]
    outputToTerminal = True

    poo = Pool(processes=6)

    start = time.time()
    print('Multi Processing started ~~')
    gdData = poo.starmap(spgame_loop, gd_args)

    gdData_fixed = []
    for row in gdData:
        for subtuple in row:
            gdData_fixed.append(subtuple)

    if outputToTerminal:
        # Terminal output we try to get the W/L Ratio for all AIs
        # Calculate the amount of wins and losses and sumos
        playerWins = {}  # Logs the amount of times a player has won BY A DISCARD FROM OTHERS
        playerLosses = {}  # Logs player losses by discarding to others
        playerTsumos = {}  # Logs the amount of times a player has won by tsumo-ing
        for win in gdData_fixed:
            summary: list[str] = game_end(win)

            if summary[0] == 'tsumo':
                try:
                    playerTsumos[summary[1]] = playerTsumos[summary[1]] + 1
                except KeyError:
                    playerTsumos[summary[1]] = 1

                continue

            # Discard wins
            # Credit the winner
            try:
                playerWins[summary[1]] = playerWins[summary[1]] + 1
            except KeyError:
                playerWins[summary[1]] = 1

            # Log the loss for the loser
            try:
                playerLosses[summary[2]] = playerLosses[summary[2]] + 1
            except KeyError:
                playerLosses[summary[2]] = 1

        # Return the output        
        compiled = compileStats(playerWins, playerLosses, playerTsumos)
        print('Stats:')
        for playerID in compiled:
            print(f'{playerID}: {compiled[playerID]}')

        print('\n-----\n')
        print(f'Wins: {playerWins} \nLosses: {playerLosses}\nTsumos: {playerTsumos}')
        print(f'Prg executed sucessfully; Time used: {round(time.time() - start, 2)}s')
        quit()

    # Pandas-csv output
    df_col = ['Win', 'From', 'TilesUsed', 'Score', 'Accolades', 'Hand']
    gd_df = pd.DataFrame(gdData_fixed, columns=df_col)

    print(gd_df.describe())
    print(f'time taken: {time.time() - start}')

    gd_df.to_csv(r'C:/Users/Asus/Documents/coding projects/mj-tw-analysis/analysis_files/analysis_files_lib12/dyn1.csv')
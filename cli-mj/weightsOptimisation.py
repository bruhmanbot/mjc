"""A script to scan through different weights
to see which value would net the best W/L Ratio"""

from player_class import gambler
from multiplayer import compileStats
from multiplayer import loadCDF, nextplayerindex
from drawing_game import deckInit
from multiprocessing import Pool


# DONE: refactor sp_gameloop code to take in extra weight argument
# Modified version of sp_game_loop
def spgame_loop_opt(first_player: int = 0, losingWeight: float = -1.0, CDF_gamma: list | tuple = loadCDF()):
    # gamers
    gamers: list[gambler] = [0, 0, 0, 0]  # Temporaily prime a list of len 4.
    gamers[0] = gambler('ai_0')
    # Set player profile to be dynamic for ai_1
    gamers[1] = gambler('ai_1',
                        player_profile={
                            "skill": "dynamic",
                            "weights": (1, losingWeight)}
                        )
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
    gameDiscards = [0]
    # public domain should be continuously updated
    publicDomain = []

    # First draw for the dealer has to be handled seperately
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
            # Only 1 person can pong at the same time, so I can break prematurely here
            gamerPong: list = g.determine_pong(gameDiscards, publicDomain)
            if len(gamerPong):
                pongPlayerIndex = g_index
                break

        if (pongPlayerIndex != -1) and (pongPlayerIndex != nextplayerindex(activePlayer)):
            # indicating a change -- Someone (other than the next player) has ponged
            # Reason we have to leave the next player is because of ups --> generally would want to up given the choice
            # This will get player to pong and discard a tile
            pairPong = [lastTile, lastTile]
            gamers[pongPlayerIndex].pong(pairPong, gameDiscards, publicDomain, tileDeck, CDF_gamma=CDF_gamma)
            activePlayer = pongPlayerIndex

            continue

        # If no one pongs/wins --> cycle the player
        activePlayer = nextplayerindex(activePlayer)
        # Evaluate for UPS
        # Returns the partial set (if applicable) to commit the up with
        nextPlayerUpPS: list = list(gamers[activePlayer].determine_up(gameDiscards, publicDomain))
        nextPlayerPONG: list = list(gamers[activePlayer].determine_pong(gameDiscards, publicDomain))
        if len(nextPlayerUpPS):
            # The up function will already ask the user for a discard if applicable
            gamers[activePlayer].up(nextPlayerUpPS, gameDiscards, publicDomain, tileDeck, CDF_gamma=CDF_gamma)
            continue

        elif len(nextPlayerPONG):
            # The up function will already ask the user for a discard if applicable
            gamers[activePlayer].pong(nextPlayerPONG, gameDiscards, publicDomain, tileDeck, CDF_gamma=CDF_gamma)
            continue

        # Normal drawing
        potentialTile = tileDeck[0]
        count_fromEnd = 1
        # Handles the exception with the first tile being a flower
        while potentialTile < 10 and count_fromEnd < len(tileDeck):
            potentialTile = tileDeck[-1 * count_fromEnd]
            count_fromEnd = count_fromEnd + 1

        winDialog: list = gamers[activePlayer].playturn(tileDeck, gameDiscards, publicDomain, CDF_gamma=CDF_gamma)
        if len(winDialog):
            # Standardise the output
            tsumoOutput: tuple = tuple(
                [gamers[activePlayer].playerID, gamers[activePlayer].playerID, 80 - len(tileDeck)] + winDialog +
                [f'{gamers[activePlayer].inner_hand} || {gamers[activePlayer].outer_hand} || < {potentialTile} >'])
            return [tsumoOutput]
        # loop ends here!


# DONE: Ancillary functions to get the dictionaries after simulation is complete
def extractGames(resultList: list[list[tuple[str]]], playerList: list[str]) \
        -> tuple[dict[str, int], dict[str, int], dict[str, int]]:
    # The dictionary that contains the amount of times a player has won
    playerWins = {}
    for player in playerList:
        # Get these as the keys of our dictionary
        playerWins[player] = 0

    # Dictionary for direct losses for each player (loss by discarding the winning tile to others)
    playerDirectLosses = playerWins.copy()
    # Dictionary for tsumos
    playerTsumos = playerWins.copy()

    unpackedResults: list[tuple] = []
    for gameResultContainer in resultList:
        # Unwrap the containers to give a list of tuples
        # The gameResult tuple is wrapped in a list
        # gameResultContainer = [(gameResult), (gameResult) ...] in case if more than 1 winner in a round
        for result in gameResultContainer:
            unpackedResults.append(result)

    # We need to loop over each gameResult
    for gameResult in unpackedResults:
        if gameResult[0] == 'draw':
            continue

        if gameResult[0] == gameResult[1]:
            # Tsumo
            playerTsumos[gameResult[0]] += 1
        else:
            # Discard win - Add win count
            playerWins[gameResult[0]] += 1
            # Add loss count
            playerDirectLosses[gameResult[1]] += 1

    return playerWins, playerDirectLosses, playerTsumos


# TODO: Loop over the new function for different weight values
def simulate_games(losingWeight: float, iterations: int, subject: str, CDF: list | tuple = loadCDF()) \
        -> dict[str, dict]:
    # Simulates (iteration) games for our test subject player with the losingWeight specified
    # Returns the stats of our subject player after so many games
    sim_args = [(i, losingWeight, CDF) for i in range(iterations)]
    playerList = ['ai_0', 'ai_1', 'ai_2', 'ai_3']

    # Use multiprocessing to run the games on a multicore process
    cores = Pool(processes=6)

    gamesResults = cores.starmap(spgame_loop_opt, sim_args)
    playerWins, playerDirectLosses, playerTsumos = extractGames(gamesResults, playerList)

    # compiledResults: dict[str, tuple] = compileStats(playerWins, playerLosses, playerTsumos)
    return {
        "win": playerWins,
        "loss": playerDirectLosses,
        "tsumo": playerTsumos
    }
    # return compiledResults[subject]
    # except KeyError:
    #     # Return empty tuple / dict
    #     print('No such subject in the game, typo? Defaulting to first key')
    #     defaultKey: str = min(playerList)
    #     return {
    #         "win": playerWins[defaultKey],
    #         "loss": playerDirectLosses[defaultKey],
    #         "tsumo": playerTsumos[defaultKey]
    #     }


def main() -> int:
    import json
    import time
    processStart: float = time.time()
    gammaDist: tuple = loadCDF()
    optFunctionMap: dict[float, dict] = {}

    # Loop over n steps from -1 to 1
    n = 100
    for i in range(n + 1):
        print(f'Iteration: {i + 1}/{n + 1}')
        weight: float = -6 + (10 * i / n)
        playerResults: dict = simulate_games(weight, 16000, 'ai_1', gammaDist)
        optFunctionMap[weight]: dict = playerResults

    # Output to a json file
    output_Destination = open("fullPlayerStats_run1.json", "w")
    output_Destination.write(json.dumps(optFunctionMap))
    output_Destination.close()

    processEnd: float = time.time()
    print(f'Function main completed in {round(processEnd - processStart, 3)} s')
    return 0


if __name__ == '__main__':
    main()

# TODO: Output to csv and plot a graph to find optimum value

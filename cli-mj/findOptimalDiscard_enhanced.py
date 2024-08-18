import numpy as np
from usefulTiles import *
from hand_situation import hand_eval_adv


def handValueAfterDiscard(inner_hand: list[int], outer_hand: list[int], discard_tile: int,
                          known_pile: list[int]) -> float:
    # Hand value is a function of three parts
    # HandValue (HV) =
    # effective_handScore (from the eval function) + Useful Tiles for Partial Sets + Useful tiles for Singles
    hand_score, partials, singletons = hand_eval_adv(inner_hand.copy(), outer_hand.copy())

    # Partials sets is split into the few 'flavours' in the following order:
    # open straights, pairs, kalongs, edge straights
    # Review partial sets and deduct hand_score if the partial set is useless
    # Also we add the useful tile numbers here lol
    effective_score = hand_score
    partialsInfo: dict = usefulness_ps(partials, known_pile.copy())

    for p in partialsInfo:
        if partialsInfo[p] == 0:
            # Partial set is fake --> no useful tiles to go with it
            if p[0] == p[1]:
                # Pair,
                effective_score = effective_score - 0.5
            elif p[1] - p[0] == 2:
                # kalong
                effective_score = effective_score - 0.25
            elif p[0] % 10 in [1, 8]:
                # Edge straights
                effective_score = effective_score - 0.25
            else:
                # Open straight
                effective_score = effective_score - 0.5

    partialSetScore = sum(partialsInfo.values())

    # Singles score
    singletons_info = usefulness_ss(singletons)
    singletons_score = sum(singletons_info.values())

    # Consolidating the info into 2 vectors and returning their dot product as the value
    hv_weights = np.array([8, 4, 1])
    hv_vars = np.array([effective_score, partialSetScore, singletons_score])

    handValue = float(np.dot(hv_weights, hv_vars))

    return handValue


def loss_prob(discard_tile: int, known_pile: list[int], game_progression: int) -> float:
    # Returns the predicted loss probability of a tile given some factors
    # P_loss = m_j *  &tile_probabilty * exp(-k * num of same tile in discards) * %gamma(game_progression)
    # &tile_probability: tile probability factor (see analysis files)
    # %gamma fitted game data to a gamma distribution (again see analysis files)
    # k = fitted params from collected data (in analysis files)
    # m_j = my normalisation constant
    ...


def findOptimalDiscard_def(inner_hand: list[int], known_pile: list[int]) -> int:
    tiles_set: set[int] = set(inner_hand)
    tilesValue: dict = {}


if __name__ == '__main__':
    # Insert functions to test here
    quit()

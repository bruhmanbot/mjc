"""The dynamic playstyle for a player. The player can switch between 4 modes depending on the hand situation
Speed (normal) -- At the start or with good progress. More aggressive.
Balanced (slightly defending) -- Discards the safest single tile (if possible). Maintains hand progress.
Defensive -- Includes discarding partial sets for safety
Ultra Defensive -- Willing to discard even complete sets for safety"""

from hand_situation import hand_eval_adv
from optimalDiscard_defense import loss_probability
from optimalDiscard import findOptimalDiscard
import random
import sys
import pandas as pd
sys.path.append('../mjcpy')
from listUtils import unpack_list 

def findOptimalDiscard_balanced(inner_hand: list[int], outer_hand: list[int], known_pile: list[int], discards, tileDeck: list[int] = [], **kwargs):

    # Initialise gammaLUT
    try:
        CDF = kwargs['CDF_gamma']
    except KeyError:
        gamma_dist_LUT = pd.read_csv('./script_data/gamma-dist.csv')
        CDF = list(gamma_dist_LUT['CDF'])
    # Obtain the hand information
    allHands = hand_eval_adv(inner_hand, outer_hand, all_hands=True)

    # grouping the info
    partials = []
    singles = []
    for hand in allHands:
        partials = partials + hand[1]
        singles = singles + hand[2]

    # to Ensure hScore is not affected, we pick singles first, but suppose we do not have singles, then we pick from partials
    try: 
        singles[0]
    except IndexError:
        # Run evaluation on partials
        # Completely unpack list
        # Turning into set to get rid of dupes
        ps_unpacked_set: set = set(unpack_list(unpack_list(partials)))
        min_p:float = 100.0
        best_t: list[int] = []

        for t in ps_unpacked_set:
            p_loss = loss_probability(t, known_pile, tileDeck, discards, CDF)
            # p_loss: float = loss_probability(t, known_pile, tileDeck)

            # Curate best tile
            if p_loss < min_p:
                min_p = p_loss
                best_t = [t]

            elif p_loss == min_p:
                # If this somehow happens, we discard a random one
                best_t.append(t)

        return random.choice(best_t)



    # find safest tile from singles, using loss probability
    min_p:float = 100.0
    best_t: list[int] = []

    for s in set(singles):
        p_loss: float = loss_probability(s, known_pile, tileDeck, discards, CDF)
        
        # Curate best tile
        if p_loss < min_p:
            min_p = p_loss
            best_t = [s]

        elif p_loss == min_p:
            # If this somehow happens, we discard a random one
            best_t.append(s)

    return random.choice(best_t)

def findOptimalDiscard_defensive(inner_hand: list[int], outer_hand: list[int], known_pile:list[int], discards: list[int], tileDeck: list[int] = [], **kwargs):
    # Initialise gammaLUT
    try:
        CDF = kwargs['CDF_gamma']
    except KeyError:
        gamma_dist_LUT = pd.read_csv('./script_data/gamma-dist.csv')
        CDF = list(gamma_dist_LUT['CDF'])
    # Obtain the hand information
    # Obtain the hand information
    allHands = hand_eval_adv(inner_hand, outer_hand, all_hands=True)

    # grouping the info
    partials = []
    singles = []
    for hand in allHands:
        partials = partials + hand[1]
        singles = singles + hand[2]

    totalPartials = unpack_list(unpack_list(partials))

    tilesConsider = set(totalPartials + singles)

    # find safest tile from singles, using loss probability
    min_p:float = 100.0
    best_t: list[int] = []
    for t in tilesConsider:
        p_loss: float = loss_probability(t, known_pile, tileDeck, discards, CDF)

        # Curate best tile
        if p_loss < min_p:
            min_p = p_loss
            best_t = [t]

        elif p_loss == min_p:
            # If this somehow happens, we discard a random one
            best_t.append(t)

    return random.choice(best_t)

def findOptimalDiscard_ultraDefensive(inner_hand: list[int], outer_hand: list[int], known_pile:list[int], discards: list[int], tileDeck: list[int] = [], **kwargs):
    # Initialise gammaLUT
    try:
        CDF = kwargs['CDF_gamma']
    except KeyError:
        gamma_dist_LUT = pd.read_csv('./script_data/gamma-dist.csv')
        CDF = list(gamma_dist_LUT['CDF'])
    # find safest tile from singles, using loss probability
    min_p:float = 100.0
    best_t: list[int] = []
    for q in inner_hand:
        p_loss = loss_probability(q, known_pile, tileDeck, discards, CDF)

        # Curate best tile
        if p_loss < min_p:
            min_p = p_loss
            best_t = [q]

        elif p_loss == min_p:
            # If this somehow happens, we discard a random one
            best_t.append(q)

    return random.choice(best_t)

def findOptimalDiscard_dynamic(mode, inner_hand: list[int], outer_hand: list[int], known_pile: list[int], discards: list[int], tileDeck: list[int], **kwargs):

    # Initialise CDF
    try:
        CDF = kwargs['CDF_gamma']
    except KeyError:
        gamma_dist_LUT = pd.read_csv('./script_data/gamma-dist.csv')
        CDF = list(gamma_dist_LUT['CDF'])
    # Error correction for mode
    if mode not in [i for i in range(4)]:
        mode = 0

    match mode:
        case 0:
            # Speed mode
            discardTile = findOptimalDiscard(inner_hand, known_pile, full_eval_mode=True)

        case 1:
            # balanced mode
            discardTile = findOptimalDiscard_balanced(inner_hand, outer_hand, known_pile, discards, tileDeck, CDF_gamma=CDF)

        case 2:
            # Defensive mode
            discardTile = findOptimalDiscard_defensive(inner_hand, outer_hand, known_pile, discards, tileDeck, CDF_gamma=CDF)
        case 3:
            # Ultra Defensive mode
            discardTile = findOptimalDiscard_ultraDefensive(inner_hand, outer_hand, known_pile, discards, tileDeck, CDF_gamma=CDF)

    return discardTile


if __name__ == '__main__':
    test_hand = [11, 12, 13, 14, 15, 16, 17, 28, 29, 35, 36, 45]
    test_hand_o = []

    print(findOptimalDiscard_defensive(test_hand, test_hand_o, [], [15, 11], [0] * 50))
    # score, ps, singles = hand_eval_adv(test_hand, test_hand_o)
    # for q in range(100):
    #     print(findOptimalDiscard_balanced(test_hand, test_hand_o, [12, 12, 15], [0] * 40))

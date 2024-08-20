## Finding the optimal discard of a hand while factoring the discards
## tileValue is two components: weights \cdot params
## weights defined by the player's playstyle, dependent on whether the player is more aggressive or defensive
## the params is composed of handValue after discard and tileDanger value
from hand_situation import hand_eval_adv
from usefulTiles import usefulness_ps, usefulness_ss
from check_calling import check_calling_tiles
import numpy as np
import pandas as pd
import random

def handValueAfterdiscard(inner_hand: list[int], outer_hand: list[int], discard: int, known_pile:list[int]) -> float:
    ## Takes in the inner_hand and computes the hand value after discarding a certain tile
    # Hand value = calibrated HandScore * 8 + usefultiles partial sets * 4 + useful tiles Singles 
    operation_hand = inner_hand.copy()
    # try removing the discard tile
    try:
        operation_hand.remove(discard)
    except ValueError:
        print("Program exitted on handValueAfterDiscard function @ line 17 of opetimaDiscard_defense.py")
        print("Reason: Discard tile not in inner_hand")
        return
    
    handScore, partials, singles = hand_eval_adv(operation_hand, outer_hand)

    partialsInfo:dict = usefulness_ps(partialSets=partials, knownPile=known_pile)

    calibrated_handScore = handScore
    for ps in partialsInfo:
        # Deducting handScore if we found a useless partial set
        if partialsInfo[ps] == 0:
            if ps[0] == ps[1]:
                # Pair
                calibrated_handScore += -0.5
            elif min(ps) == max(ps) - 2:
                # Kalong
                calibrated_handScore += -0.25
            elif (min(ps) % 10) in [1,8]:
                # Edge straights
                calibrated_handScore += -0.25
            else:
                # Open straights
                calibrated_handScore += -0.5

    # # Prioritise calling
    # callers: dict = check_calling_tiles(operation_hand, outer_hand)
    # if len(callers.keys()) > 0:
    #     # print('CALLING:', callers.keys())
    #     calibrated_handScore = calibrated_handScore + 1
    
    usefulTiles_partialSets: int = sum(partialsInfo.values())

    singlesInfo: dict = usefulness_ss(singles, knownPile=known_pile)
    usefulTiles_Singles: int = sum(singlesInfo.values())

    handValue_weights = np.array([4, 0.2, 0.01])
    handValue_params = np.array([calibrated_handScore, usefulTiles_partialSets, usefulTiles_Singles])

    # print(discard, handValue_params)

    handValue:float = round(np.dot(handValue_weights, handValue_params),2)
    # print(discard, handValue_params)

    return float(handValue)

def loss_probability(tile:int, known_pile:list[int], tileDeck:list[int], discards:list[int], gammaLUT:list[float]=[]) -> float:
    # loss probabilty = tile popularity * x occurences in public domain * game progression
    # In math terms: P(loss) = t_p * [A * exp(-k*x)] * %gamma(g)
    # t_p - popularity factor (1 for LT, 4.5 for 1/9, 8.6 for 2-8)
    # game_progression (g) defined by 80 - len(tileDeck) : How many tiles are consumed
    # gamma function is used to model CDF for games ended at a certain g
    if tile in discards[-4:]:
        # Last 4 tiles cannot lose
        p_loss = 0
        return p_loss
    elif tile in discards[-12:]:
        recency = 0.5 # Recency factor
    else:
        recency = 1
    
    if tile > 40:
        t_p = 1
    elif tile % 10 in [1,9]:
        t_p = 2
    else:
        t_p = 3.5

    x = discards.count(tile)
    x = x+1 # Since that was how I modelled everything

    if t_p == 1:
        A = 4.0
        k = 1.5
    else:
        A = 1.2
        k = 0.9

    try:
        gamma_g = gammaLUT[80 - len(tileDeck)]
    except IndexError:
        gamma_dist_LUT = pd.read_csv('./script_data/gamma-dist.csv')
        CDF = list(gamma_dist_LUT['CDF'])
        gamma_g = CDF[80-len(tileDeck)]
    
    # Scaling constant m_j
    m_j = 0.64
    # print(f'exp part: {A * np.exp(-1 * k * x)}')
    # print(f'{gamma_g} - Gamama')

    p_loss = recency * m_j * t_p * A * np.exp(-1 * k * x) * (gamma_g)


    return p_loss

def findOptimalDiscard_enhanced(inner_hand: list[int], outer_hand: list[int], known_pile: list[int], discards: list[int], 
                                tileDeck: list[int], weights: tuple=(1, 1), goal='normal', **kwargs) -> int:
    # Try to find top discard tile based on danger and speed (and potential gains)
    tilesToConsider = set(inner_hand)
    tileValueDB: dict = {}
    weights_vector = np.array(weights)

    # CDF for p_loss
    try:
        CDF:list = kwargs['CDF_gamma']
        CDF[79]
    except KeyError or IndexError:
        gamma_dist_LUT = pd.read_csv('./script_data/gamma-dist.csv')
        CDF = list(gamma_dist_LUT['CDF'])

    for t in tilesToConsider:
        hValue: float = handValueAfterdiscard(inner_hand.copy(), outer_hand.copy(), t, known_pile)
        ## If applicable
        ... # Check potential score

        match goal:
            case 'normal':
                potentialScore:int = 16 # Generally the median
            case 'ligu':
                potentialScore: int = 48 # Generally the score you get
            case 'buddha':
                potentialScore: int = 60 # Median for buddha

        
        # norm serves as a normalisation constant
        norm: float = 25
        # print(handValueAfterdiscard * potentialScore)
        tile_params = np.array([hValue * potentialScore / norm, 0])

        # Loss part (danger)
        p_loss = loss_probability(t, discards, tileDeck, discards, gammaLUT=CDF)
        # Slightly diff treatment for lucky tiles bcs they generally net higher scores
        if t > 40:
            loss_value = 20 * p_loss
        else:
            loss_value = 16 * p_loss

        tile_params[1] = loss_value

        tileValue: float = np.dot(weights_vector, tile_params)
        tileValueDB[t] = round(float(tileValue),3)

    max_value = max(tileValueDB.values())
    choices = []
    for tile in tileValueDB:
        if tileValueDB[tile] == max_value:
            choices.append(tile)

    return random.choice(choices)





if __name__ == '__main__':
    domain = []
    td = [0] * 80

    i_hand = [11, 11, 12, 14, 15, 18, 21, 26, 26, 27, 31, 33, 36, 39, 39, 41, 17]
    o_hand = []

    print('running func findOptimalDiscard_enh')
    # db = findOptimalDiscard_enhanced(i_hand, o_hand, domain, td, weights=(1, -1))

    # for row in db:
    #     print (f'{row}: {db[row]}')
    for q in i_hand:
        print(q, handValueAfterdiscard(i_hand, o_hand, q, domain))

    print(findOptimalDiscard_enhanced(i_hand, o_hand, domain, td))
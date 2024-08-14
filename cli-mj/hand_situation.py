import sys
import random
sys.path.append('P:/mjc-main/mjcpy')

from listUtils import * # type: ignore

def removelt(list1: list, threshold=40):
    filtered_list = filter(lambda x: x <threshold, list1)
    removed_items = filter(lambda x: x > threshold, list1)

    return list(filtered_list), list(removed_items)


def hand_eval(inner_hand, outer_hand, priority='str'):
    # Evaluates the current situation of the hand
    # Returns completed sets and half completed sets

    # takes in the inner_hand with the drawn tile
    inner_hand_wk = inner_hand.copy()

    if priority == 'str':
        # remove lt
        inner_hand_wk, LT = removelt(inner_hand_wk)
        straights, remTiles = straightsplit(inner_hand_wk) # type: ignore
        triplets, remTiles = tripletsplit(remTiles + LT) # type: ignore # type: ignore

        numCompletedSets = (len(straights) + len(triplets)) / 3

        # Finds partial sets for the remaining tiles
        
        remTiles.sort()
        partialSetsScore, partialSets, singles = partial_set_eval(remTiles, priority='str')

        # Assuming all outside sets are already complete to save time
        outside_score = 2 * int(len(outer_hand) / 3)

        fullScore = partialSetsScore + numCompletedSets * 2 + outside_score

    else:

        triplets, remTiles = tripletsplit(inner_hand_wk) # type: ignore
        # remove lt
        remTiles, LT = removelt(remTiles)
        straights, remTiles = straightsplit(remTiles) # type: ignore

        numCompletedSets = (len(straights) + len(triplets)) / 3

        # Finds partial sets for the remaining tiles
        remTiles = remTiles + LT
        remTiles.sort()
        partialSetsScore, partialSets, singles = partial_set_eval(remTiles, priority='pair')

        # Assuming all outside sets are already complete to save time
        outside_score = 2 * int(len(outer_hand) / 3)

        fullScore = partialSetsScore + numCompletedSets * 2 + outside_score

    return fullScore, partialSets, singles

def partial_set_eval(tilesList: list, priority='str'):
    tilesList_wk = tilesList.copy()
    if priority == 'str':
        # open straights first
        openStraights = open_straights_eval(tilesList_wk)
        # pair!
        pairs = pairs_eval(tilesList_wk)
        # ka long (middle)
        kalong = kalong_eval(tilesList_wk)
        # Edge straights
        edgeStraights = edge_straights_eval(tilesList_wk)
    else:
        # Pair mode --> prioritise pairs
        # pair!
        pairs = pairs_eval(tilesList_wk)
        # open straights first
        openStraights = open_straights_eval(tilesList_wk)
        # ka long (middle)
        kalong = kalong_eval(tilesList_wk)
        # Edge straights
        edgeStraights = edge_straights_eval(tilesList_wk)

    partialSets = [openStraights , pairs , kalong, edgeStraights]
    psScore = len(openStraights) * 0.5 + len(pairs) * 0.5 + len(kalong) * 0.25 + len(edgeStraights) * 0.25
    return psScore, partialSets, tilesList_wk

def edge_straights_eval(tilesList: list):
    edgeStraights = []
    g = 0
    while g < len(tilesList):
        if ((tilesList[g] + 1) in tilesList and tilesList[g]<40):
                # remTile[g] + 2 cannot be in tilesList or else it will have been extracted as a straight
            t = tilesList[g]
            tilesList.remove(t)
            tilesList.remove(t+1)

            if (t % 10 in [1,8]):
                edgeStraights.append(list([t, t+1]))
                g = 0
            else:
                pass

        else:
            g = g + 1
    return edgeStraights

def kalong_eval(tilesList):
    kalong = []
    g = 0
    while g < len(tilesList):
        if (tilesList[g] + 2) in tilesList and tilesList[g] < 40:
            t = tilesList[g]
            if int((t+2)/10) == int(t/10):
                kalong.append(list([t, t+2]))
                tilesList.remove(t)
                tilesList.remove(t+2)
                g = 0
            else:
                g = g + 1
                continue
                
        else:
            g = g + 1
    return kalong

def pairs_eval(tilesList):
    pairs = []
    g = 0
    while g < len(tilesList):
        if tilesList.count(tilesList[g]) == 2: 
                # suppose should not be more than 3 or else it gets identified as a triplet
            t = tilesList[g]
            pairs.append(list([t, t]))
            tilesList.remove(t)
            tilesList.remove(t)
            g = 0
            
        else:
            g = g + 1
    return pairs

def open_straights_eval(tilesList):
    openStraights = []
    g = 0
    while g < len(tilesList):
        if ((tilesList[g] + 1) in tilesList and tilesList[g]<40):
                # remTile[g] + 2 cannot be in tilesList or else it will have been extracted as a straight
            t = tilesList[g]
            if (t % 10 in [1,8]):
                    # edgeStraights.append(list([t, t+1]))
                g = g + 1 
                continue
                    # reserve for later
            else:
                tilesList.remove(t)
                tilesList.remove(t+1)
                openStraights.append(list([t, t+1]))
            g = 0

        else:
            g = g + 1
    return openStraights
    

def straight_dissect_recur_core(inner_hand: list) -> list:
    # A recursive function to find the most possible straights?
    # Outputs tuple([straights], [remaining tiles])
    if type(inner_hand) != list:
        return []
    inner = inner_hand.copy()
    inner.sort()
    inner_uniq = set(inner)
    # Use a set to reduce run time
    potentialStraights = []
    for t in inner_uniq:
        if t > 40:
            continue
        if (t+1)in inner_uniq and (t+2) in inner_uniq:
            straight = [t+k for k in range(3)] # the straight!
            potentialStraights.append(straight)

    # Commit recursion if found >= 1 straight
    if len(potentialStraights):
        total_output_recur:list = []
        for straight in potentialStraights:
            remTiles = list_XOR(inner, straight, remove_all=False) # type: ignore
            temp_output: list = straight_dissect_recur_core(remTiles)
            # temp_output == [([straights], [remTiles]), (more tuples...)]
            for sub_tuple in temp_output:
                sub_tuple[0].append(straight)
                total_output_recur.append(sub_tuple)

        return total_output_recur

    # False condition return all tiles as remaining tiles
    output_tp = [([], inner)]
    return output_tp

def straight_dissect_recur(inner_hand:list) -> list:
    # enhanced versopm of straight split to give all possible combinations
    # packaged here or else the recursion goes boogaloo
    combinations:list[tuple] = straight_dissect_recur_core(inner_hand)
    combinations_uniq = []
    # tuples in combinations: ([straights identified], [remTiles])
    for combinationTuple in combinations:
        # sort everything
        sort_straights(combinationTuple[0]) # type: ignore
        combinationTuple[1].sort()
        # Extract unique elements --> make remaining computation faster
        if combinationTuple not in combinations_uniq:
            combinations_uniq.append(combinationTuple)

    return combinations_uniq

def hand_eval_adv(inner_hand: list, outer_hand: list) -> object:
    combinationsLib: list = straight_dissect_recur(inner_hand=inner_hand)
    combinationsTierDB: dict = {}
    # Generate the possible combinations in a library
    for c_i, combination in enumerate(combinationsLib):
        c_trips, remTiles = tripletsplit(combination[1]) # type: ignore
        # Add the triplets to the best combs
        c_trips_splitted = split_list(c_trips, 3) # type: ignore
        for trip in c_trips_splitted:
            combination[0].append(trip)

        # Get the set Score
        setScore = 2 * (len(combination[0]))
        # arrange the score and place it in the tierlist (dict)
        # Index of combination: resulting setScore
        combinationsTierDB[c_i] = setScore
    
    def extract_max_value_from_dict(combinationsLib, combinationsTierDB: dict):
        # Sub function for the line of code below (refactored because i may use this again somewhere idk)
        best_combs_score = max(combinationsTierDB.values())
        best_combs = []
        # Select the highest scoring
        for c_i in combinationsTierDB:
            if combinationsTierDB[c_i] == best_combs_score:
                best_combs.append(combinationsLib[c_i])
        return best_combs_score, best_combs

    best_combs_score, best_combs = extract_max_value_from_dict(combinationsLib, combinationsTierDB)

    # Best combs now a collection of the best possible hand(s) dissected from above
    combinationsTierDB = {} # clear the dict for further re-use!

    for c_i, combination in enumerate(best_combs):
        pairMode = partial_set_eval(combination[1], priority='pair')    
        strMode = partial_set_eval(combination[1], priority='str')    
        if pairMode[0] > strMode[0]:
            comb_scr = pairMode[0] + best_combs_score
            combinationsTierDB[c_i] = (comb_scr, pairMode[1], pairMode[2])
        else:
            comb_scr = strMode[0] + best_combs_score
            combinationsTierDB[c_i] = (comb_scr, strMode[1], strMode[2])
        # Writing our results to the DB

    # select highest scoring after partial set computation
    best_combs = []
    best_combs_score = 0.0
    for c_i in combinationsTierDB:
        if combinationsTierDB[c_i][0] > best_combs_score:
            best_combs_score = combinationsTierDB[c_i][0]
            best_combs = [int(c_i)]
        elif combinationsTierDB[c_i][0] == best_combs_score:
            best_combs.append(c_i)

    # Ideally we wouldn't need random here but I will include this to eliminate potential bias
    chosen_comb:int = random.choice(best_combs)

    # Add outer_hand things
    best_combs_score = best_combs_score + 2 * len(outer_hand) / 3

    # Hand score, partial sets, singled tiles
    return best_combs_score, combinationsTierDB[chosen_comb][1], combinationsTierDB[chosen_comb][2]


 



if __name__ == '__main__':
    import time # timing function runtime
    hand = [12, 12, 12, 13, 14, 15, 27]

    hand.sort()
    ## SIMPLE MODE
    
    print('Running hand_eval on test case')

    eval_simp = hand_eval(hand, outer_hand=[])
    
    print(f'Output: {eval_simp}')



    print('-----------------------------------')
    # ADV MODE
    print('Running hand_eval_adv on test case')
    eval_adv = hand_eval_adv(hand, [])

    print(f'Output: {eval_adv}')


import sys
sys.path.append('../mjcpy')

from validityCheck import hand_validity_check # type: ignore
from CounterA import std_hand_score_count # type: ignore
from buddha_check import buddha_hand_validity_check # type:ignore
from CounterB import buddha_hand_score_count # type:ignore
from ligu_check import ligu_hand_validity_check # type: ignore
from CounterL import ligu_score_count # type: ignore

def check_calling_tiles(inner_hand: list, outer_hand: list, output_score=False) -> dict:
    output_dict = {}
    for test_tile in range(11,40):
        if test_tile % 10 == 0:
            # Skip invalid tiles
            continue
        if not(test_tile - 1 in inner_hand or test_tile + 1 in inner_hand or test_tile in inner_hand):
            # Skip this tile if it is not related
            continue
        validityRes = hand_validity_check(inner_hand.copy(), outer_hand.copy(), [int(test_tile)])

        if validityRes[0] == 1:
            
            # Winning tiles is winning!
            if output_score:
                # Only run the further score counting function if required
                # Assign the func arguments
                innerS, outerS, innerT, outerT, eye = validityRes[1:]

                sc = std_hand_score_count(innerS, outerS, innerT, outerT, eye,
                                     [test_tile], 0, 1, 1, [])
                # Score into the dictionary
                output_dict[test_tile] = int(sc[3])
                continue
            # Not counting the scores (save time)
            else:
                output_dict[test_tile] = 1

    for test_tile in range(41,48):
        if not(test_tile in inner_hand):
            continue
        validityRes = hand_validity_check(inner_hand.copy(), outer_hand.copy(), [test_tile])

        if validityRes[0] == 1:
            # Winning tiles is winning!
            if output_score:
                # Only run the further score counting function if required
                # Assign the func arguments
                innerS, outerS, innerT, outerT, eye = validityRes[1:]

                sc = std_hand_score_count(innerS, outerS, innerT, outerT, eye,
                                     [test_tile], 0, 1, 1, [])
                # Score into the dictionary
                output_dict[test_tile] = int(sc[3])
                continue
            # Not counting the scores (save time)
            else:
                output_dict[test_tile] = 1
    

    return output_dict

def check_calling_tiles_bd(inner_hand:list, outer_hand:list, output_score=False)-> dict:
    if len(outer_hand):
        return {}
    # not bd if outer_hand is not empty
    bd_calling_dict = {}
    if len(inner_hand) == len(set(inner_hand)):
    # Approaching from 1 in 16 --> only check 1 tile is sufficient
        bd_valid = buddha_hand_validity_check(inner_hand, outer_hand, [inner_hand[0]])
        if bd_valid[0] == 2:
            # hand is valid with the first tile as a bd hand
            if output_score:
                # Score should basically be the same --> optimise 
                # score is only different if 2/5/8 eye
                bd_score = buddha_hand_score_count(inner_hand, [inner_hand[0]], [inner_hand[0]], 0, 1, 1, [])
                for q in inner_hand:
                    # bd_score[1] is the score output e.g. 64
                    bd_calling_dict[q] = int(bd_score[1])
            else:
                for q in inner_hand:
                    bd_calling_dict[q] = 1
        else:
            return bd_calling_dict

    # Approaching from 1 pair + missing 1 tile
    LTs = list(filter(lambda x: x>40, inner_hand))
    if len(set(LTs)) < 7:
        # less than 7 uniq LTs
        # Find missing one and verify it
        for g in range(41,48):
            bd_valid = buddha_hand_validity_check(inner_hand, outer_hand, [g])
            if bd_valid[0] == 2:
                # Breaks if valid with the g tile as winning
                if output_score:
                    # bd_score[1] is the score output e.g. 64
                    bd_score = buddha_hand_score_count(bd_valid[1], bd_valid[2], [g], 0, 1, 1, [])
                    bd_calling_dict[g] = bd_score[1]
                else:
                    bd_calling_dict[g] = 1
                break
        return bd_calling_dict
    # Last missing tile is not lucky tile
    for t in range(11,40):
        if t % 10 == 0:
            # Skips invalid tiles
            continue
        elif (t+1) in inner_hand or (t-1) in inner_hand or t in inner_hand:
            continue
            # Skips obviously invalid tiles
        bd_valid = buddha_hand_validity_check(inner_hand, outer_hand, [t])

        if bd_valid[0] == 2:
            # Valid with the tile
            if output_score:
                bd_score = buddha_hand_score_count(bd_valid[1], bd_valid[2], t, 0, 1, 1, [])
                bd_calling_dict[t] = bd_score[1]
            else:
                bd_calling_dict[t] = 1  

    return bd_calling_dict

def check_calling_tiles_ligu(inner_hand:list, outer_hand:list, output_score=False) -> dict:
    if len(outer_hand):
        return {}
    
    ligudict = {}
    for t in inner_hand:
        # assuming extra t tile --> see if win 
        # if yes --> count score (output_score == True)
        # output to dict
        ligu_res = ligu_hand_validity_check(inner_hand, outer_hand, [t])

        if ligu_res:
            if output_score:
                ligudict[t] = ligu_score_count(inner_hand, [t], 0, 1, 1, [])
            else:
                ligudict[t] = 1
    
    return ligudict

    

if __name__ == '__main__':
    inner_hand = [11, 12, 13, 14, 15, 15, 16, 17, 18, 18, 33, 33, 33, 35, 36, 37]
    outer_hand = []
    import time

    init_time = time.time()
    callers = check_calling_tiles(inner_hand, outer_hand, output_score=False)
    final_time = time.time()
    delta = final_time - init_time
    print(callers)
    print(f'runtime: {delta * 1000} ms')

import sys
sys.path.append('P:/mjc-main/mjcpy')

from validityCheck import hand_validity_check # type: ignore
from CounterA import std_hand_score_count # type: ignore

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

if __name__ == '__main__':
    inner_hand = [11, 11, 11, 19, 19, 19, 23, 24, 25, 26, 27, 28, 29]
    outer_hand = [42, 42, 42]
    import time

    init_time = time.time()
    callers = check_calling_tiles(inner_hand, outer_hand, output_score=False)
    final_time = time.time()
    delta = final_time - init_time
    print(callers)
    print(f'runtime: {delta * 1000} ms')

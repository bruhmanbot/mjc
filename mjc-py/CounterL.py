from listUtils import *
import numpy as np
from accoladeClassinit import accoladecsv_init
from flower import flower_count

def ligu_score_count(WinningHandInner:list , WinningTile: list,
                     self_drawn: int, wind: int, seat: int, Flower:list, AccoladeID=accoladecsv_init()):
    # Winning Hand outer not needed because its ligu
    # counts the score for ligu ligu and returns the accolades
    ScoreL = 0
    AccoladesL = []

    def add_accolade(ID: int) -> None:
        nonlocal ScoreL
        nonlocal AccoladesL
        # Normal mode: checks if any 1 of the kans is NOT concealed
        result = AccoladeID[ID].evaluate_score()
        ScoreL += int(result[0])
        AccoladesL.append(f'{result[1]} - {int(result[0])}')
        return
    
    # LIGU Accolade
    add_accolade(82)

    # Flowers
    flowerRes = flower_count(Flower, seat, AccoladeID)

    # Adding the final scores
    ScoreL = ScoreL + flowerRes[0]
    AccoladesL.append(flowerRes[1])

    # See if the final tile is dudu or 1 in 8
    if WinningHandInner.count(WinningTile[0]) == 1:
        # 1 corresponds to the case of du du
        add_accolade(20)
    elif WinningHandInner.count(WinningTile[0]) == 3:
        # 3 --> 1 in 2
        add_accolade(21)
    else:
        # 1 in 8 case (i.e. count == 2)
        add_accolade(83)

    # find pairs and triplets for score counting
    WinningHandTotal = WinningHandInner + WinningTile
    pairs = find_occurence(WinningHandTotal, 2)
    triplet = find_occurence(WinningHandTotal, 3)
    quads = find_occurence(WinningHandTotal, 4)

    for i in quads:
        pairs.append(i)
        pairs.append(i)

    # Wind & Scholar tile accolades
    LTScore = 0

    if triplet[0] > 40:
        if 40 < triplet[0] < 45: # Wind Tiles
            LTScore = AccoladeID[5].pts
            if triplet[0] == 40 + wind:
                # Matching wind
                LTScore = LTScore + AccoladeID[6].pts
            if triplet[0] == 40 + seat:
                # Matching seat
                LTScore = LTScore + AccoladeID[7].pts
        else: # ScholarTiles
            LTScore = AccoladeID[14].pts

        ScoreL = ScoreL + LTScore
        AccoladesL.append(f'Lucky Tiles - {LTScore}')

    # No lucky tile check
    if max(WinningHandTotal) < 40:
        LTPresent = 0
    else:
        LTPresent = 1

    if LTPresent == 0:
        add_accolade(16)

    # Consec pairs?
    unique_num_tiles = []
    consec_strings = []

    for i in (pairs + triplet):
        if not(i in unique_num_tiles) and i < 40:
            unique_num_tiles.append(i)

    unique_num_tiles.sort()
    unique_num_tiles2 = unique_num_tiles.copy()

    while len(unique_num_tiles) > 0:
        ASeq = find_arithmetic_seq(unique_num_tiles[0], unique_num_tiles, 1)
        # Count consec pairs and adds the consec no to the list consec_string
        consec_strings.append(len(ASeq))
        # Remove the counted straights
        for q in ASeq:
            unique_num_tiles.remove(q)

    if len(unique_num_tiles) == 0:
        ASeq = []

    # Aseq should return the length of each consec non Lucky straight
    # e.g. Aseq = [1, 1, 3, 1, 2]

    for i in consec_strings:
        if i < 3:
            continue
    
        # accolade id = 81+i e.g. if i = 5, accolade id -> 86
        add_accolade(int(81+i))

    unique_unit_tiles = np.array(unique_num_tiles2) % 10
    unique_units = list(unique_unit_tiles)
    unique_units.sort()



    # Suits
    SuitsPresence = [0, 0, 0]
    # [Characters, Strings, Cartons]
    for j in unique_num_tiles2:
        if j < 40:
            suit_index = int(j/10) - 1
            SuitsPresence[suit_index] = 1

    # ASeq can only be found if there are non lucky tiles
    if len(unique_num_tiles2) > 0:
        Aseq = find_arithmetic_seq(unique_units[0], unique_units, 1)

        # Super mixed dragon
        if len(Aseq) == 8 and sum(SuitsPresence) > 1:
            add_accolade(90)

    # Mixed flush, flushes, etc.

    match sum(SuitsPresence):

        case 0:
        # No normal tiles, only lucky tiles
            add_accolade(62)

        case 1:
            if LTPresent == 0: # No lucky tiles + 1 suit only
                add_accolade(61)
            else:
                add_accolade(60)

        case 2:
            if LTPresent == 0:
                add_accolade(59)

        case 3:
            if LTPresent == 1:
                WindPresent = 0
                ScholarPresent = 0
                for j in (pairs + triplet):
                    if 40 < j < 45:
                        WindPresent = 1
                    if j > 45:
                        ScholarPresent = 1

                if (WindPresent + ScholarPresent) == 2:
                    add_accolade(57)

    # Yaojiu
    yj = [11, 19, 21, 29, 31, 39]
    lt = [(41+i) for i in range(7)]

    yj_lt = yj+lt

    uniq_tiles = list(set(WinningHandTotal))

    if set_containslists(uniq_tiles, yj):
        add_accolade(72)
    elif set_containslists(uniq_tiles, yj_lt):
        
        # only 1/9 with lucky tiles
        if (f'{AccoladeID[62].acco_name} - {AccoladeID[62].pts}' in AccoladesL):
            pass
            # No double counting with LT only
        else:
            add_accolade(71)



    if self_drawn == 1:
        add_accolade(74)

    # Base!!
    add_accolade(75)

    # Final output
    final_hand = pairs * 2 + triplet * 3
    final_hand.sort()
    return final_hand, int(ScoreL), AccoladesL


# Testing
if __name__ == "__main__":
    WinningHandInnerL = [41, 41, 41, 41, 42, 42, 43, 43, 44, 44, 45, 45, 46, 46, 46, 47]
    WinningHandOuterL = []
    WinningTileL = [47]
    TestRes = ligu_score_count(WinningHandInnerL, WinningTileL, 1, 2, 3, [1,4,5,6])
    print(TestRes)
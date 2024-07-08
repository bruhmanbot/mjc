from listUtils import *
import numpy as np


def ligu_score_count(WinningHandInner:list , WinningTile: list,
                     self_drawn: int, wind: int, seat: int, Flower:list):
    # Winning Hand outer not needed because its ligu
    # counts the score for ligu ligu and returns the accolades
    ScoreL = 5
    AccoladesL = ['Base - 5']

    # Flowers
    FlowerScore = 0
    if len(Flower) == 0:
        # No flower case
        FlowerScore = 1
        AccoladesL.append('No Flowers - 1')
        ScoreL = ScoreL + FlowerScore
    else:
        # If there are flowers
        for i in Flower:
            if i % 4 == seat % 4:
                FlowerScore = FlowerScore + 2  # Matching flowers
            else:
                FlowerScore = FlowerScore + 1  # Non-Matching flowers

        if set_containslists([1, 2, 3, 4], Flower):  # One whole collection
            FlowerScore = FlowerScore - 5 + 10  # One set of flowers = 10 pts (but not counting individual pts)

        if set_containslists([5, 6, 7, 8], Flower):  # One whole collection
            FlowerScore = FlowerScore - 5 + 10  # One set of flowers = 10 pts (but not counting individual pts)
            if set_containslists([k + 1 for k in range(8)], Flower):  # All 8 flowers
                FlowerScore = 30

        # Adding the final scores
        ScoreL = ScoreL + FlowerScore
        AccoladesL.append(f'Flowers - {FlowerScore}')

    # See if the final tile is dudu or 1 in 8
    if WinningHandInner.count(WinningTile[0]) == 1:
        # 1 corresponds to the case of du du
        ScoreL = ScoreL + 42
        AccoladesL.append('LiguLigu - 40')
        AccoladesL.append('Dudu - 2')
    else:
        # the count should either be 1 or 2
        ScoreL = ScoreL + 50
        AccoladesL.append('1 in 8 LiguLigu - 50')

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
            LTScore = LTScore + 1
            if triplet[0] == 40 + wind:
                # Matching wind
                LTScore = LTScore + 1
            if triplet[0] == 40 + seat:
                # Matching seat
                LTScore = LTScore + 1
        else: # ScholarTiles
            LTScore = LTScore + 2

        ScoreL = ScoreL + LTScore
        AccoladesL.append(f'Lucky Tiles - {LTScore}')

    # No lucky tile check
    if max(WinningHandTotal) < 40:
        LTPresent = 0
    else:
        LTPresent = 1

    if LTPresent == 0:
        ScoreL = ScoreL + 1
        AccoladesL.append('No Lucky Tiles - 1')

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
        match i:
            case 3:
                ScoreL = ScoreL + 3
                AccoladesL.append('3 Consecutive Pairs - 5')

            case 4:
                ScoreL = ScoreL + 8
                AccoladesL.append('4 Consecutive Pairs - 10')

            case 5:
                ScoreL = ScoreL + 20
                AccoladesL.append('5 Consecutive Pairs - 20')

            case 6:
                ScoreL = ScoreL + 40
                AccoladesL.append('6 Consecutive Pairs - 40')

            case 7:
                ScoreL = ScoreL + 80
                AccoladesL.append('7 Consecutive Pairs - 80')

            case 8:
                ScoreL = ScoreL + 240
                AccoladesL.append('Super Dragon - 240')

    unique_unit_tiles = np.array(unique_num_tiles2) % 10
    unique_units = list(unique_unit_tiles)
    unique_units.sort()

    # ASeq can only be found if there are non lucky tiles
    if len(unique_num_tiles2) > 0:
        Aseq = find_arithmetic_seq(unique_units[0], unique_units, 1)

        # Super mixed dragon
        if len(Aseq) == 8 and not('Super Dragon - 240' in AccoladesL):
            ScoreL = ScoreL + 80
            AccoladesL.append('Super Mixed Dragon - 80')

    # Suits
    SuitsPresence = [0, 0, 0]
    # [Characters, Strings, Cartons]
    for j in unique_num_tiles2:
        if j < 40:
            suit_index = int(j/10) - 1
            SuitsPresence[suit_index] = 1
    # Mixed flush, flushes, etc.
    match sum(SuitsPresence):

        case 0:
        # No normal tiles, only lucky tiles
            ScoreL = ScoreL + 140
            AccoladesL.append('Lucky Tiles Only - 140')

        case 1:
            if LTPresent == 0: # No lucky tiles + 1 suit only
                ScoreL = ScoreL + 80
                AccoladesL.append('Full Flush - 80')
            else:
                ScoreL = ScoreL + 30
                AccoladesL.append('Mixed Flush - 30')

        case 2:
            if LTPresent == 0:
                ScoreL = ScoreL + 5
                AccoladesL.append('2 Non-Lucky Suits - 5')

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
                    ScoreL = ScoreL + 10
                    AccoladesL.append('5 small Suits - 10')

    if self_drawn == 1:
        ScoreL = ScoreL + 2
        AccoladesL.append('Self Drawn - 2')

    # Final output
    final_hand = pairs * 2 + triplet * 3
    final_hand.sort()
    return final_hand, ScoreL, AccoladesL


# Testing
if __name__ == "__main__":
    WinningHandInnerL = [11, 11, 12, 12, 13, 13, 14, 14, 35, 35, 16, 16, 17, 17, 17, 18]
    WinningHandOuterL = []
    WinningTileL = [18]
    TestRes = ligu_score_count(WinningHandInnerL, WinningTileL, 1, 2, 3, [])
    print(TestRes)
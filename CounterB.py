from listUtils import *
import numpy as np



def buddha_hand_score_count(FinalHand:list, EyePair: list, WinningTile: list,
                         SelfDrawn: int, Wind: int, Seat: int, Flower:list) -> object:
    # Winning Hand outer not needed because its 16 Buddhas
    # counts the score for Buddhas and returns the accolades
    ScoreB = 55
    AccoladesB = ['Base - 5', '16 Buddhas - 50']

    # Flowers
    FlowerScore = 0
    if len(Flower) == 0:
        # No flower case
        FlowerScore = 1
        AccoladesB.append('No Flowers - 1')
        ScoreB = ScoreB + FlowerScore
    else:
        # If there are flowers
        for i in Flower:
            if i % 4 == Seat % 4:
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
        ScoreB = ScoreB + FlowerScore
        AccoladesB.append(f'Flowers - {FlowerScore}')

    if WinningTile[0] == EyePair[0]:
        ScoreB = ScoreB + 10
        AccoladesB.append('16 Waiting Tiles - 10')
    # Dudu and other things
    elif WinningTile[0] > 40:
        ScoreB = ScoreB + 2
        AccoladesB.append('Dudu - 2')
    elif WinningTile[0] % 10 <= 3:
        if WinningTile[0] + 3 in FinalHand:
            ScoreB = ScoreB + 2
            AccoladesB.append('Dudu - 2')
    elif WinningTile[0] % 10 <= 6:
        if (WinningTile[0] + 3 in FinalHand) and (WinningTile[0] - 3 in FinalHand):
            ScoreB = ScoreB + 2
            AccoladesB.append('Dudu - 2')
    else:
        if WinningTile[0] - 3 in FinalHand:
            ScoreB = ScoreB + 2
            AccoladesB.append('Dudu - 2')

    numTiles = FinalHand[0:9]
    num_split = split_list(numTiles, 3)
    chars = list(np.array(num_split[0]) % 10)
    strings = list(np.array(num_split[1]) % 10)
    cartons = list(np.array(num_split[2]) % 10)

    tot_numTile = chars + strings + cartons
    tot_numTile.sort()

    if chars == strings == cartons:
        ScoreB = ScoreB + 10
        AccoladesB.append('Same 3 Number Tiles - 10')
    elif tot_numTile == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        ScoreB = ScoreB + 10
        AccoladesB.append('Buddha Dragon - 10')

    if SelfDrawn == 1:
        ScoreB = ScoreB + 2
        AccoladesB.append('Self Drawn - 2')

    OutputHand = FinalHand + WinningTile

    return OutputHand, ScoreB, AccoladesB

if __name__ == "__main__":
    FinalHand1 = [11, 15, 19, 21, 25, 29, 31, 35, 39, 41, 42, 43, 44, 45, 46, 47]
    EyeP = [47]
    WinningT = [21]
    print(buddha_hand_score_count(FinalHand1,EyeP,WinningT, 0, 1, 1))


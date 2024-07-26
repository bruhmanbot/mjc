from listUtils import *
import numpy as np
from accoladeClassinit import *
from accoladeClass import *
from flower import flower_count



def buddha_hand_score_count(FinalHand:list, EyePair: list, WinningTile: list,
                         SelfDrawn: int, Wind: int, Seat: int, Flower:list, AccoladeID=accoladecsv_init()) -> object:
    
    # intialise the vars
    ScoreB = 0
    AccoladesB = []
    # Add accolade function 
    # Everything doesn't have a rel_kan here so its useless
    def add_accolade(ID: int) -> None:
        nonlocal ScoreB
        nonlocal AccoladesB
        result = AccoladeID[ID].evaluate_score()
        ScoreB += int(result[0])
        AccoladesB.append(f'{result[1]} - {int(result[0])}')
        return

    # Winning Hand outer not needed because its 16 Buddhas
    add_accolade(76) # 16 buddhas
    # Base is added at the very end!!

    # Flowers
    flowerRes = flower_count(Flower, Seat, AccoladeID)

    # Adding the final scores & accolades from flowers
    ScoreB = ScoreB + flowerRes[0]
    AccoladesB.append(flowerRes[1])

    if WinningTile[0] == EyePair[0]:
        add_accolade(77)
    # Dudu and other things
    elif WinningTile[0] > 40:
        add_accolade(20)
    elif WinningTile[0] % 10 <= 3:
        if WinningTile[0] + 3 in FinalHand:
            add_accolade(20)
    elif WinningTile[0] % 10 <= 6:
        if (WinningTile[0] + 3 in FinalHand) and (WinningTile[0] - 3 in FinalHand):
            add_accolade(20)
    elif WinningTile[0] - 3 in FinalHand:
        add_accolade(20)
    else:
        pass

    numTiles = FinalHand[0:9]
    num_split = split_list(numTiles, 3)
    chars = list(np.array(num_split[0]) % 10)
    strings = list(np.array(num_split[1]) % 10)
    cartons = list(np.array(num_split[2]) % 10)

    tot_numTile = chars + strings + cartons
    tot_numTile.sort()

    if chars == strings == cartons:
        add_accolade(79)
    elif tot_numTile == [(i+1) for i in range(9)]:
        add_accolade(78)

    if SelfDrawn == 1:
        add_accolade(74)

    # Base

    add_accolade(75)

    OutputHand = FinalHand + WinningTile

    return OutputHand, ScoreB, AccoladesB

if __name__ == "__main__":
    FinalHand1 = [11, 15, 19, 21, 25, 29, 31, 35, 39, 41, 42, 43, 44, 45, 46, 47]
    EyeP = [47]
    WinningT = [47]
    print(buddha_hand_score_count(FinalHand1,EyeP,WinningT, 0, 1, 1, [1,2,3,4]))


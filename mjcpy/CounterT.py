from listUtils import set_containslists
from accoladeClassinit import accoladecsv_init
from flower import flower_count


def orphan_hand_score_count(InnerStraights: list, InnerTriplets: list, WinningTile: list, Eye: list,
                            SelfDrawn: int, Wind: int, Seat: int, Flower: list, AccoladeID=accoladecsv_init()) -> object:
    # Winning Hand outer not needed because its 13 orphans
    # counts the score for Buddhas and returns the accolades
    ScoreT = 0
    AccoladesT = []

    def add_accolade(ID: int) -> None:
        nonlocal ScoreT
        nonlocal AccoladesT
        # Normal mode: checks if any 1 of the kans is NOT concealed
        result = AccoladeID[ID].evaluate_score()
        ScoreT += int(result[0])
        AccoladesT.append(f'{result[1]} - {int(result[0])}')
        return

    # Flowers
    # Flowers
    flowerRes = flower_count(Flower, Seat, AccoladeID)

    # Adding the final scores
    ScoreT = ScoreT + flowerRes[0]
    AccoladesT.append(flowerRes[1])

    # Check winning tile points
    if len(InnerStraights) != 0:
        # In the middle
        if WinningTile[0] == InnerStraights[1]:
            add_accolade(20)

        # Check condition for ending on a 3/7 in 123/789
        elif WinningTile[0] % 10 == 7 and len(InnerStraights) != 0:
            if WinningTile[0] == InnerStraights[0]:
                add_accolade(20)
        elif WinningTile[0] % 10 == 3 and len(InnerStraights) != 3:
            if WinningTile[0] == InnerStraights[2]:
                add_accolade(20)
    # Check for 13 tile finish
    elif WinningTile[0] == Eye[0]:
        add_accolade(81)
    # Check dudu for NOT ending on the straight (imply that it ended on triplet or missing orphan)
    elif not (WinningTile[0] in InnerStraights):
        add_accolade(20)

    # Check Yaojiu
    InnerKan = InnerTriplets + InnerStraights
    YJPresent = 0
    AllYJ = 1
    for i in InnerKan:
        if i < 40:
            if i % 10 == 1 or i % 10 == 9:
                # Only 1 needs to be 1/9 for YJpresent to be 1 --> positive check
                YJPresent = 1
            else:
                # Only 1 needs to NOT be 1/9 for all YJ to be broken
                AllYJ = 0
        else:
            # this corresponds to a case where the kan is a lucky tile

            YJPresent = 1
            # All YJ is kept at 1 as before
            # AllYJ = 1 would also imply a 4 in 1
            break

    if AllYJ == 1:
        add_accolade(71)
        add_accolade(54)
    elif YJPresent == 1:
        add_accolade(69)
    # Check lucky tile
    if AllYJ == 1:
        if InnerKan[0] > 40:  # Indicate that it is a lucky tile
            LTScore = AccoladeID[5].pts
            if InnerKan[0] % 10 == Wind:
                LTScore = LTScore + AccoladeID[6].pts
            if InnerKan[0] % 10 == Seat:
                LTScore = LTScore + AccoladeID[7].pts
            if InnerKan[0] % 10 > 4:
                # Scholar tile
                LTScore = AccoladeID[14].pts
            # adding LTscore to the ScoreT counter
            ScoreT = ScoreT + LTScore
            AccoladesT.append(f'Lucky Tiles - {LTScore}')

    # Self Drawn
    if SelfDrawn == 1:
        add_accolade(74)

    # Base
    add_accolade(75)

    # Generate the output hand
    Orphans = [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47]
    FinalHand = Orphans + Eye
    FinalHand.sort()
    FinalHand = InnerKan + FinalHand

    return FinalHand, int(ScoreT), AccoladesT


if __name__ == "__main__":
    InnerStr = []
    InnerTriplet = [47, 47, 47]
    EyeP = [45]
    WinningT = [45]

    result = orphan_hand_score_count(InnerStr, InnerTriplet, WinningT, EyeP, 1, 2, 3, [7])
    print(result)

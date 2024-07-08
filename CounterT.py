from listUtils import set_containslists


def orphan_hand_score_count(InnerStraights: list, InnerTriplets: list, WinningTile: list, Eye: list,
                            SelfDrawn: int == (0 or 1), Wind: int, Seat: int, Flower: list) -> object:
    # Winning Hand outer not needed because its 13 orphans
    # counts the score for Buddhas and returns the accolades
    ScoreT = 105
    AccoladesT = ['Base - 5', '13 Orphans - 100']

    # Flowers
    FlowerScore = 0
    if len(Flower) == 0:
        # No flower case
        FlowerScore = 1
        AccoladesT.append('No Flowers - 1')
        ScoreT = ScoreT + FlowerScore
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
        ScoreT = ScoreT + FlowerScore
        AccoladesT.append(f'Flowers - {FlowerScore}')

    # Check winning tile points
    if len(InnerStraights) != 0:
        # In the middle
        if WinningTile[0] == InnerStraights[1]:
            ScoreT = ScoreT + 2
            AccoladesT.append('Dudu - 2')

        # Check condition for ending on a 3/7 in 123/789
        elif WinningTile[0] % 10 == 7 and len(InnerStraights) != 0:
            if WinningTile[0] == InnerStraights[0]:
                ScoreT = ScoreT + 2
                AccoladesT.append('Dudu - 2')
        elif WinningTile[0] % 10 == 3 and len(InnerStraights) != 3:
            if WinningTile[0] == InnerStraights[2]:
                ScoreT = ScoreT + 2
                AccoladesT.append('Dudu - 2')
    # Check for 13 tile finish
    elif WinningTile[0] == Eye[0]:
        ScoreT = ScoreT + 20
        AccoladesT.append('13 Tile Finish - 20')
    # Check dudu for NOT ending on the straight (imply that it ended on triplet or missing orphan)
    elif not (WinningTile[0] in InnerStraights):
        ScoreT = ScoreT + 2
        AccoladesT.append('Dudu - 2')

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
        ScoreT = ScoreT + 80
        AccoladesT.append('Only 1/9 with Lucky Tiles - 80')

        ScoreT = ScoreT + 5
        AccoladesT.append('4 in 1 - 5')
    elif YJPresent == 1:
        ScoreT = ScoreT + 15
        AccoladesT.append('Mixed 1/9 with Lucky Tiles - 15')
    # Check lucky tile
    if AllYJ == 1:
        if InnerKan[0] > 40:  # Indicate that it is a lucky tile
            LTScore = 1
            if InnerKan[0] % 10 == Seat:
                LTScore = LTScore + 1
            if InnerKan[0] % 10 == Wind:
                LTScore = LTScore + 1
            if InnerKan[0] % 10 > 4:
                LTScore = LTScore + 1
            # adding LTscore to the ScoreT counter
            ScoreT = ScoreT + LTScore
            AccoladesT.append(f'Lucky Tiles - {LTScore}')

    # Self Drawn
    if SelfDrawn == 1:
        ScoreT = ScoreT + 2
        AccoladesT.append('Self Drawn - 2')

    # Generate the output hand
    Orphans = [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47]
    FinalHand = Orphans + Eye
    FinalHand.sort()
    FinalHand = InnerKan + FinalHand

    return FinalHand, ScoreT, AccoladesT


if __name__ == "__main__":
    InnerStr = []
    InnerTriplet = [47, 47, 47]
    EyeP = [45]
    WinningT = [45]

    result = orphan_hand_score_count(InnerStr, InnerTriplet, WinningT, EyeP, 1, 2, 3, [7])
    print(result)

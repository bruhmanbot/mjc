from listUtils import *
import numpy as np
from accoladeClass import Acco
from accoladeClassinit import accoladecsv_init
from matrix_diagonal import check_nxn_diags

# New comment just dropped!

def std_hand_score_count(InnerStraights: list, OuterStraights: list, InnerTriplets: list,
                         OuterTriplets: list, EyePair: list, WinningTile: list,
                         SelfDrawn: int, Wind: int, Seat: int, Flower: list) -> object:
    # Standard hand point checking
    # Splitting into different Kans
    OuterKans = split_list(OuterStraights + OuterTriplets, 3)
    InnerKans = split_list(InnerStraights + InnerTriplets, 3)
    TotalKans = OuterKans + InnerKans
    # EyePair = EyePair (no need modification)

    # Regenerating WinningHandTotal
    WinningHandTotal = InnerStraights + OuterStraights + InnerTriplets + OuterTriplets + EyePair

    # Further splitting into Straights and Triplets
    InnerStraights = []
    InnerTriplets = []
    OuterStraights = []
    OuterTriplets = []

    for i in InnerKans:
        if i[1] == i[0]:
            InnerTriplets.append(i)
        else:
            InnerStraights.append(i)

    for j in OuterKans:
        if j[1] == j[0]:
            OuterTriplets.append(j)
        else:
            OuterStraights.append(j)

    # Sum of number on the Kans
    TotalKansSum = []
    for j in TotalKans:
        TotalKansSum.append(sum(j))

    # Useful Params for Pt Checking
    # Base Points + Other Params
    Score = 5
    Accolades = ['Base - 5']

    # SelfDrawn = 0 for no, 1 for yes
    countsd = 1

    # Flowers
    FlowerScore = 0

    # Wind Tiles
    WindScore = 0

    # Scholar Tiles
    ScholarScore = 0

    # No of Scholar Tiles
    # ScholarTileCount = 0

    # dudu single moment
    dudu = 0
    Fakedudu = 0

    # 般高 Same Straight Same Suit and Off-suit Same Straights
    TotalStraights = InnerStraights + OuterStraights

    # Only considering unit place for TotalStriaghts --> Offsuit repeated straights accolades
    TotalStraights_Unit = TotalStraights.copy()
    for straightNum, straight in enumerate(TotalStraights):
        for tilePos, tile in enumerate(straight):
            TotalStraights_Unit[straightNum][tilePos] = tile % 10

    # Get Straight Sums
    StraightMiddleTile = np.array([0] * len(TotalStraights))
    for index, m in enumerate(TotalStraights):
        StraightMiddleTile[index] = int(sum(m)) / 3
    StraightSumUnit = list(StraightMiddleTile % 10)
    OsRepeatedStraights_CountList = unique_occurence_count(StraightSumUnit)

    # Triplets
    TotalTriplets = InnerTriplets + OuterTriplets
    # TripletSums = []
    NumberTriplets = []

    # Triplets of the same number

    for i in TotalTriplets:
        # Lucky tiles do not count
        if i[0] < 40:
            NumberTriplets.append(int(i[0]))

    NumberTripletUnit = list(np.array(NumberTriplets) % 10)

    # Find the amount of time each numbers' triplets repeats
    RepeatedTriplets_CountList = unique_occurence_count(NumberTripletUnit)

    QuadTiles = find_occurence(WinningHandTotal, 4)  # Find all tiles which appeared 4 times in the winning hand

    # Yaojiu is present? (set to 0 for the default code to work)
    # YaojiuPresent = 0

    # Initialise scoring table
    AccoladeID = accoladecsv_init()

    # Function used to add accolades
    # Updates score and accolade list accordingly
    def add_accolade(ID: int, rel_kan=[], inverse_kan=False) -> None:
        nonlocal Score
        nonlocal Accolades
        nonlocal InnerKans
        if not inverse_kan:
            result = AccoladeID[ID].evaluate_score(relevant_kans=rel_kan, outer_kans=OuterKans)
            Score += int(result[0])
            Accolades.append(f'{result[1]} - {int(result[0])}')
        else:
            result = AccoladeID[ID].evaluate_score_var2(relevant_kans=rel_kan, inner_kans=InnerKans)
            Score += int(result[0])
            Accolades.append(f'{result[1]} - {int(result[0])}')
        return

    def remove_accolade(ID: int, rel_kan=[], inverse_kan=False) -> None:
        nonlocal Score
        nonlocal Accolades
        nonlocal InnerKans
        if not inverse_kan:
            result = AccoladeID[ID].evaluate_score(relevant_kans=rel_kan, outer_kans=OuterKans)
            Score += int(-1 * result[0])
            Accolades.remove(f'{result[1]} - {int(result[0])}')
        else:
            result = AccoladeID[ID].evaluate_score_var2(relevant_kans=rel_kan, inner_kans=InnerKans)
            Score += int(-1 * result[0])
            Accolades.remove(f'{result[1]} - {int(result[0])}')
        return

    # Flowers
    if len(Flower) == 0:
        # No flower case
        add_accolade(ID=0)
    else:
        # If there are flowers
        for i in Flower:
            if i % 4 == Seat % 4:
                FlowerScore = FlowerScore + AccoladeID[2].pts  # Matching flowers
            else:
                FlowerScore = FlowerScore + AccoladeID[1].pts  # Non-Matching flowers

        # Amount of points a set of flowers would normally get when counted seperately
        set_deduction = 3 * AccoladeID[1].pts + AccoladeID[2].pts

        if set_containslists([1, 2, 3, 4], Flower):  # One whole collection
            FlowerScore = FlowerScore - set_deduction + AccoladeID[3].pts
            # One set of flowers = 10 pts (but not counting individual pts)

        if set_containslists([5, 6, 7, 8], Flower):  # One whole collection
            FlowerScore = FlowerScore - set_deduction + AccoladeID[3].pts
            # One set of flowers = 10 pts (but not counting individual pts)
            if set_containslists([k + 1 for k in range(8)], Flower):  # All 8 flowers
                FlowerScore = AccoladeID[4].pts

        # Adding the final scores
        Score = Score + FlowerScore
        Accolades.append(f'Flowers - {FlowerScore}')

    # Number of Wind Tiles
    if 80 < sum(EyePair) < 89:
        WindTileCount = 0.5  # Eye is wind tile
    else:
        WindTileCount = 0

    for i in TotalKansSum:
        if 120 < i < 133:  # All wind tiles sum to 123 - 133 (but NOT other tiles!)
            WindTileCount = WindTileCount + 1
            WindScore = WindScore + AccoladeID[5].pts  # Any Wind tile

            # Matching wind
            if i == (40 + Wind) * 3:
                WindScore = WindScore + AccoladeID[6].pts

            # Matching Seat
            if i == (40 + Seat) * 3:
                WindScore = WindScore + AccoladeID[7].pts

    if WindTileCount >= 2.5:
        # Small 3 winds
        if WindTileCount == 2.5:
            add_accolade(8)

        # Big 3 winds
        if WindTileCount == 3:
            add_accolade(9)

        # Small 4 Winds
        if WindTileCount == 3.5:
            add_accolade(10)

        # Large 4 winds
        if WindTileCount == 4:
            add_accolade(11)

    elif WindTileCount >= 1:
        Accolades.append('Wind Tiles - ' + str(WindScore))

    # Scholar Tiles Score Counting

    if sum(EyePair) > 89:  # Scholar tiles sum to 90 92 and 94
        ScholarTileCount = 0.5  # Eye is scholar tile
    else:
        ScholarTileCount = 0

    for i in TotalKansSum:
        if 133 < i:  # All wind tiles sum to over 133 (but NOT other tiles!)
            ScholarTileCount = ScholarTileCount + 1

    if ScholarTileCount >= 2.5:
        # 3 great scholars
        if ScholarTileCount == 3:
            add_accolade(13)
        # 3 Minor Scholars
        else:
            add_accolade(12)
    elif ScholarTileCount > 0.5:
        ScholarScore = int(ScholarTileCount) * AccoladeID[14].pts
        Accolades.append('Scholar Tiles - ' + str(ScholarScore))

    # No Characters
    if ScholarTileCount + WindTileCount == 0:
        if len(Flower) == 0:
            # - {no flower score} because no flowers is double counted
            add_accolade(15)
            remove_accolade(0)
        else:
            # No lucky tiles
            add_accolade(16)

    # Accumulating the scores
    Score = Score + WindScore + ScholarScore

    # In the middle
    for i in InnerKans:
        if WinningTile[0] % 10 == 3 and WinningTile[0] < 40:
            if WinningTile[0] == i[2] and WinningTile[0] != i[1]:
                # Edge tile
                add_accolade(17)
                dudu = 1
                break
        if WinningTile[0] % 10 == 7 and WinningTile[0] < 40:
            if WinningTile[0] == i[0] and WinningTile[0] != i[1]:
                # Edge tile
                add_accolade(17)
                dudu = 1
                break
        else:
            if WinningTile[0] == i[1] and WinningTile[0] != i[0]:  # Winning tile is filling the hole
                add_accolade(18)
                dudu = 1
                break
        if abs(WinningTile[0] - EyePair[0]) in [3, 0] and same_set(WinningTile[0],
                                                                   EyePair[0]):  # Call 69 (from 6678) gets 9
            if abs(EyePair[0] - i[1]) == 2:  # 3345 -- 3/6
                Fakedudu = Fakedudu + 1
        elif WinningTile[0] in i:  # Call 69 (from 6678) gets 6 // 3345 -- 3
            Fakedudu = Fakedudu + 1

    if dudu == 0:
        if WinningTile[0] in EyePair:
            if Fakedudu != 0:
                add_accolade(19)
            else:
                add_accolade(20)

    # 1 in 2
    for i in InnerTriplets:
        if WinningTile[0] in i:
            add_accolade(21)
            break

    # General's Eye (258 eye)
    if EyePair[1] < 40 and (EyePair[1] % 10) in [2, 5, 8]:
        add_accolade(22)

    # All straights
    if len(OuterTriplets) + len(InnerTriplets) == 0:
        if f'{AccoladeID[15].acco_name} - {int(AccoladeID[15].pts)}' in Accolades:
            # Removing double counted no lucky tiles and flowers
            remove_accolade(15)

            # All straights with no lucky tiles and flowers
            add_accolade(23)
        else:
            Score = Score + 5
            Accolades.append("All Straights - 5")

    # Smol old and dragon

    NumberDragon = [[11, 12, 13], [14, 15, 16], [17, 18, 19]]
    StringDragon = [[21, 22, 23], [24, 25, 26], [27, 28, 29]]
    CartonDragon = [[31, 32, 33], [34, 35, 36], [37, 38, 39]]
    DragonSet = [NumberDragon, StringDragon, CartonDragon]
    DragonList = NumberDragon + StringDragon + CartonDragon

    YaojiuTriplets = [[[11, 11, 11], [19, 19, 19]], [[21, 21, 21], [29, 29, 29]], [[31, 31, 31], [39, 39, 39]]]

    # Dragon
    for i in DragonSet:
        if set_containslists(i, TotalKans):
            add_accolade(25, rel_kan=i)
        elif set_containslists([i[0], i[2]], TotalKans):
            add_accolade(26, rel_kan=[i[0], i[2]])

    # Smol Old (Triplet Version)

    for m in YaojiuTriplets:
        if set_containslists(m, TotalKans):
            add_accolade(26, rel_kan=m)

    # Mixed Dragon (use determinant here)
    MixedDragonArray = [0] * 9
    # for i in DragonSet:
    #     for j in i:
    #         if j in InnerKans:
    #             index_change = DragonSet.index(i) * 3 + i.index(j)
    #             MixedDragonArray[index_change] = 1
    #
    # MixedDragonArrayInner = np.array(MixedDragonArray)
    # MixedDragonArrayInner = MixedDragonArrayInner.reshape((3, 3))

    for i in DragonSet:
        for j in i:
            if j in TotalKans:
                index_change = DragonSet.index(i) * 3 + i.index(j)
                MixedDragonArray[index_change] = 1

    MixedDragonArrayTot = np.array(MixedDragonArray)
    MixedDragonArrayTot = MixedDragonArrayTot.reshape((3, 3))

    # Calculate diagonals
    target_diags = check_nxn_diags(MixedDragonArrayTot)

    # From valid mixed dragons to scoring
    for diag in target_diags:
        func_kan = []
        for kan in diag:
            func_kan.append(DragonList[kan])
        add_accolade(27, func_kan)

    # Concealed Triplets
    if len(InnerTriplets) >= 2:
        match len(InnerTriplets):
            # Accolade 28-32 for concealed triplet accolades
            case 2:
                add_accolade(28)
            case 3:
                add_accolade(29)
            case 4:
                add_accolade(30)
            case 5:
                if SelfDrawn:
                    # KanKan
                    add_accolade(32)
                    countsd = 0
                else:
                    # 5 Conealed triplets
                    add_accolade(31)

    # Counting Off-suit Straight Repeats
    # Isolating 4 straights and 5 straights
    # Following list made to stop double counting 2 os straights
    Checked_occurrences = []

    Count_SuitedStraights = 1
    for i in OsRepeatedStraights_CountList:
        if not (i in Checked_occurrences):
            match i:
                case 4:
                    OS_repeated_straight = find_occurence(TotalStraights_Unit, 4)
                    # List should be length 1

                    straight_indices = find_index_duplicate_item(OS_repeated_straight[0], TotalStraights_Unit)
                    # List of integers
                    # Gets indices of the repeated straights and then finds the kans and shoves it into func_kan
                    # for further processing
                    func_kan = []
                    for j in straight_indices:
                        # Utilising the fact that total straights and total straights unit does not change any indices
                        func_kan.append(TotalStraights[j])

                    add_accolade(35, func_kan)
                    Count_SuitedStraights = 0
                case 5:
                    OS_repeated_straight = find_occurence(TotalStraights_Unit, 5)
                    # List should be length 1

                    straight_indices = find_index_duplicate_item(OS_repeated_straight[0], TotalStraights_Unit)
                    # List of integers
                    # Gets indices of the repeated straights and then finds the kans and shoves it into func_kan
                    # for further processing
                    func_kan = []
                    for j in straight_indices:
                        # Utilising the fact that total straights and total straights unit does not change any indices
                        func_kan.append(TotalStraights[j])

                    add_accolade(36, func_kan)
                    Count_SuitedStraights = 0
                case 3:
                    # Only one case where occurrence = 3 (no double 3 相逢)
                    OS_repeated_straight = find_occurence(TotalStraights_Unit, 3)
                    # List should be length 1

                    straight_indices = find_index_duplicate_item(OS_repeated_straight[0], TotalStraights_Unit)

                    # List of integers
                    # Gets indices of the repeated straights and then finds the kans and shoves it into func_kan
                    # for further processing
                    func_kan = []
                    for j in straight_indices:
                        # Utilising the fact that total straights and total straights unit does not change any indices
                        func_kan.append(TotalStraights[j])

                    if len(set(func_kan)) == 3:  # If all items are unique. length of the set(func_kan) == 3
                        add_accolade(34, func_kan)
                    # A more complicated system is needed here to avoid counting 2 suited straights + 1 off suit
                    # straight
                    elif len(set(func_kan)) > 1:
                        # Only considering the two unique straights
                        add_accolade(33, list(set(func_kan)))
                    # The above corresponds to the case of 2 suited + 1 off suit
                case 2:
                    # Since there are cases that the target_list has 2 elements
                    Checked_occurrences.append(2)

                    # Only one case where occurrence = 3 (no double 3 相逢)
                    OS_repeated_straight = find_occurence(TotalStraights_Unit, 2)
                    # List should be length 1/2

                    for j in OS_repeated_straight:
                        straight_indices = find_index_duplicate_item(j, TotalStraights_Unit)

                        # List of integers
                        # Gets indices of the repeated straights and then finds the kans and shoves it into func_kan
                        # for further processing
                        func_kan = []
                        for k in straight_indices:
                            # Utilising the fact that total straights and total straights unit
                            # does not change any indices
                            func_kan.append(TotalStraights[k])

                        if len(set(func_kan)) != 1:  # Off-suit case
                            # Pretty sure this is the only accolade i need to do this for
                            add_accolade(33, func_kan, inverse_kan=True)

    if Count_SuitedStraights == 1:
        RepeatedStraights_CountList = unique_occurence_count(TotalStraights)
    else:
        RepeatedStraights_CountList = []

    # Calculating le accolades for suited straights
    for j in RepeatedStraights_CountList:
        match j:
            case 2:
                Score = Score + 5
                Accolades.append('2 Suited Repeated Straights - 5')
            case 3:
                Score = Score + 15
                Accolades.append('3 Suited Repeated Straights - 15')
            case 4:
                Score = Score + 30
                Accolades.append('4 Suited Repeated Straights - 30')

    # Bu Bu Gao 步步高 (BBG)
    # Tricolor bu bu gao (BBG)

    for i in range(len(StraightSumUnit)):
        firstMiddleTile = StraightMiddleTile[i]
        MT_unit = firstMiddleTile % 10
        # Finding potential bu bu gaos
        straight1_index_list = find_index_duplicate_item(MT_unit + 1, StraightSumUnit)
        straight2_index_list = find_index_duplicate_item(MT_unit + 2, StraightSumUnit)
        # Retrieves the indices of the items with the next straight number
        # e.g. for i = 4 from (13, 14, 15), gets i no for i = 5 (x4, x5, x6) ,
        # and i = 6 (y5, y6, y7)
        # lists must be non empty to continue
        for q in straight1_index_list:
            for j in straight2_index_list:
                BBG_suits = [firstMiddleTile, StraightMiddleTile[q], StraightMiddleTile[j]]
                BBG_suits = np.array(BBG_suits)
                BBG_suits = list(np.floor(BBG_suits / 10))

                BBG_suitCount = len(unique_occurence_count(BBG_suits))
                # suit count = 3 --> Tricolor ; suitcount = 1 --> Single suit

                # Since TotalStraights = Inner + Outer and the other straight related lists
                # are arithmetic derivatives, the inner straights tiles are still listed first
                # if all 3 tiles are inner, then three indices should be smaller than len(InnerStriaghts) - 1
                # All inner check
                indices = [i, q, j]
                AllInner = True
                for k in indices:
                    if k > len(InnerStraights) - 1:
                        AllInner = False

                if BBG_suitCount == 3:
                    if AllInner:
                        Score = Score + 10
                        Accolades.append('Concealed Tricolor BBG - 10')
                    else:
                        Score = Score + 5
                        Accolades.append('Tricolor BBG - 5')
                elif BBG_suitCount == 1:
                    if AllInner:
                        Score = Score + 20
                        Accolades.append('Concealed BBG - 20')
                    else:
                        Score = Score + 10
                        Accolades.append('BBG - 10')

    # Ladder (123, 234, 456, 567, 678)
    if 'All Straights - 5' in Accolades:
        # Ladders only exist if all straights
        Straight_seq = find_arithmetic_seq(min(StraightSumUnit), StraightSumUnit, 1)
        if len(Straight_seq) == 5:
            Accolades.remove('All Straights - 5')
            if len(OuterStraights) == 0:
                Score = Score + 60 - 5
                Accolades.append('Concealed Ladder - 60')
            else:
                Score = Score + 30 - 5
                Accolades.append('Ladder - 30')

    # Calculating le accolades for same numbered triplets (off-suit)
    check2 = 1  # avoid checking 2 twice
    for j in RepeatedTriplets_CountList:
        if check2 != 0:
            match j:
                case 2:
                    check2 = 0
                    target_list = find_occurence(NumberTripletUnit, 2)
                    for i in target_list:
                        if EyePair[0] % 10 == i:
                            # The eye pair is also the same number as the two same numbered pairs
                            # e.g. [16, 16, 16, 26, 26, 26] with eye [36, 36]
                            Score = Score + 10
                            Accolades.append('3 small Brothers - 10')
                        else:
                            Score = Score + 3
                            Accolades.append('2 Brothers - 3')

                case 3:
                    Score = Score + 15
                    Accolades.append('3 BIG Brothers - 15')

    # Consecutive suited triplets
    i = 0
    # Only sort if it is not empty to avoid the error
    if len(NumberTriplets) != 0:
        NumberTriplets.sort()

    while i < len(NumberTriplets):
        ConsTriplets = find_arithmetic_seq(NumberTriplets[i], NumberTriplets, 1)
        ConsTripletsNo = len(ConsTriplets)
        if ConsTripletsNo > 1:
            if EyePair[0] == ConsTriplets[0] - 1 or EyePair[0] == ConsTriplets[-1] + 1:
                ConsTripletsNo = ConsTripletsNo + 0.5
            # Giving out the accolades
            match ConsTripletsNo:
                case 2:
                    Score = Score + 3
                    Accolades.append('2 Sisters - 3')
                case 2.5:
                    Score = Score + 8
                    Accolades.append('3 small Sisters - 8')
                case 3:
                    Score = Score + 15
                    Accolades.append('3 BIG Sisters - 15')
                case 3.5:
                    Score = Score + 20
                    Accolades.append('4 small Sisters - 20')
                case 4:
                    Score = Score + 40
                    Accolades.append('4 BIG Sisters - 40')
                case 4.5:
                    Score = Score + 60
                    Accolades.append('5 small Sisters - 60')
                case 5:
                    Score = Score + 80
                    Accolades.append('5 BIG Sisters - 80')
                case 6:
                    Score = Score + 120
                    Accolades.append('6 small Sisters - 120')
        # Removing the counted items from the list
        for j in ConsTriplets:
            NumberTriplets.remove(j)
        i = 0

    # 4 in 1 / 4 in 2 / 4 in 4

    for q in QuadTiles:
        KanAppearance = 0
        for i in TotalKans:  # Searches through each kan to see how kans q is contained in
            if q in i:
                KanAppearance = KanAppearance + 1
        # if 2 kan, that should be a triplet + a straight--> 4 in 1
        # or 2 straight + eyePair --> 4 in 2
        # 3 kan is impossible
        # 4 kan is 4 in 4
        match KanAppearance:
            case 2:
                if q == EyePair[0]:
                    Score = Score + 10
                    Accolades.append('4 in 2 - 10')
                else:
                    Score = Score + 5
                    Accolades.append('4 in 1 - 5')
            case 4:
                Score = Score + 20
                Accolades.append('4 in 4 - 20')
            case _:
                continue

    # 5 Suits (Large) and (Smol) and other suited things
    # Since we already have wind tile and scholar tile count, we can test for presence of the 3 suited tiles

    # 5 Suits
    SuitsPresence = [0, 0, 0, WindTileCount, ScholarTileCount]  # Indicate the presence of the 3 non-lucky tile suits

    for i in TotalKansSum:
        if 30 < i < 60:  # Suit 1 (11-19) so sum doesn't exceed 60
            SuitsPresence[0] = 1
        if 60 < i < 90:  # Suit 2 (21-29) so sum ranges between 60 and 90
            SuitsPresence[1] = 1
        if 90 < i < 120:  # Suit 3 (31-39) so sum ranges between 90 and 120
            SuitsPresence[2] = 1

    if EyePair[0] < 40:
        match int(EyePair[0] / 10):
            case 1:
                SuitsPresence[0] = SuitsPresence[0] + 0.5
            case 2:
                SuitsPresence[1] = SuitsPresence[1] + 0.5
            case 3:
                SuitsPresence[2] = SuitsPresence[2] + 0.5

    # Normalizing SuitsPresence
    for i in range(len(SuitsPresence)):
        if SuitsPresence[i] >= 1:
            SuitsPresence[i] = 1

    # 5 Suits
    if sum(SuitsPresence) == 4.5:
        Score = Score + 10
        Accolades.append("Small 5 Suits - 10")
    elif sum(SuitsPresence) == 5:
        Score = Score + 15
        Accolades.append("BIG 5 Suits - 15")

    # 2 Non-Lucky Suits
    # Sum of SuitsPresence should be less than or equal to 2 and there is no contribution from lucky tiles
    if sum(SuitsPresence) <= 2 and SuitsPresence[-2:] == [0, 0]:
        Score = Score + 5
        Accolades.append("2 Non-Lucky Suits - 5")

    # Mixed Flush
    # Only one in the first 3 suits should be not equal to 0 and LuckyTile count must exceed 0
    # & Full flush
    # Only one in the first 3 suits should appear and LuckyTile count = 0
    # Lucky Tiles only
    if sum(SuitsPresence[0:3]) <= 1:
        if SuitsPresence[0:3] == [0, 0, 0]:
            Score = Score + 100
            Accolades.append("Lucky Tiles Only - 150")
        elif SuitsPresence[-2:] != [0, 0]:
            Score = Score + 30
            Accolades.append("Mixed Flush - 30")
        else:
            Score = Score + 80
            Accolades.append("Full Flush - 80")

    # All triplets
    # If there are no straights, there must only be triplets
    if len(TotalStraights) == 0 and not ('KanKan - 120' in Accolades):
        # No double counting if KanKan // lucky tile only
        if SuitsPresence[0:3] != [0, 0, 0]:
            Score = Score + 30
            Accolades.append("All triplets - 30")

    # Dependent and Independent 全求人 半求人 門清 門清一摸七
    if len(OuterKans) == 5:
        # 5 Kans outside and winning with only 1 tile
        if SelfDrawn == 1:
            # Half Dependent?
            Score = Score + 10
            Accolades.append('Half from others - 10')
            countsd = 0
        else:
            Score = Score + 15
            Accolades.append('All from others - 15')
    elif len(OuterKans) == 0 and not ('KanKan - 120' in Accolades):
        # All kans are inside
        if SelfDrawn == 1:
            Score = Score + 7
            Accolades.append('Independent - 7')
            countsd = 0
        else:
            Score = Score + 3
            Accolades.append('Clean Doorstep - 3')

    # Yaojius
    # No Yaojiu (Tanyao)
    YaojiuPresent = 0

    if SuitsPresence[-2:] == [0, 0]:
        for i in WinningHandTotal:
            if i % 10 == (1 or 9):
                YaojiuPresent = 2
                break
        if YaojiuPresent == 0:
            Score = Score + 5
            Accolades.append('Tanyao - 5')

    # Mixed Yaojiu (Pure and non-Pure) + Pure Yaojiu
    # The following for loop checks if there is a 1/9 in every non-lucky tile kan

    for i in TotalKans:
        if YaojiuPresent == 0:
            break
        elif sum(i) < 120:
            YJCheckKan = np.array(i)  # Setting the kan to be checked
            if 1 in list(YJCheckKan % 10) or 9 in list(YJCheckKan % 10):  # If a yaojiu is present in the kan
                if len(unique_occurence_count(list(YJCheckKan % 10))) != 1:
                    # If the kan is 111/999 len(...) should return 1
                    YaojiuPresent = 1
                # A pure 111/999 hand doesn't exec this code and yaojiupresent remains 2
                continue
            else:
                YaojiuPresent = 0
                break

    match YaojiuPresent:
        case 2:
            if SuitsPresence[-2:] == [0, 0]:
                Score = Score + 180
                Accolades.append('Only 1/9 - 180')
            else:
                Score = Score + 100
                Accolades.append('Only 1/9 with Lucky Tiles - 100')
        case 1:
            if SuitsPresence[-2:] == [0, 0]:
                Score = Score + 50
                Accolades.append('Pure Mixed 1/9 - 50')
            else:
                Score = Score + 25
                Accolades.append('Mixed 1/9 with Lucky Tiles - 25')

    # Self-Drawn
    if countsd == 1 and SelfDrawn == 1:
        Score = Score + 2
        Accolades.append('Self Drawn - 2')
    # JIHU CHIKEN CHIKEN CHIKEN
    if Score == 6:
        Score = 30
        Accolades.clear()
        Accolades.append('Base - 5')
        Accolades.append('Chicken - 25')

    # Final output
    return InnerKans, OuterKans, EyePair, Score, Accolades


# Testing
if __name__ == "__main__":
    ace = std_hand_score_count([11, 12, 13, 11, 12, 13, 21, 22, 23, 31, 32, 33], [34, 35, 36],
                               [], [], [16, 16], [36], 1,
                               2, 3, [])

    print(ace[4], ace[3])

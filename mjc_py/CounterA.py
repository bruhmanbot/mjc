import numpy as np
from flower import flower_count
from accoladeClassinit import accoladecsv_init
from listUtils import *
from matrix_diagonal import check_nxn_diags


# Code begins here

def std_hand_score_count(InnerStraights: list, OuterStraights: list, InnerTriplets: list,
                         OuterTriplets: list, EyePair: list, WinningTile: list,
                         SelfDrawn: int, Wind: int, Seat: int, Flower: list, AccoladeID=accoladecsv_init()) -> object:
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
    Score = 0
    Accolades = []

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
    TotalStraights_Unit = []
    for straight in TotalStraights:
        new_straight = []
        for tile in straight:
            new_straight.append(int(tile % 10))
        TotalStraights_Unit.append(new_straight)

    OsRepeatedStraights_CountList = unique_occurence_count(TotalStraights_Unit)

    # Get Middle tile info
    StraightMiddleTile = np.array([0] * len(TotalStraights))
    for index, m in enumerate(TotalStraights):
        StraightMiddleTile[index] = int(sum(m)) / 3
    StraightSumUnit = list(StraightMiddleTile % 10)

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
    # AccoladeID = accoladecsv_init()

    # Function used to add accolades
    # Updates score and accolade list accordingly
    def add_accolade(ID: int, rel_kan=[], inverse_kan=False) -> None:
        nonlocal Score
        nonlocal Accolades
        nonlocal InnerKans
        if not inverse_kan:
            # Normal mode: checks if any 1 of the kans is NOT concealed
            result = AccoladeID[ID].evaluate_score(relevant_kans=rel_kan, outer_kans=OuterKans)
            Score += int(result[0])
            Accolades.append(f'{result[1]} - {int(result[0])}')
        else:
            # Inverse mode: checks if there exist a version of all the kans in innerkans
            # Should only be used for offsuit repeated straights i think
            result = AccoladeID[ID].evaluate_score_var2(relevant_kans=rel_kan, inner_kans=InnerKans)
            Score += int(result[0])
            Accolades.append(f'{result[1]} - {int(result[0])}')
        return

    def remove_accolade(ID: int, rel_kan=[], inverse_kan=False) -> None:
        nonlocal Score
        nonlocal Accolades
        nonlocal InnerKans
        if inverse_kan:
            result = AccoladeID[ID].evaluate_score(relevant_kans=rel_kan, outer_kans=OuterKans)
            Score += int(-1 * result[0])
            Accolades.remove(f'{result[1]} - {int(result[0])}')
        else:
            result = AccoladeID[ID].evaluate_score_var2(relevant_kans=rel_kan, inner_kans=InnerKans)
            Score += int(-1 * result[0])
            Accolades.remove(f'{result[1]} - {int(result[0])}')
        return

    # Flowers
        # Flowers
    flowerRes = flower_count(Flower, Seat, AccoladeID)

    # Adding the final scores & accolades from flowers
    Score = Score + flowerRes[0]
    Accolades.append(flowerRes[1])

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
            # all straights
            add_accolade(24)

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
            add_accolade(25, rel_kan=i, inverse_kan=True)
        # Smol add
        elif set_containslists([i[0], i[2]], TotalKans):
            add_accolade(26, rel_kan=[i[0], i[2]], inverse_kan=True)

    # Smol Old (Triplet Version)

    for m in YaojiuTriplets:
        if set_containslists(m, TotalKans):
            add_accolade(26, rel_kan=m)

    # Mixed Dragon (use determinant here)
    MixedDragonArray = [0] * 9

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
        add_accolade(27, func_kan, inverse_kan=True)

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
    doCheck_2 = True

    Count_SuitedStraights = 1
    for i in OsRepeatedStraights_CountList:
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
                    func_kan.append(tuple(TotalStraights[j]))

                if len(set(func_kan)) == 3:  # If all items are unique. length of the set(func_kan) == 3
                    add_accolade(34, func_kan)
                # A more complicated system is needed here to avoid counting 2 suited straights + 1 off suit
                # straight
                elif len(set(func_kan)) > 1:
                    # Only considering the two unique straights
                    add_accolade(33, list(set(func_kan)))
                # The above corresponds to the case of 2 suited + 1 off suit
            case 2:
                if doCheck_2:
                    # Since there are cases that the target_list has 2 elements
                    doCheck_2 = False

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
                            func_kan.append(tuple(TotalStraights[k]))

                        if len(set(func_kan)) != 1:  # Off-suit case
                            # Pretty sure this is the only accolade i need to do this for
                            add_accolade(33, func_kan, inverse_kan=True)

    if Count_SuitedStraights == 1:
        RepeatedStraights_CountList = unique_occurence_count(TotalStraights)
    else:
        RepeatedStraights_CountList = []

    # Calculating le accolades for suited straights
    doCheck_2 = True
    for j in RepeatedStraights_CountList:
        match j:
            case 2:
                # Two of the same straight same suit
                if doCheck_2:
                    # Prevents double counting since there may be 2 items with value == 2 in the CountList
                    suited_straights = find_occurence(TotalStraights, 2)
                    # Finds the straights which have repeated twice
                    for straight in suited_straights:
                        # Since the straight repeating twice is already known, 
                        # can directly add to func_kan
                        # Also since it is repeating, one kan is enough
                        func_kan = list(straight)

                        # Check if any 1 of the straight is outside --> normal
                        # Normal mode is sufficient
                        add_accolade(37, func_kan)

                doCheck_2 = False
            case 3:
                suited_straights = find_occurence(TotalStraights, 3)
                # Finds the straight which has repeated 3 times
                # should only be 1 such straight at max (suited_straights is list of length 1)
                add_accolade(38, suited_straights[0])
                # Normal type check suffices here (if none of the 3 are outside == all 3 are inside)

            case 4:
                suited_straights = find_occurence(TotalStraights, 4)
                # Finds the straight which has repeated 4 times
                # should only be 1 such straight at max (suited_straights is list of length 1)
                add_accolade(39, suited_straights[0])
                # Normal type check suffices here (if none of the 4 are outside == all 3 are inside)

    # Bu Bu Gao 步步高 (BBG)
    # Tricolor bu bu gao (BBG)
    for i, straight in enumerate(TotalStraights_Unit):
        # first straight in the sequence is straight with index i in TotalStraights and TotalStraights_Unit
        i_nparr = np.array(straight)

        straight1_index_list = find_index_duplicate_item(list(i_nparr + 1), TotalStraights_Unit)
        # Returns the indices of the next straight e.g. [1,2,3] find indices for [2,3,4]
        straight2_index_list = find_index_duplicate_item(list(i_nparr + 2), TotalStraights_Unit)
        # Returns the indices of the next straight e.g. [1,2,3] find indices for [3,4,5]

        i_nparr = np.array(TotalStraights[i])
        # Setting i as an np_array containing its original straight
        # Finding the suit of i
        i_suit = np.floor(i_nparr.mean() / 10)

        for q in straight1_index_list:
            # Setting q and j to be arrays with their original straights
            q_nparr = np.array(TotalStraights[q])
            # Finding suit of q
            q_suit = np.floor(q_nparr.mean() / 10)
            for j in straight2_index_list:
                # Iterating over all combinations of q and j (i.e. all possible combinations for BBG)
                j_nparr = np.array(TotalStraights[j])
                # Finding suit for j
                j_suit = np.floor(j_nparr.mean() / 10)

                suit_set = {i_suit, q_suit, j_suit}
                # Set of the three suit of the three straights

                if len(suit_set) == 3:  # 3 distinct suits --> Tricolor
                    func_kan = [list(i_nparr), list(q_nparr), list(j_nparr)]
                    add_accolade(40, func_kan, inverse_kan=True)
                    # Need to use inverse mode since its possible for repeated straight + BBG
                elif len(suit_set) == 1:  # 1 suit --> Single suit BBG
                    func_kan = [list(i_nparr), list(q_nparr), list(j_nparr)]
                    add_accolade(41, func_kan, inverse_kan=True)
                    # Need to use inverse mode since its possible for repeated straight + BBG

    # Ladder (123, 234, 456, 567, 678)
    if len(TotalTriplets) == 0:
        # Ladders only exist if all straights i.e. no triplets!
        Straight_seq = find_arithmetic_seq(min(StraightSumUnit), StraightSumUnit, 1)
        if len(Straight_seq) == 5:
            remove_accolade(24)
            # Ladder == 42
            add_accolade(42, rel_kan=TotalStraights)

    def add_eye_to_inner() -> None:
        # Determines if eye should be appended to innerkans
        # Useful for the brother/sister
        # Make sure to delete Eyepair after use to avoid incorrect indexing for other functions
        nonlocal InnerKans, EyePair, SelfDrawn
        # Always inner if final tile is SelfDrawn
        if SelfDrawn:
            InnerKans.append(EyePair)
            return
        # Executes if the final tile is not self drawn
        elif WinningTile[0] != EyePair[0]:
            # Eyepair must be concealed/inside if WinningTile is not the eye
            InnerKans.append(EyePair)
            return
        # unpack innerkan list -> count occurence of eye need to write unpack function!
        WinningHandInner = unpack_list(InnerKans)
        # >= 1 --> add to innerkans
        if WinningHandInner.count(EyePair[0]) >= 1:
            InnerKans.append(EyePair)
            return
        # == 0 DO NOT ADD TO innerkans
        else:
            return

    def remove_eye_from_inner() -> None:
        nonlocal EyePair, InnerKans
        # Removes the eye from InnerKans (if possible) after use
        try:
            # Removes Eyepair from InnerKans if successful
            InnerKans.remove(EyePair)
        except ValueError:
            # Nothing should occur if Eyepair is not in Innerkans to begin with
            pass
        return

    # Calculating le accolades for same numbered triplets (off-suit)
    doCheck_2 = 1  # avoid checking 2 twice
    for j in RepeatedTriplets_CountList:
        match j:
            case 2:
                if doCheck_2:
                    doCheck_2 = 0
                    target_list = find_occurence(NumberTripletUnit, 2)
                    for i in target_list:
                        indices = find_index_duplicate_item(i, NumberTripletUnit)
                        # Adding the normal number triplets into func kan
                        func_kan = []
                        for k in indices:
                            kan = [NumberTriplets[k]] * 3
                            # Returning a list of length 3
                            func_kan.append(kan)
                            # Adds the list to func_kan

                        if EyePair[0] % 10 == i:
                            # The eye pair is also the same number as the two same numbered pairs
                            # e.g. [16, 16, 16, 26, 26, 26] with eye [36, 36]
                            func_kan.append(EyePair)

                            # Add the eye pair to innerKans (if applicable) for add_accolade function
                            add_eye_to_inner()
                            add_accolade(44, func_kan)

                            # Fixing up InnerKans list
                            remove_eye_from_inner()

                        else:
                            # 2 bros
                            add_accolade(43, func_kan)

            case 3:
                # Find unit number which has appeared 3 times in triplets
                # Should only have one such element if available
                unit = int(find_occurence(NumberTripletUnit, 3)[0])
                # Holy list comprehension
                func_kan = [[10 * (suit + 1) + unit] * 3 for suit in range(3)]
                # 3 bros
                add_accolade(45, func_kan)

    # Consecutive suited triplets
    i = 0
    # Only sort if it is not empty to avoid the error
    if len(NumberTriplets) != 0:
        NumberTriplets.sort()

    while i < len(NumberTriplets):
        ConsTriplets = find_arithmetic_seq(NumberTriplets[i], NumberTriplets, 1)
        ConsTripletsNo: float = len(ConsTriplets)
        if ConsTripletsNo > 1:
            # loading the consecutive triplets into func_kan
            func_kan = [[repeating_tile] * 3 for repeating_tile in ConsTriplets]

            # checks if the eye extends the AS
            if EyePair[0] == ConsTriplets[0] - 1 or EyePair[0] == ConsTriplets[-1] + 1:
                # Adds the Eyepair to func_kan if needed
                ConsTripletsNo = ConsTripletsNo + 0.5
                func_kan.append([EyePair])
                # Adds the eye to inner for checking
                add_eye_to_inner()

            # Linear equation to map ConsTripletsNo to ID of the accolade
            # AccoladeID = 2*ConsTripletsNo + 42
            sisID = int(2 * ConsTripletsNo + 42)

            # Giving out the accolades
            add_accolade(sisID, func_kan)

            # Removing the eyepair from InnerKans
            remove_eye_from_inner()

        # Removing the counted items from the list
        for j in ConsTriplets:
            NumberTriplets.remove(j)
        i = 0

    # 4 in 1 / 4 in 2 / 4 in 4

    for q in QuadTiles:
        func_kan = []
        KanAppearance = 0
        for i in TotalKans:  # Searches through each kan to see how kans q is contained in
            if q in i:
                KanAppearance = KanAppearance + 1
                # Prepping func_kan again
                func_kan.append(i)
        # if 2 kan, that should be a triplet + a straight--> 4 in 1
        # or 2 straight + eyePair --> 4 in 2
        # 3 kan is impossible
        # 4 kan is 4 in 4
        match KanAppearance:
            case 2:
                if q == EyePair[0]:  # 4 in 2
                    # Adding eyepair to func_kan and InnerKans
                    func_kan.append(EyePair)
                    add_eye_to_inner()
                    add_accolade(55, func_kan)
                    # Fixing up InnerKans
                    remove_eye_from_inner()
                else:  # 4 in 1
                    add_accolade(54, func_kan)
            case 4:  # 4 in 4
                add_accolade(55, func_kan)
            case _:
                # This part technically is not required since there shouldn't be a case where this occurs?
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
        # Small 5 suits
        add_accolade(57)
    elif sum(SuitsPresence) == 5:
        # Big 5 suits
        add_accolade(58)

    # 2 Non-Lucky Suits
    # Sum of SuitsPresence should be less than or equal to 2 and there is no contribution from lucky tiles
    if (1 < sum(SuitsPresence) <= 2) and SuitsPresence[-2:] == [0, 0]:
        add_accolade(59)

    # Mixed Flush
    # Only one in the first 3 suits should be not equal to 0 and LuckyTile count must exceed 0
    # & Full flush
    # Only one in the first 3 suits should appear and LuckyTile count = 0
    # Lucky Tiles only
    if sum(SuitsPresence[0:3]) <= 1:
        if SuitsPresence[0:3] == [0, 0, 0]:
            # Lucky Tiles only
            add_accolade(62)
        elif SuitsPresence[-2:] != [0, 0]:
            # Mixed Flush
            add_accolade(60)
        else:
            # Full Flush
            add_accolade(61)

    # All triplets
    # If there are no straights, there must only be triplets
    if len(TotalStraights) == 0 and not (f'{AccoladeID[32].acco_name} - {int(AccoladeID[32].pts)}' in Accolades):
        # No double counting if KanKan // lucky tile only
        if SuitsPresence[0:3] != [0, 0, 0]:
            # All triplets
            add_accolade(63)

    # Dependent and Independent 全求人 半求人 門清 門清一摸七
    if len(OuterKans) == 5:
        # 5 Kans outside and winning with only 1 tile
        if SelfDrawn == 1:
            # Half Dependent?
            add_accolade(64)
            countsd = 0
        else:
            # All from others
            add_accolade(65)
    # No double counting if KanKan
    elif len(OuterKans) == 0 and not (f'{AccoladeID[32].acco_name} - {int(AccoladeID[32].pts)}' in Accolades):
        # All kans are inside
        if SelfDrawn == 1:
            # independence 門清一摸七
            add_accolade(66)
            countsd = 0
        else:
            # Clean doorstep
            add_accolade(67)

    # Yaojius
    # No Yaojiu (Tanyao)
    YaojiuPresent = 0

    for i in WinningHandTotal:
        if i % 10 == (1 or 9) or i > 40:
            YaojiuPresent = 2
            break

    if SuitsPresence[-2:] == [0, 0] and YaojiuPresent == 0:
        # Tanyao
        add_accolade(68)

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
                # Only 1/9
                add_accolade(72)
                # Removing All triplets
                remove_accolade(63)
            else:
                # Only 1/9 With Lucky Tiles
                add_accolade(71)
                # Removing All triplets
                remove_accolade(63)
        case 1:
            if SuitsPresence[-2:] == [0, 0]:
                # Pure Mixed 1/9
                add_accolade(70)
            else:
                # Mixed 1/9 with Lucky Tiles
                add_accolade(69)

    # Self-Drawn
    if countsd == 1 and SelfDrawn == 1:
        add_accolade(74)
    # JIHU CHIKEN CHIKEN CHIKEN
    if Score == 1:
        Score = 0
        Accolades.clear()
        # chicken
        add_accolade(73)

    # Base
    add_accolade(75)

    # Final output
    return InnerKans, OuterKans, EyePair, Score, Accolades


# Testing
if __name__ == "__main__":
    ace = std_hand_score_count([], [],
                               [11, 11, 11, 19, 19, 19, 44, 44, 44, 41, 41, 41], [42, 42, 42], [45, 45], [44], 1,
                               2, 3, [])

    print(ace[4], ace[3])

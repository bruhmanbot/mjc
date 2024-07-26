from listUtils import *


def check_list_elements_unrelated(list3):
    # Checks if the list elements are related 搭唔搭
    list3.sort()
    for i in range(len(list3)-1):
        if list3[i + 1] - list3[i] <= 2:
            return False

    return True


def buddha_hand_validity_check(WinningHandInner, WinningHandOuter, WinningTile):
    # Checking the winning hand
    WinningHandTotal = WinningTile + WinningHandOuter + WinningHandInner

    tileCount = unique_occurence_count(WinningHandTotal)
    if max(tileCount) > 4:
        return 0, [], [], []

    # Checking if there are outer tiles
    if len(WinningHandOuter) > 0:
        # Invalid hand condition
        return 0, [], [], []

    # Check if all lucky tiles are there
    for i in range(41, 48):
        if not (i in WinningHandTotal):
            # Invalid hand condition
            return 0, [], [], []

    # Seperating lucky and non-lucky tiles
    Non_LT_Hand = []
    for j in WinningHandTotal:
        if j < 40:
            Non_LT_Hand.append(j)
    # Split into buddha or 13 orphans

    StraightsB, RemTiles_S = straightsplit(Non_LT_Hand)
    TripletsB, RemTiles_T = tripletsplit(Non_LT_Hand)
    if len(StraightsB) + len(TripletsB) > 0:
        # A straight or triplet exists (i.e. actual kan)
        check_hand = 0
        # Check_hand = 0 for 13 orphans hand (potential)
    else:
        check_hand = 1
        # Check_hand = 1 for 16 Buddhas Hand (potential)

    Orphans = [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47]  # 13 orphans

    if check_hand == 0:
        # 13 orphas check
        RemHand1 = WinningHandTotal.copy()

        for i in Orphans:
            try:
                RemHand1.remove(i)
            except ValueError:
                return 0, [], [], []
                # Returns false value immediately after an orphan is missing
            else:
                continue
        # Should be 4 tiles remaining in RemHand1
        StraightsB, RemHand2 = straightsplit(RemHand1)
        TripletsB, RemHand = tripletsplit(RemHand2)

        # If RemHand survives until now, it should only have 1 tile left, which is our eye
        # And that should also be an orphan
        if RemHand[0] in Orphans:
            return 1, StraightsB, TripletsB, RemHand[0]
        else:
            return 0, [], [], []

    elif check_hand == 1:
        # 16 buddhas check

        # Find the eye
        Potential_eyes = element_appeared_n_times_find(WinningHandTotal, 2)

        if len(Potential_eyes) != 1:
            return 0, [], [], []
        # Exactly one tile appeared twice for 16 Buddhas

        WinningHandTotalB = WinningHandTotal.copy()
        WinningHandTotalB.remove(Potential_eyes[0])

        for i in range(41,48): # Removes all Lucky Tiles
            try:
                WinningHandTotalB.remove(i)
            except ValueError:
                return 0, [], [], []
                # Returns false value immediately after an orphan is missing
            else:
                continue

        # At here the 9 number tiles should remain, but here is to check that
        if max(WinningHandTotalB) > 40:
            return 0, [], [], []

        # Split the 9 tiles into the 3 suits
        chars = []
        strings = []
        cartons = []
        for i in WinningHandTotalB:
            if 10 < i < 20:
                chars.append(i)
            elif 20 < i < 30:
                strings.append(i)
            elif 30 < i < 40:
                cartons.append(i)
            else:
                return 0, [], [], []
            # Since this indicates there is somehow an extra lucky tile

        # Checks if the 3 number tiles are related and assess them for the final condition
        validConditionB = bool((check_list_elements_unrelated(chars)) and (check_list_elements_unrelated(strings))
                               and (check_list_elements_unrelated(cartons)))

        FinalHand = WinningHandTotal.copy()
        FinalHand.remove(Potential_eyes[0])
        FinalHand.sort()

        if validConditionB:
            return 2, FinalHand, Potential_eyes, []
        else:
            return 0, [], [], []


if __name__ == "__main__":
    WH_Out = []
    WH_In = [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47, 16, 16, 16]
    WT = [47]
    WH_In.sort()
    print(WH_In)
    print(buddha_hand_validity_check(WH_In, WH_Out, WT))

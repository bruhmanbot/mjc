from listUtils import *

def hand_validity_check(WinningHandInner, WinningHandOuter, WinningTile):
    # Checking the winning hand
    WinningHandTotal = WinningTile + WinningHandOuter + WinningHandInner
    if not(listtypecheck(WinningHandTotal, int) == 1 and len(WinningHandTotal) == 17):
        WinningHandValid = 0
        return WinningHandValid, [], [], [], [], []
    
    # Check if any tile has more than 4 occurences
    tileCount = unique_occurence_count(WinningHandTotal)
    if max(tileCount) > 4:
        WinningHandValid = 0
        return WinningHandValid, [], [], [], [], []

    # Procedure: Find eye -> Check straights -> Check triplets
    # Assign 2 for WinningHandValid for actual winning hands

    # Find all possible eyes
    # Winning Deck includes all inner and the winning tile
    PotentialEyes = element_appeared_n_times_find(WinningHandInner + WinningTile, 2)
    Eye = 0

    # See if hands stand with different eyes
    # Only applies for standard hands
    InnerWinningHandValid = 0
    InnerStraights = []
    InnerTriplets = []
    LuckyTiles = []

    for iteration, i in enumerate(PotentialEyes):
        # Remove the two eye tiles from the WinningDeck
        WinningDeck = list(WinningHandInner + WinningTile).copy()
        WinningDeck.remove(i)
        WinningDeck.remove(i)

        # Removing the lucky tiles for straight checking
        for m in WinningDeck:
            if m > 40:
                WinningDeck.remove(m)
                if iteration == 0:
                    LuckyTiles.append(m)

        # Straight Checking
        # Using result as a temp var to store the outputs from funcs
        InnerStraights, RemainingInnerTilesToCheck = straightsplit(WinningDeck)

        # Triplet checking

        InnerTriplets, RemainingInnerTiles = tripletsplit(RemainingInnerTilesToCheck + LuckyTiles)

        # Check to see if the hand is winning using Algorithm Straight then Triplet
        if len(RemainingInnerTiles) == 0:

            InnerWinningHandValid = 1
            Eye = i
            break
        else:
            # Use Alternative algorithm here Triplet then straight
            # Remaking Winning Deck

            WinningDeck = list(WinningHandInner + WinningTile).copy()

            WinningDeck.remove(i)
            WinningDeck.remove(i)

            # Triplet Check to Lucky Tile removal to Straight Check
            InnerTriplets, RemainingInnerTilesToCheck = tripletsplit(WinningDeck)

            # Check if lucky tiles exists
            LuckyTilesExist = 0
            for m in RemainingInnerTilesToCheck:
                if m > 40:
                    LuckyTilesExist = 1
                    break

            if LuckyTilesExist == 0:
                InnerStraights, RemainingInnerTiles = straightsplit(RemainingInnerTilesToCheck)
                if len(RemainingInnerTiles) == 0:
                    InnerWinningHandValid = 1
                    Eye = i
                    break


    # Setting our eye
    EyePair = [Eye, Eye]

    # Outer Check
    OuterWinningHandValid = 0
    WinningHandOuter_noLT = list(filter(lambda x: x < 40, WinningHandOuter))
    LT = list(filter(lambda x: x > 40, WinningHandOuter))
    OuterStraights, RemainingOuterTilesToCheck = straightsplit(WinningHandOuter_noLT)
    OuterTriplets, RemainingOuterTiles = tripletsplit(RemainingOuterTilesToCheck + LT)

    if len(RemainingOuterTiles) == 0:
        OuterWinningHandValid = 1
    else:
        OuterTriplets, RemainingOuterTilesToCheck = tripletsplit(WinningHandOuter)
        OuterStraights, RemainingOuterTiles = straightsplit(RemainingOuterTilesToCheck)
        if len(RemainingOuterTiles) == 0:
            OuterWinningHandValid = 1

    # Combining Results to give total check

    if not bool(InnerWinningHandValid and OuterWinningHandValid):
        WinningHandValid = 0
        return 0, [], [], [], [], []
    else:
        WinningHandValid = 1

    return WinningHandValid, InnerStraights, OuterStraights, InnerTriplets, OuterTriplets, EyePair

# Testing purposes
if __name__ == "__main__":

    WinningHandInnerT = [18, 18, 27, 27, 31, 31, 31]
    WinningHandOuterT = [46, 46, 46, 38, 38, 38, 32, 32, 32]
    WinningTileT = [27]

    print(hand_validity_check(WinningHandInnerT, WinningHandOuterT, WinningTileT))

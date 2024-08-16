from listUtils import *


def ligu_hand_validity_check(WinningHandInner: list, WinningHandOuter: list, WinningTile: list):
    # Checks if the hand is suitable for ligu ligu
    # ligu ligu has no outer tiles
    if len(WinningHandOuter) != 0:
        WinningHandLiguValid = 0
        return WinningHandLiguValid
    
    WinningHandTotal = WinningHandInner + WinningTile
    
    tileCount = unique_occurence_count(WinningHandTotal)
    if max(tileCount) > 4:
        WinningHandLiguValid = 0
        return WinningHandLiguValid

    
    pairs = find_occurence(WinningHandTotal, 2)
    triplet = find_occurence(WinningHandTotal, 3)
    quads = find_occurence(WinningHandTotal, 4)

    # Ligu has 8 pairs + 1 triplet
    if (len(pairs) + len(quads) * 2 != 7) or (len(triplet) != 1):
        WinningHandLiguValid = 0
        return WinningHandLiguValid
    else:
        WinningHandLiguValid = 1
        return WinningHandLiguValid


# Testing
if __name__ == "__main__":
    WinningHandInnerL = [13, 13, 17, 17, 19, 19, 25, 25, 32, 32, 32, 32, 34, 34, 43, 43]
    WinningHandOuterL = []
    WinningTileL = [17]

    print(ligu_hand_validity_check(WinningHandInnerL, WinningHandOuterL, WinningTileL))

from CounterA import *
from validityCheck import *
from ligu_check import ligu_hand_validity_check
from CounterL import ligu_score_count
from buddha_check import buddha_hand_validity_check
from CounterB import buddha_hand_score_count
from CounterT import orphan_hand_score_count


# Press the green button in the gutter to run the script.
def mj_scorecount(WinningTile: list, WinningHandOuter: list, WinningHandInner: list, SelfDrawn: int, Wind: int,
                  Seat: int, flowers: list):
    # # Entering the winning hand
    #
    # # Enter the winning hand (Winning tile)
    # WinningTile = [43]
    #
    # # Enter the winning hand (outer tiles) IN ORDER!
    # WinningHandOuter = []
    #
    # # Enter the winning hand (inner tiles)
    # WinningHandInner = [12, 15, 18, 22, 26, 29, 29, 31, 34, 38, 41, 42, 44, 45, 46, 47]
    #
    # # Other params
    # SelfDrawn = 0  # 1 for yes, 0 for no
    # Wind = 3  # 1234 for ESWN
    # Seat = 4  # 1 for Dealer

    funcResult = []  # Priming output list

    # Checking type and length
    WinningHandTotal = WinningTile + WinningHandOuter + WinningHandInner
    if listtypecheck(WinningHandTotal, int) != 1 or len(WinningHandTotal) != 17:
        funcResult.append("Invalid Hand")
        funcResult.append("~")
        return funcResult

    # Running validity tests
    # Standard Hands
    WinningHandValid, InnerStraights, OuterStraights, InnerTriplets, OuterTriplets, EyePair = (
        hand_validity_check(WinningHandInner, WinningHandOuter, WinningTile))

    # LiguLigu
    WinningHandLigu = ligu_hand_validity_check(WinningHandInner, WinningHandOuter, WinningTile)

    # Buddha // 13 Orphans
    # The two results variables will be renamed again once we have established the identity of our hand
    WinningHandBuddha, BuddhaRes1, BuddhaRes2, BuddhaRes3 = buddha_hand_validity_check(WinningHandInner,
                                                                                       WinningHandOuter, WinningTile)

    # Cheating Hand
    if WinningHandBuddha + WinningHandValid + WinningHandLigu == 0:
        funcResult.append("Invalid Hand")
        funcResult.append("Cheating - -30")
        return funcResult

    # Counting Scores
    # Standard hand
    if WinningHandValid == 1:
        result = std_hand_score_count(InnerStraights, OuterStraights, InnerTriplets, OuterTriplets,
                                      EyePair, WinningTile, SelfDrawn, Wind, Seat, flowers)
        # InnerKans = result[0]
        # OuterKans = result[1]
        # EyePair = result[2]
        Score = result[3]
        Accolades = result[4]
        # print(f'Standard Hand \n -----------------------------------')
        # print(f'Outer Hand: {OuterKans}')
        # print(f'Inner Hand: {InnerKans} {EyePair}')
        funcResult.append(Score)
        funcResult.append(Accolades)

    # Ligu Hand
    if WinningHandLigu == 1:
        result = ligu_score_count(WinningHandInner, WinningTile, SelfDrawn, Wind, Seat, flowers)
        # FinalHandL = result[0]
        ScoreL = result[1]
        AccoladesL = result[2]
        # print(f'Ligu Hand \n -----------------------------------')
        # print(f'Winning Hand: {FinalHandL}')
        funcResult.append(ScoreL)
        funcResult.append(AccoladesL)

    # Buddha // 13 orphans
    if WinningHandBuddha == 1:
        # 13 orphans
        # T suffix denotes use for 13 orphans
        InnerStraightsT = BuddhaRes1.copy()
        InnerTripletsT = BuddhaRes2.copy()
        EyeT = [BuddhaRes3]

        result = orphan_hand_score_count(InnerStraightsT, InnerTripletsT, WinningTile,
                                         EyeT, SelfDrawn, Wind, Seat, flowers)
        # FinalHandT = result[0]
        ScoreT = result[1]
        AccoladesT = result[2]
        # Output MSG
        funcResult.append(ScoreT)
        funcResult.append(AccoladesT)

    elif WinningHandBuddha == 2:
        # 16 Buddhas
        FinalHandB = BuddhaRes1.copy()
        EyeB = BuddhaRes2.copy()
        # Running through the score counting algorithms
        result = buddha_hand_score_count(FinalHandB, EyeB, WinningTile, SelfDrawn, Wind, Seat, flowers)
        # FinalHandB = result[0]
        ScoreB = result[1]
        AccoladesB = result[2]
        # Output MSG
        funcResult.append(ScoreB)
        funcResult.append(AccoladesB)

    return funcResult


if __name__ == '__main__':
    # Enter the winning hand (Winning tile)
    WTile = [45]

    # Enter the winning hand (outer tiles) IN ORDER!
    WOuter = []

    # Enter the winning hand (inner tiles)
    WInner = [11, 14,17, 22, 25, 28, 39,36,33, 41, 42, 43, 44, 45, 46, 47]

    dialog = mj_scorecount(WTile, WOuter, WInner, 0, 1, 1, [1,2,3,4])

    print(dialog)

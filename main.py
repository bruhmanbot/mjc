from CounterA import *
from validityCheck import *
from ligu_check import ligu_hand_validity_check
from CounterL import ligu_score_count
from buddha_check import buddha_hand_validity_check
from CounterB import buddha_hand_score_count
from CounterT import orphan_hand_score_count

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Entering the winning hand

    # Enter the winning hand (Winning tile)
    WinningTile = [43]

    # Enter the winning hand (outer tiles) IN ORDER!
    WinningHandOuter = []

    # Enter the winning hand (inner tiles)
    WinningHandInner = [12, 15, 18, 22, 26, 29, 29, 31, 34, 37, 41, 42, 44, 45, 46, 47]

    # Other params
    SelfDrawn = 0  # 1 for yes, 0 for no
    Wind = 3  # 1234 for ESWN
    Seat = 4  # 1 for Dealer

    # Checking type and length
    WinningHandTotal = WinningTile + WinningHandOuter + WinningHandInner
    if listtypecheck(WinningHandTotal, int) == 1 and len(WinningHandTotal) == 17:
        WinningHandValid = 1  # 1 would mean it makes sense but not necessarily winning
    else:
        print('You entered something blatantly wrong, are you stupid?')
        quit()

    # Running validity tests
    # Standard Hands
    WinningHandValid, InnerStraights, OuterStraights, InnerTriplets, OuterTriplets, EyePair = (
        hand_validity_check(WinningHandInner, WinningHandOuter, WinningTile))

    # LiguLigu
    WinningHandLigu = ligu_hand_validity_check(WinningHandInner, WinningHandOuter, WinningTile)

    # Buddha // 13 Orphans
    # The two results variables will be renamed again once we have established the identity of our hand
    WinningHandBuddha, BuddhaRes1, BuddhaRes2, BuddhaRes3 = buddha_hand_validity_check(WinningHandInner, WinningHandOuter, WinningTile)

    # Counting Scores
    # Standard hand
    if WinningHandValid == 1:
        result = std_hand_score_count(InnerStraights, OuterStraights, InnerTriplets, OuterTriplets,
                                      EyePair, WinningTile, SelfDrawn, Wind, Seat)
        InnerKans = result[0]
        OuterKans = result[1]
        EyePair = result[2]
        Score = result[3]
        Accolades = result[4]
        print(f'Standard Hand \n -----------------------------------')
        print(f'Outer Hand: {OuterKans}')
        print(f'Inner Hand: {InnerKans} {EyePair}')
        for i in Accolades:
            print(i)
        print(f'Score: {Score}')
    else:
        print("Non-standard hand")

    # Ligu Hand
    if WinningHandLigu == 1:
        result = ligu_score_count(WinningHandInner, WinningTile, SelfDrawn, Wind, Seat)
        FinalHandL = result[0]
        ScoreL = result[1]
        AccoladesL = result[2]
        print(f'Ligu Hand \n -----------------------------------')
        print(f'Winning Hand: {FinalHandL}')
        for i in AccoladesL:
            print(i)
        print(f'Score: {ScoreL}')

    # Buddha // 13 orphans
    if WinningHandBuddha == 1:
        # 13 orphans
        # T suffix denotes use for 13 orphans
        InnerStraightsT = BuddhaRes1.copy()
        InnerTripletsT = BuddhaRes2.copy()
        EyeT = [BuddhaRes3]

        result = orphan_hand_score_count(InnerStraightsT, InnerTripletsT, WinningTile,
                                         EyeT, SelfDrawn, Wind, Seat)
        FinalHandT = result[0]
        ScoreT = result[1]
        AccoladesT = result[2]
        # Output MSG
        print(f'13 Orphans\n -----------------------------------')
        print(f'Winning Hand: {FinalHandT}')
        for i in AccoladesT:
            print(i)
        print(f'Score: {ScoreT}')

    elif WinningHandBuddha == 2:
        # 16 Buddhas
        FinalHandB = BuddhaRes1.copy()
        EyeB = BuddhaRes2.copy()
        # Running through the score counting algorithms
        result = buddha_hand_score_count(FinalHandB, EyeB, WinningTile, SelfDrawn, Wind, Seat, [])
        FinalHandB = result[0]
        ScoreB = result[1]
        AccoladesB = result[2]
        # Output MSG
        print(f'16 Buddhas\n -----------------------------------')
        print(f'Winning Hand: {FinalHandB}')
        for i in AccoladesB:
            print(i)
        print(f'Score: {ScoreB}')



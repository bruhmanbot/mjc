import random

def split_suits(hand:list):
    # splits the hand into the 3 suits and outputs the unit digits of the 3 suits
    # e.g. [11, 14, 17, 25 ,26, 27, 33, 35, 36] --> [1, 4, 7], [5 ,6, 7], [3, 5, 6]
    suit = [[], [], []]

    for t in hand:
        if t > 40:
            continue
        elif 30 < t < 40:
            suit[2].append(t)
        elif 20 < t < 30:
            suit[1].append(t)
        else:
            suit[0].append(t)

    return suit


def buddha_suitCompleteness(suit:list):
    # outputs all unrelated possible combinations of tiles in the same suit
    # e.g. [11, 14, 15, 17, 18] --> [[11, 14, 17], [11, 14, 18], [11, 15, 18]]
    # MAKE A COPY OF THE LIST SO THE FUNCTION IS NON DESTRUCTIVE!
    suit_wk = suit.copy()    
    suit_wk.sort()

    # impossible to have unrelatedness with the 2 following conditions
    if len(suit_wk) == 0:
        # Empty suit
        return []
    elif suit_wk[0] % 10 > 3:
        return []

    elif suit_wk[-1] % 10 < 7:
        return []
    
    # Splitting into low / mid / high range
    suit_low = set(list(filter(lambda x: (x % 10)<4, suit_wk))) # Low range: 1,2,3)
    suit_mid = set(list(filter(lambda x: 3<(x%10)<7, suit_wk))) # mid range : 4, 5, 6
    suit_high = set(list(filter(lambda x: (x%10)>6, suit_wk))) # High range: 7, 8, 9

    # Budhha sets: sets that fulfill the unrelatedness criteria
    buddha_sets = []
    for i in suit_low:
        # Finding available companions in the mid range
        mid_complem = [(j+i+3) for j in range(3)]
        for j in mid_complem:
            # Skip if j in not in the hand
            # Breaks the whole loop if j exceeds 6 (all subsequent elements dont matter)
            if j%10 > 6:
                break
            elif j not in suit_mid:
                continue

            # Finding available companions in the high range
            for k in range(3):
                if int(j+3+k) in suit_high:
                    # Add the buddha sets if possible
                    buddha_sets.append(tuple((i,j, j+3+k)))
                elif (j+3+k) % 10 == 0:
                    # Exit the loop early to save time
                    break

    # Retruning the output
    return buddha_sets

def range_split(suit:list) -> list:
    # Generate the amt of uniq tiles on a range
    suit_low = set(list(filter(lambda x: (x % 10)<4, suit))) # Low range: 1,2,3)
    suit_mid = set(list(filter(lambda x: 3<(x%10)<7, suit))) # mid range : 4, 5, 6
    suit_high = set(list(filter(lambda x: (x%10)>6, suit))) # High range: 7, 8, 9
    return [suit_low, suit_mid, suit_high]

def listsXOR(list1:list, list2:list, remove_all=True):
    # deletes elements from list 1 assuming list 2 is a subset of list 1
    list1w = list1.copy()
    for q in list2:
        list1w.remove(q)
        # remove_all = False only removes 1 occurence
        while list1w.count(q) > 0 and remove_all:
                list1w.remove(q)

    return list1w


def buddha_findBestDiscard(inner_hand:list, knownPile: list, return_all=False) -> any:
    ## Assuming that we are aiming for a buddha hand --> outputs a tile that u should throw away
    # Priority: Throw away triplets/quads --> Throw away excess tiles in suits (if possible) --> Throw away excess pairs
    # e.g. if [5,6,9] throw away 5 s.t. [6,9] allows for the most tiles to get an unrelated set [1/2/3,6,9]
    excessTiles = []
    for t in set(inner_hand):
        if inner_hand.count(t) >= 3:
            # Filter triplets / quads
            excessTiles.append(t)

    # Return random excess tile if it exist    
    if len(excessTiles):

        if return_all:
            return excessTiles
        return random.choice(excessTiles)
    
    suits_splitted = split_suits(inner_hand)
    buddha_sets = []
    for s in suits_splitted:
        # Evaluates where there is a complete buddha set here
        unrelated_sets = buddha_suitCompleteness(s)
        if len(unrelated_sets) == 0:
            buddha_sets.append([])
            continue
        else:
            # append unrelated set chosen
            buddha_sets.append(random.choice(unrelated_sets))

    for ind, s in enumerate(buddha_sets):
        # Considering all the chosen sets
        # Noting that type(s) == list
        if len(s) == 0:
            # Skip if no excess tiles
            continue
        # Adds excess tiles based on removing all elements of the selected buddha set from the original splitted suit
        excessTiles = excessTiles + listsXOR(suits_splitted[ind], s)

    if len(excessTiles):
        if return_all:
            return excessTiles
        # Return random excess tile here
        return random.choice(excessTiles)
    
    # Somehow without a completed buddha set on any of the 3 suits
    
    ranges_list = []
    for s in suits_splitted:
        ranges_list = ranges_list + range_split(s)
        
    # Ranges list arranged as such:
    # [1-low, 1-mid, 1-high, 2-low, 2-mid, 2-high, 3-low, 3-mid, 3-high {sets}]
    # Find one set with 2 (or more) elements, and output the less "extreme" one
    mid_range_keeps: dict = {}
    for index_q, q in enumerate(ranges_list):
        if len(q) <= 1:
            continue
        # Skips all single lists or empty lists
        elif index_q % 3 == 0:
            # Low range
            excessTiles.append(max(q))
            continue
            
        elif index_q % 3 == 2:
            # High range
            excessTiles.append(min(q))
            continue
        
        # Mid range
        # Using this dict to record of the {mid range tile to keep: useful tile count}
        # e.g. for tiles 5-8, outputs the tile count of 1 and 2 summed together (count(1) + count(2))
       
        if (len(ranges_list[index_q-1]) == 0) and (len(ranges_list[index_q+1]) == 0):
            # No lower range complement and no higher range complement:
            excessTiles = excessTiles + list(q)
            continue
            # Doesn't really matter what we do

        if (len(ranges_list[index_q+1]) != 0):
            # High range complement exists
            hr_complement = max(ranges_list[index_q+1])
            
            # find if the lr_complement has a friend up here
            # If it has, we keep the smallest tile that is the friend --> i.e. discard others
            q_filtered: list = list(filter(lambda x: x<=hr_complement-3, q))
            if len(q_filtered):
                keep_tile: int = max(q_filtered)
                # Extract the low range useful tiles
                useful_count = 0
                counter = 1
                while True:
                    # Target tile is keep_tile suit, but ending in 1/2/3
                    tile:int = int(keep_tile/10) * 10 + counter

                    # Check if tile is related, e.g. 3 > 5 - 3 (so we exit the loop)
                    if tile > keep_tile - 3:
                        break

                    # Add the count of the tile to our useful_count
                    useful_count += 4 - knownPile.count(tile)
                    counter += 1


                mid_range_keeps[keep_tile] = useful_count
                # add all the tiles to excessTiles (will remove keep tile later)
                excessTiles = excessTiles + list(set(q))
            else:
                # e.g. 567 --> we're kinda cooked, but we'd like to keep the larger ones ig
                excessTiles.append(min(q))

        if (len(ranges_list[index_q-1]) != 0):
            # Lower range complement exists
            # No upper range complement --> discard largest tile that doesn't hamper progress
            lr_complement = min(ranges_list[index_q-1])
            
            # find if the lr_complement has a friend up here
            # If it has, we keep the smallest tile that is the friend --> i.e. discard others
            q_filtered: list = list(filter(lambda x: x>=lr_complement+3, q))
            if len(q_filtered):
                keep_tile: int = max(q_filtered)

                # Extract the low range useful tiles
                useful_count = 0
                counter = 9
                while True:
                    # Target tile is keep_tile suit, but ending in 1/2/3
                    
                    tile: int = int(keep_tile/10) * 10 + counter
                    # Check if tile is related, e.g. 8 < 6 + 3 (so we exit the loop)
                    if tile < keep_tile + 3:
                        break

                    # Add the count of the tile to our useful_count
                    useful_count += (4 - knownPile.count(tile))
                    counter += -1


                mid_range_keeps[keep_tile] = useful_count
                # add all the tiles to excessTiles (will remove keep tile later)
                excessTiles = excessTiles + list(set(q))
            else:
                # e.g. 345 --> we're kinda cooked, but we'd like to keep the larger ones ig
                excessTiles.append(max(q))


    # After the for loop
    excessTiles = list(set(excessTiles))
    mid_range_keeps_T = list(set(mid_range_keeps.keys()))


    if mid_range_keeps_T == excessTiles and len(excessTiles):
        # If we get here, it is most likely due to situations like
        # 2 4 5 7, where 2 sets exists, 2-5, 4-7
        worst = min(mid_range_keeps.values())
        dcOptions = []


        for q in mid_range_keeps:
            if mid_range_keeps[q] == worst:
                dcOptions.append(q)

        if return_all:
            return dcOptions
        
        return random.choice(dcOptions)
    # else
    excessTiles = listsXOR(excessTiles, mid_range_keeps)
    # Return random excess tile if it exist    
    if len(excessTiles):
        if return_all:
            return excessTiles
        return random.choice(excessTiles)

    
    # If the program survivens until here, we have:
    # No triplets, no extra number tiles, and probably a bunch of lucky tiles
    # If we still aint winning, we probably have a few excess pairs
    # Select all tiles that appear more than once with XOR function
    excessTiles = listsXOR(inner_hand, list(set(inner_hand)), remove_all=False)
    if len(excessTiles) == 0:
        print(inner_hand)
    # and we return a random excess pair
    if return_all:
            return excessTiles
    return random.choice(excessTiles)


            
if __name__ == '__main__':
    # Testing example
    # Test for getunit_suits
    # splitTest = split_suits([11, 14, 17, 25 ,26, 27, 33, 35, 36, 45, 45])
    # print(f'getunitTest = {splitTest}')

    # # buddha_suitCompleteness
    # completenessTest = buddha_suitCompleteness([11 + i for i in range(9)])
    # print(f'completenessTest = {completenessTest}')

    hand = [12, 16, 19, 22, 24, 25, 27, 33, 36, 39, 41, 42, 43, 45, 45, 46, 47]

    print(len(hand))
    print(buddha_findBestDiscard(hand, [28, 28, 28, 28, 29, 29, 29], return_all=True))
import sys
sys.path.append('P:/mjc-main/mjcpy')

from listUtils import * # type: ignore

def removelt(list1: list, threshold=40):
    filtered_list = filter(lambda x: x <threshold, list1)
    removed_items = filter(lambda x: x > threshold, list1)

    return list(filtered_list), list(removed_items)


def hand_eval(inner_hand, outer_hand, priority='str'):
    # Evaluates the current situation of the hand
    # Returns completed sets and half completed sets

    # takes in the inner_hand with the drawn tile
    inner_hand_wk = inner_hand.copy()

    if priority == 'str':
        # remove lt
        inner_hand_wk, LT = removelt(inner_hand_wk)
        straights, remTiles = straightsplit(inner_hand_wk) # type: ignore
        triplets, remTiles = tripletsplit(remTiles + LT) # type: ignore # type: ignore

        numCompletedSets = (len(straights) + len(triplets)) / 3

        # Finds partial sets for the remaining tiles
        # open ended straight
        remTiles.sort()
        openStraights = []
        edgeStraights = []
        g = 0
        while g < len(remTiles):
            if ((remTiles[g] + 1) in remTiles and remTiles[g]<40):
                # remTile[g] + 2 cannot be in remTiles or else it will have been extracted as a straight
                t = remTiles[g]
                if (t % 10 in [1,8]):
                    # edgeStraights.append(list([t, t+1]))
                    g = g + 1 
                    continue
                    # reserve for later
                else:
                    remTiles.remove(t)
                    remTiles.remove(t+1)
                    openStraights.append(list([t, t+1]))
                g = 0

            else:
                g = g + 1
        
        # pair!
        pairs = []
        g = 0
        while g < len(remTiles):
            if remTiles.count(remTiles[g]) == 2: 
                # suppose should not be more than 3 or else it gets identified as a triplet
                t = remTiles[g]
                pairs.append(list([t, t]))
                remTiles.remove(t)
                remTiles.remove(t)
                g = 0
            
            else:
                g = g + 1

        # ka long (middle)
        kalong = []
        g = 0
        while g < len(remTiles):
            if (remTiles[g] + 2) in remTiles and remTiles[g] < 40:
                t = remTiles[g]
                if int((t+2)/10) == int(t/10):
                    kalong.append(list([t, t+2]))
                    remTiles.remove(t)
                    remTiles.remove(t+2)
                    g = 0
                else:
                    g = g + 1
                    continue
                
            else:
                g = g + 1

        # Edge straights
        g = 0
        while g < len(remTiles):
            if ((remTiles[g] + 1) in remTiles and remTiles[g]<40):
                # remTile[g] + 2 cannot be in remTiles or else it will have been extracted as a straight
                t = remTiles[g]
                remTiles.remove(t)
                remTiles.remove(t+1)

                if (t % 10 in [1,8]):
                    edgeStraights.append(list([t, t+1]))
                    g = 0
                else:
                    pass

            else:
                g = g + 1

        partialSets = [openStraights , pairs , kalong, edgeStraights]
        partialSetsScore = len(openStraights) * 0.5 + len(pairs) * 0.5 + len(kalong) * 0.25 + len(edgeStraights) * 0.25

        # Assuming all outside sets are already complete to save time
        outside_score = 2 * int(len(outer_hand) / 3)

        fullScore = partialSetsScore + numCompletedSets * 2 + outside_score

        return fullScore, partialSets, remTiles
    

    else:

        triplets, remTiles = tripletsplit(inner_hand_wk) # type: ignore
        # remove lt
        remTiles, LT = removelt(remTiles)
        straights, remTiles = straightsplit(remTiles) # type: ignore

        numCompletedSets = (len(straights) + len(triplets)) / 3

        # Finds partial sets for the remaining tiles

        # pair!
        pairs = []
        g = 0
        while g < len(remTiles):
            if remTiles.count(remTiles[g]) == 2: 
                # suppose should not be more than 3 or else it gets identified as a triplet
                t = remTiles[g]
                pairs.append(list([t, t]))
                remTiles.remove(t)
                remTiles.remove(t)
                g = 0
            
            else:
                g = g + 1

        # open ended straight
        remTiles.sort()
        openStraights = []
        edgeStraights = []
        g = 0
        while g < len(remTiles):
            if ((remTiles[g] + 1) in remTiles and remTiles[g]<40):
                # remTile[g] + 2 cannot be in remTiles or else it will have been extracted as a straight
                t = remTiles[g]
                remTiles.remove(t)
                remTiles.remove(t+1)
                if (t % 10 in [1,8]):
                    edgeStraights.append(list([t, t+1]))
                else:
                    openStraights.append(list([t, t+1]))
                g = 0

            else:
                g = g + 1
        
        

        # ka long (middle)
        kalong = []
        g = 0
        while g < len(remTiles):
            if (remTiles[g] + 2) in remTiles and remTiles[g] < 40:
                t = remTiles[g]
                if int((t+2)/10) == int(t/10):
                    kalong.append(list([t, t+2]))
                    remTiles.remove(t)
                    remTiles.remove(t+2)
                    g = 0
                else:
                    g = g + 1
                    continue
                
            else:
                g = g + 1

        partialSets = [openStraights , pairs , kalong, edgeStraights]
        partialSetsScore = len(openStraights) * 0.5 + len(pairs) * 0.5 + len(kalong) * 0.25 + len(edgeStraights) * 0.25

        # Assuming all outside sets are already complete to save time
        outside_score = 2 * int(len(outer_hand) / 3)

        fullScore = partialSetsScore + numCompletedSets * 2 + outside_score

        return fullScore, partialSets, remTiles

if __name__ == '__main__':
    hand = [11, 12, 13, 14, 15, 15, 16, 17, 18, 18, 33, 33, 33, 35, 36, 37]

    eval = hand_eval(hand, [])

    print(eval)
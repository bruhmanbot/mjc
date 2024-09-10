import sys
sys.path.append('../mjcpy')

from listUtils import * # type: ignore

def countUsefulTiles(partialSets: list, singles:list, knownPile: list):
    # Generates the amt of useful tiles on next draw judging from current partial sets
    # and info available in the known pile of tiles

    # Partial sets follow the format in a nested list
    # partialset = [openstraights, pairs, kalongs, edgestraights]

    useful_tiles = []
    useful_tiles_weighted = []

    for ps in partialSets[0]:
        # ps = [34, 35], as e.g.
        # first considering the open straights
        useful_tiles.append(ps[0] - 1)
        useful_tiles.append(ps[1] + 1)
        # Appending the end and starting numbers

    for ps in partialSets[1]:
        # pairs
        useful_tiles_weighted.append(ps[1])
        # Adding an extra weight due to pong potentials (~2x)


    for ps in partialSets[2]:
        # kalongs
        useful_tiles.append(ps[0] + 1)

    for ps in partialSets[3]:
        # edge tiles
        if (min(ps) % 10) == 1:
            useful_tiles.append(ps[0] + 2)
            # tile ending with 3
        else:
            useful_tiles.append(ps[0] - 1)
            # tile ending with 7

    # Counting up the useful tiles with respect to knownPile (weighted)
    useful_count = 0
    useful_tiles = list(set(useful_tiles))
    for i in useful_tiles:
        useful_count += 4 * (4 - knownPile.count(i))

    for i in useful_tiles_weighted:
        useful_count += 8 * (4 - knownPile.count(i))

    for s in singles:
        if s > 40:
            # only pairs for LT
            useful_count += 4 - knownPile.count(s)
            useful_tiles.append(s)
            continue
        else:
            # Pair and straights
            useful_tiles.append(s)
            useful_count += 4 - knownPile.count(i)
            if s%10 != 9:
                useful_tiles.append(s+1)
                useful_count += 4 - knownPile.count(s+1)
            if s%10 != 1:
                useful_tiles.append(s-1)
                useful_count += 4 - knownPile.count(s-1)
            
            # Kalongs

            if int((s-2)/10) == int(s/10):
                useful_tiles.append(s-2)
                useful_count += (1/2) * (4 - knownPile.count(s-2))

            if int((s+2)/10) == int(s/10):
                useful_count += (1/2) * (4 - knownPile.count(s+2))
                useful_tiles.append(s+2)

    return useful_count, (useful_tiles_weighted + useful_tiles)

def usefulness_ps(partialSets: list, knownPile: list):
    # Partial sets follow the format in a nested list
    # partialset = [openstraights, pairs, kalongs, edgestraights]
    # outputs to a dictionary
    # {[28, 29]: 2, [34, 35]: 6} etc.
    outputdict = {}

    # Open ended straights, appends num of useful tiles to a dictionary
    for ps in partialSets[0]:
        outputdict[tuple(ps)] = (4 - knownPile.count(ps[0] - 1)) + (4 - knownPile.count(ps[0] + 2))

    # Pairs
    for ps in partialSets[1]:
        outputdict[tuple(ps)] = (4 - knownPile.count(ps[0])) * 2 # 2 factor due to pongs
        # Pairs are rarely discarded so long as they are alive

    # kalongs
    for ps in partialSets[2]:
        outputdict[tuple(ps)] = (4 - knownPile.count(ps[0] + 1))

    # edges
    for ps in partialSets[3]:
        if (min(ps) % 10) == 1:
            outputdict[tuple(ps)] = (4 - knownPile.count(ps[0] + 2))
            continue

        else:
            outputdict[tuple(ps)] = (4 - knownPile.count(ps[0] - 1))

    return outputdict

def usefulness_ss(singles:list, knownPile: list):
    ssdict = {}
    for s in singles:

        if s > 40:
            # only pairs for LT
            ssdict[s] = 4 - knownPile.count(s)
            continue
        else:
            # Pair and straights
            ssdict[s] = 4 - knownPile.count(s)
            if s%10 != 9:
                ssdict[s] += 4 - knownPile.count(s+1)
            if s%10 != 1:
                ssdict[s] += 4 - knownPile.count(s-1)
            
            # Kalongs

            if int((s-2)/10) == int(s/10):
                ssdict[s] += (4 - knownPile.count(s-2)) * 0.5

            if int((s+2)/10) == int(s/10):
                ssdict[s] += (4 - knownPile.count(s+2)) * 0.5

    return ssdict

def sortdict(dictionary: dict):
    # sorts the dictionary wrt the score on the RHS
    sortedDict = sorted(dictionary.items(), key= lambda x: x[1])
    return sortedDict


if __name__ == '__main__':
    known = []

    partial = [[[32, 33]], [[35,35]], [], [[28, 29]]]

    singles = [41, 44]

    j = usefulness_ps(partial, known)
    print(j)
    k = usefulness_ss(singles, known)
    print(k)
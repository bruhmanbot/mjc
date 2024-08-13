def split_list(lst, chunk_size):
    chunks = []
    for ds in range(0, len(lst), chunk_size):
        chunk = lst[ds:ds + chunk_size]
        chunks.append(chunk)
    return chunks


def same_set(item1, item2):
    if int(item1 / 10) == int(item2 / 10):
        return True
    else:
        return False


def set_containslists(items, set_search):
    # Considers the things in a list 'items' and checks if all of the things are in set_search
    for thing in items:
        if not (thing in set_search):
            return False
    return True


def unique_occurence_count(list):
    # Counts the uniqure occurence of each item inside a list and returns them in a list
    # e.g. count number of times each item appears in list [1, 2, 3, 2, 1]
    # >> uniqure_occurence_count(list)
    # Returns [2, 2, 1]
    # Order solely dependent on how the items are originally order in the list

    # Identify unique items
    UniqueList = []
    item_count = []
    for i in list:
        if not (i in UniqueList):
            UniqueList.append(i)

    # Count occurences
    for m in UniqueList:
        item_count.append(list.count(m))

    return item_count


def find_occurence(list_search, occurence) -> list:
    # Finds the elements in a list which have appeared n amount of times
    # and outputs them in a list
    output_list = []
    for i in list_search:
        if list_search.count(i) == occurence and not (i in output_list):
            output_list.append(i)
    return output_list


def find_index_duplicate_item(item, list_to_search):
    # returns the i of duplicate items in a list
    index_search = 0
    item_index_list = []
    while True:
        try:
            location = list_to_search.index(item, index_search)
        except ValueError:
            break
        else:
            item_index_list.append(location)
            index_search = location + 1

    return item_index_list


def find_arithmetic_seq(start, list_search, interval):
    # find the number of elements in an AS with the interval, starting at some point
    # within the items in a list and returns the AS
    # e.g. [1, 2, 3, 4, 6, 9, 11, 5] find the longest AS starting at 1
    # return [1, 2, 3, 4, 5, 6]
    next_term_exists = True
    AS_output = [start]
    while next_term_exists:
        if (start + interval) in list_search:
            AS_output.append(start + interval)
            start = start + interval
        else:
            next_term_exists = False

    return AS_output


def listtypecheck(list1, type1):
    for i in list1:
        if type(i) is type1:
            continue
        else:
            return 0
    return 1


def straightsplit(list2):
    # Identifies straights in a list and returns the straights in kan and the remaining items in list2
    kan = []
    list2.sort()
    k = 0
    while k < len(list2):
        if (list2[k] + 1) in list2 and (list2[k] + 2) in list2:
            StraightStart = list2[k]
            for m in range(3):
                kan.append(StraightStart + m)
                list2.remove(StraightStart + m)
            k = 0
        else:
            k = k + 1

    return kan, list2


def tripletsplit(list2):
    # Finds and identifies triplets in a list and returns the triplets in kan, the remaining items in list2
    kan = []
    i = 0
    while i < len(list2):
        if list2.count(list2[i]) >= 3:
            tripletNumber = list2[i]
            for m in range(3):
                kan.append(tripletNumber)
                list2.remove(tripletNumber)
            i = 0
        else:
            i = i + 1
    return [kan, list2]


def element_appeared_n_times_find(list2, n):
    # Find all possible eyes and puts them into a list
    eye = []
    for i in list2:
        if list2.count(i) >= n and not (i in eye):
            eye.append(i)
    return eye


def unpack_list(list_unpack: list) -> list:
    # Unpacks a list containing nested lists
    # e.g. [[1,2,3] , [4,5,6]] --> [1,2,3,4,5,6]
    output_list = []
    for nested_list in list_unpack:
        output_list = output_list + nested_list
    return output_list

def list_XOR(list_ref:list, list_remove:list, remove_all=False) -> list:
    # Considers the items in list_remove and removes them from list_ref
    # Removes all if True, removes only 1 instance if false
    # Returns the modified list_ref
    list_ref_wk = list_ref.copy()
    for t in list_remove:
        if remove_all:
            while list_ref.count(t) > 0:
                list_ref_wk.remove(t)
        elif t in list_ref_wk:
            # Remove only 1 instance when remove_all = False
            list_ref_wk.remove(t)
        else: 
            return "not a subset"

    return list_ref_wk

def swap(list_swap: list, ind_a: int, ind_b: int):
    # sub function for swapping elements in list
    t = list_swap[ind_a]
    list_swap[ind_a] = list_swap[ind_b]
    list_swap[ind_b] = t
    return

def sort_straights(list_straights: list[list[int]]) -> None:
    # sorts the nest lists of the straights based on a (revised) bubblesort approach

    while True:
        swapped = False
        j = 1
        while j <= (len(list_straights) - 1):

            if list_straights[j][0] < list_straights[j-1][0]:
                # Swap if incorrect
                swap(list_straights, j, j-1)
                swapped = True
            j = j + 1

        if not swapped:
            break

    return

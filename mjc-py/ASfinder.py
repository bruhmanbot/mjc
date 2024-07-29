def find_arithmetic_seq(start, list_search, interval):
    # find the number of elements in an AS with the interval, starting at some point
    # within the items in a list and returns the AS
    # e.g. [1, 2, 3, 4, 6, 9, 11, 5] find the longest AS starting at 1
    # return [1, 2, 3, 4, 5, 6]
    next_term_exists = True
    AS_output = [start]
    while next_term_exists:
        if (start + interval) in list_search:
            AS_output.append(start+interval)
            start = start + interval
        else:
            next_term_exists = False

    return AS_output



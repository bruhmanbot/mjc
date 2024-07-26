from accoladeClassinit import accoladecsv_init
from listUtils import set_containslists
# computes the flower(s)
# return flowerScore and accolade for flowers!

def flower_count(flower:list, seat, accID=accoladecsv_init()):
    output_acc = []
    flowerScore = 0
    # flowers
   
    if len(flower) == 0:
        # No flower case
        output_acc = f'{accID[0].acco_name} - {accID[0].pts}'
        flowerScore = accID[0].pts
        return flowerScore, output_acc
    
    # If there are flowers
    flower_work = flower.copy()
    # Make a copy for the working list

    # Amount of points a set of flowers would normally get when counted seperately
    set_deduction = 3 * accID[1].pts + accID[2].pts

    if set_containslists([k + 1 for k in range(8)], flower):  # All 8 flowers
        output_acc = f'{accID[4].name} - {accID[4].pts}'
        flowerScore = accID[4].pts
        return flowerScore, output_acc

    flower_work.sort()

    if set_containslists([1, 2, 3, 4], flower):  # One whole collection
        flowerScore = flowerScore + accID[3].pts
        # One set of flowers = 10 pts (but not counting individual pts)
        for i in range(4):
            flower_work.pop(0)
        # Remove first 4 elements (1,2,3,4) after sorting

    if set_containslists([5, 6, 7, 8], flower):  # One whole collection
        flowerScore = flowerScore + accID[3].pts
        # One set of flowers = 10 pts (but not counting individual pts)
        for i in range(4):
            flower_work.pop()
        # Removes last 4 elements (5,6,7,8) after sorting
        

    for i in flower_work:
        if i % 4 == seat % 4:
            flowerScore = flowerScore + accID[2].pts  # Matching flowers
        else:
            flowerScore = flowerScore + accID[1].pts  # Non-Matching flowers

    # Returning string and flowerScore
    output_acc = f'Flowers - {flowerScore}'

    return flowerScore, output_acc
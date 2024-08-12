from drawing_game import deckInit
from player_class import gambler
import random

def update_public_domain(*gamers: gambler) -> list:
    global discards
    new_domain = discards # + other outer hands

    for g in gamers:
        new_domain = new_domain + g.outer_hand

    return new_domain


if __name__ == '__main__':
    # gamers
    me = gambler('me')
    ai = gambler('ai')
    # global vars
    me.inner_hand = [12, 13, 14, 15, 16, 41, 41, 32, 33, 34]
    me.outer_hand = [43, 43, 43]
    ai.inner_hand = [21, 22, 23, 24, 25, 26, 27, 28, 22, 22]
    ai.outer_hand = [46, 46, 46]

    me.evalhand()
    ai.evalhand()

    # Input discard tiles for UpTest
    discards = []
    public_domain = update_public_domain(me, ai)
    m = input('First discard?')
    discards.append(int(m))
    print(me)
    print(me.hand_score)
    print(f'should i up? {me.determine_up(discards, public_domain)}')

    m = input('second discard?')
    discards.append(int(m))
    print(ai)
    print(f'Shoul AI up? {ai.determine_up(discards, public_domain)}')


        

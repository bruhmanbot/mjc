from drawing_game import *
from liguStrats import findOptimalDiscardLigu
from optimalDiscard import findOptimalDiscard, getRandomUselessTile
from buddhastrats import buddha_findBestDiscard
from hand_situation import hand_eval, hand_eval_adv
from check_calling import *
from usefulTiles import *


class gambler:

    def __init__(self, id_input, skill_level:int) -> None:
        # start up the variables that we will use
        
        self.inner_hand: list[int] = []
        self.outer_hand: list[int] = []
        self.flowers: list[int] = []
        self.partial_sets: list[list] = []
        self.hand_score: float = 0.0
        # calling: list of tiles that win!
        self.calling: list[int] = []
        self.playerID: str = id_input
        self.skill: bool = bool(skill_level)


    def __str__(self) -> str:
        return f'Gambler ID: {self.playerID}, with hand:\n{self.inner_hand} || {self.outer_hand}'


    def init_draw(self, deck:list, hand_len=16) -> list:
        # original draw of 16 tiles
        self.inner_hand, out_deck = draw(1, hand_len, deck)
        result_hand = filter(lambda x: x > 10, self.inner_hand)
        result_flowers = filter(lambda x: x < 10, self.inner_hand)

        self.inner_hand = list(result_hand)
        self.flowers = list(result_flowers)

        # Flowers
        while len(self.inner_hand) != hand_len:
            player_drawnTiles, out_deck = draw(-1, 16-len(self.inner_hand), out_deck)
            self.inner_hand = self.inner_hand + list(filter(lambda x: x>10, player_drawnTiles))
            self.flowers = self.flowers + list(filter(lambda x: x<10, player_drawnTiles))
        # Repeatedly gets flowers until main hand == 16 tiles

        self.inner_hand.sort()
        self.flowers.sort()

        # update the outer deck
        deck[:] = out_deck

        return
    
    def evalhand(self) -> None:
        # Differentiate the modes --> Save time if full_mode is not ran
        if self.skill:
            self.hand_score, self.partial_sets, temp = hand_eval_adv(self.inner_hand, self.outer_hand)
        else:
            self.hand_score, self.partial_sets, temp = hand_eval(self.inner_hand, self.outer_hand, priority='str')

        # Update calling tiles:
        if self.hand_score >= 7.5:
            callers = check_calling_tiles(self.inner_hand, self.outer_hand, output_score=False)
            self.calling = list(callers.keys())

        elif self.hand_score <= 0.5:
            # buddha
            callers = check_calling_tiles_bd(self.inner_hand, self.outer_hand, output_score=False)
            self.calling = self.calling + list(callers.keys())

        # Always check ligu bcz i dont know a quick way to exclude it
        callers = check_calling_tiles_ligu(self.inner_hand, self.outer_hand, output_score=False)
        self.calling = self.calling + list(callers.keys())

        return

    def draw(self, deck:list) -> None:
        # Draws from the deck
        self.inner_hand, self.flowers, out_deck = playerdraw(self.inner_hand, self.flowers, deck)
        self.flowers.sort()
        # update the outer deck
        deck[:] = out_deck
        return

    def disc(self, tile:int, discard:list, known_pile:list) -> None:
        discard.append(tile)
        known_pile.append(tile)
        self.inner_hand.remove(tile)
        self.inner_hand.sort()
        return
    
    def playturn(self, deck: list, discard:list, known_pile:list, hand_goal='normal') -> str:
        # Plays the turn of the player
        # Draws a tile from the deck first
        self.draw(deck)
        # Player hand and flowers are automatically updated
        # known pile updated here as well

        # Returns a string to see if you win!

        # see if won
        if self.inner_hand[-1] in self.calling:
            return 'winners! by sumo!'

        match hand_goal:
            case 'normal':
                discardTile = findOptimalDiscard(self.inner_hand, known_pile + self.inner_hand, full_eval_mode=self.skill)
            case 'buddha':
                discardTile = buddha_findBestDiscard(self.inner_hand, known_pile + self.inner_hand)
            case 'ligu':
                discardTile = findOptimalDiscardLigu(self.inner_hand, known_pile + self.inner_hand)
            case _:
                discardTile = findOptimalDiscard(self.inner_hand, known_pile + self.inner_hand)
                # Failsafe

        self.disc(discardTile, discard, known_pile)


        # Re-eval hand
        self.evalhand()
        # Return empty string if not won
        return ''

    
    def up(self, partial:list[int], discard:list, known_pile:list) -> None:
        # Commiting up (chow) on the previous discard tile
        fullSet:list = partial + discard[-1:]
        fullSet.sort()
        # pop from the discard to simulate what actually happens in the middle
        discard.pop(-1)
        # Adds the full set to the outer hand
        self.outer_hand[:] = self.outer_hand + fullSet
        
        # Update the publicly known knownPile with the full set
        known_pile[:] = known_pile + fullSet

        # Remove the tiles from inner hand
        for q in partial:
            self.inner_hand.remove(q)

        if self.playerID == 'me':
            print(self)
            discardTile = askdiscard(self.inner_hand)
        else:
            discardTile = findOptimalDiscard(self.inner_hand, known_pile + self.inner_hand, full_eval_mode=self.skill)

        self.disc(discardTile, discard, known_pile)
            
        # Re-eval hand
        self.evalhand()

        return
    
    def determine_up(self, discard:list, known_pile:list) -> list:
        # Returns the best possible partial set to up with
        # possible partial sets, partial sets which need to be a subset 
        # in order for upping to be possible
        up_feasible=False
        ps = []
        # Tile in question
        tile = discard[-1]
        if discard[-1] > 40:
            # bruh
            return []
        if (tile - 1 in self.inner_hand) and (tile + 1 in self.inner_hand):
            # Check for kalong case
            up_feasible = True
            ps.append([tile - 1, tile + 1])
        if (tile + 1 in self.inner_hand) and (tile + 2 in self.inner_hand):
            up_feasible = True
            ps.append([tile + 1, tile + 2])
        
        if (tile - 1 in self.inner_hand) and (tile - 2 in self.inner_hand):
            up_feasible = True
            ps.append([tile - 1, tile - 2])

        # Exit if up is not feasible
        if up_feasible == False:
            return []
               
        
        # Determine whether it is worth it to up
        comp_dict = {}
        for method in ps:
            innerHandAfterUp = self.inner_hand.copy()
            outerHandAfterUp = self.outer_hand.copy() + [tile]
            
            for pt in method:
                innerHandAfterUp.remove(pt)
                outerHandAfterUp.append(pt)
            
            nextDiscard: int = findOptimalDiscard(innerHandAfterUp, outerHandAfterUp, full_eval_mode=self.skill)
            innerHandAfterUp.remove(nextDiscard)
            if self.skill:
                eval_afterUp = hand_eval_adv(innerHandAfterUp, outerHandAfterUp)
            else:
                eval_afterUp = hand_eval(innerHandAfterUp, outerHandAfterUp)

            # Assign score for each method
            comp_dict[tuple(method)] = eval_afterUp[0]

        # If after upping, gives no significant benefit
        if max(comp_dict.values()) <= self.hand_score:
            # Does not up
            return []
        
        # Extracting the best ways to up
        best_ps = []
        for method in comp_dict:
            if comp_dict[method] == max(comp_dict.values()):
                best_ps.append(method)

        # In the case where only 1 method prevails
        if len(best_ps) == 1:
            return best_ps[0]
        
        # packaging best_ps to pass into the usefulness_ps function
        # The remaining empty sections are for pairs
        best_ps_f = [[], [], [], []]
        for ps in best_ps:
            # ps: tuple
            if max(ps) == min(ps) + 1:
            # open end // edge straight
                if min(ps) in [1,8]:
                    # Add to edge staights
                    best_ps_f[3].append(ps)
                else:
                    # add to open ended straights
                    best_ps_f[0].append(ps)
            else:
                # Add to kalogs
                best_ps_f[2].append(ps)
        # Multiple methods prevail (at most 3)
        # Choose the (random) partial set with the least amt of useful tiles (cuz its hard to come by)
        best_ps_dict = usefulness_ps(best_ps_f, knownPile=known_pile)

        # The getRandomUselessTile function outputs the key of the dict, which is a tuple
        # Convert back into list
        output = list(getRandomUselessTile(best_ps_dict))
        output.sort()
        return output
          
    
    def pong(self, pair:list, discard:list, known_pile:list) -> None:
        # Commiting pong on the previous discard tile
        fullSet:list = pair + discard[-1:]
        fullSet.sort()

        # pop from the discard to simulate what actually happens in the middle
        discard.pop(-1)

        # Adds the full set to the outer hand
        self.outer_hand = self.outer_hand + fullSet

        # Update the publicly known knownPile with the pair (last tile already included in previous discard)
        known_pile[:] = known_pile + pair

        # Remove the tiles (pair) from inner hand
        self.inner_hand.remove(pair[0])
        self.inner_hand.remove(pair[0])
        

        if self.playerID == 'me':
            print(self)
            discardTile = askdiscard(self.inner_hand)
        else:
            discardTile = findOptimalDiscard(self.inner_hand, known_pile + self.inner_hand, full_eval_mode=self.skill)

        self.disc(discardTile, discard, known_pile)

        # Re-eval hand
        self.evalhand()

        return
    
    def determine_pong(self, discard:list, known_pile:list) -> list:
        # Returns whether you should ponggers
        # Flow: See if can pong --> See if score increases after pong + discard
        # Pong tile in question
        tile = discard[-1]
        if self.inner_hand.count(tile) < 2:
            return []
        
        # Simulate the inner and outer hands

        innerHandAfterPong = self.inner_hand.copy()
        outerHandAfterPong = self.outer_hand.copy()

        # Simulate moving the tiles
        innerHandAfterPong.remove(tile)
        innerHandAfterPong.remove(tile)
        outerHandAfterPong = outerHandAfterPong + [tile] * 3

        # Finding the best discard tile

        nextDiscard = findOptimalDiscard(innerHandAfterPong, known_pile, full_eval_mode=self.skill)
        innerHandAfterPong.remove(nextDiscard)

        if self.skill:
            eval_afterPong = hand_eval_adv(innerHandAfterPong, outerHandAfterPong)
        else:
            eval_afterPong = hand_eval(innerHandAfterPong, outerHandAfterPong)

        # Returns empty list (no pongs) if no benefits
        if eval_afterPong[0] == self.hand_score:
            return []
        
        return [tile] * 2
    
    def gong(self, tile, discards:list, known_pile:list) -> None:
        # Gongs and updates the known_pile (public domain)
        if self.inner_hand.count(tile) == 3:
            # open gong
            if discards[-1] == tile:
                # Remove the 3 tiles and add them to outer hand
                # Here a gong is considered a pong for the player because its easier to evaluate
                for q in range(3):
                    self.inner_hand.remove(tile)
                    self.outer_hand.append(tile)
                    known_pile.append(tile)
                # Add the final time
                known_pile.append(tile)



if __name__ == '__main__':
    # Set up a test game
    # initialise the gamblers
    me = gambler('me', 1)

    me.inner_hand = [11, 11, 11, 12, 13, 17, 18, 19, 21, 22, 23, 28, 28, 32, 33, 34]
    me.outer_hand = []

    me.evalhand()

    print(me.calling)



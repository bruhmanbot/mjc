from drawing_game import draw, playerdraw, askdiscard
from liguStrats import findOptimalDiscardLigu
from optimalDiscard import findOptimalDiscard, getRandomUselessTile
from buddhastrats import buddha_findBestDiscard
from hand_situation import hand_eval, hand_eval_adv
from check_calling import check_calling_tiles, check_calling_tiles_bd, check_calling_tiles_ligu
from usefulTiles import usefulness_ps
from dynamic_playstyle import findOptimalDiscard_dynamic
import sys

sys.path.append('../mjcpy')

from listUtils import find_occurence # type: ignore
from MJCounter import mj_scorecount # type: ignore

class gambler:

    def __init__(self, id_input, player_profile:dict =None) -> None:
        # start up the variables that we will use
        
        self.inner_hand: list[int] = []
        self.outer_hand: list[int] = []
        self.flowers: list[int] = []
        self.partial_sets: list[list] = []
        self.hand_score: float = -1.0
        # calling: list of tiles that win!
        self.calling: list[int] = []
        self.playerID: str = id_input
        # Construct player profile (configure playstyle)
        # Below is the deault profile (as an example)
        self.profile = {
<<<<<<< HEAD
            "skill": 1, # Must be an integer (for now)
=======
            "skill": 0, # Defined skillset with a string
>>>>>>> bd021757faba91682694bdcbbbc6d350f4c13939
            
            # dictionary to represent {startingPairs: Max Starting Score to proceed}
            # Note that generally for high scoring hands it is better to go for the normal route --> Specify the max that the bot
            # will sacrifice speed for ligu. Of course if you want a bot that goes for ligu 100%, set the max to like -1.
            # If score is not listed --> Go for normal hand
            "liguThreshold": {
                0: -1, # Never go for ligu
                1: 0.5, # Go for ligu if only 1 pair (but realistically for this situation you should go for buddha anyways)
                2: -1, # No favourable situation
                3: -1,
                4: 2.75,
                5: 4.5,
                6: 6.25,
                7: 10, # Always go for ligu
                8: 14,
            },

            # Same thing as above but for buddha {startingLT: MaxScore to proceed}
            "bdThreshold": {
                0: -1, # literally why would you go for it
                1: -1,
                2: -1,
                3: -1,
                4: -1,
                5: 1.75,
                6: 2.75,
                7: 4 # I mean come on of course you are going to go for it under most cases
            },

            # Default goal for hand
            "goal": "normal",

            # Mode
            "mode": 0

        }

        # Overwrite self.profile if entered something
        try:
            player_profile.values()
            for q in player_profile:
                self.profile[q] = player_profile[q]

        except AttributeError:
            pass


        # Backwards compatibility with code below, will update later
        self.skill: bool = bool(self.profile["skill"])

        


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
    
    def evalhand(self, tileDeck = []) -> None:
        # Differentiate the modes --> Save time if full_mode is not ran
        # if self.profile["skill"]:
        #     self.hand_score, self.partial_sets, temp = hand_eval_adv(self.inner_hand, self.outer_hand)
        # else:
            
        
        # Dynamic mode
        if self.profile["skill"] == 'dynamic':
            self.hand_score, self.partial_sets, temp = hand_eval_adv(self.inner_hand, self.outer_hand)      
    
        else:
            self.hand_score, self.partial_sets, temp = hand_eval(self.inner_hand, self.outer_hand, priority='str')

        # Update calling tiles:
        self.calling = []
        if self.hand_score >= 8.5:
            callers = check_calling_tiles(self.inner_hand, self.outer_hand, output_score=False)
            self.calling = list(callers.keys())
    
        elif self.hand_score <= 0.5:
            # buddha
            callers = check_calling_tiles_bd(self.inner_hand, self.outer_hand, output_score=False)
            self.calling = self.calling + list(callers.keys())

        # Always check ligu bcz i dont know a quick way to exclude it
        callers = check_calling_tiles_ligu(self.inner_hand, self.outer_hand, output_score=False)
        self.calling = self.calling + list(callers.keys())

        if self.profile['skill'] != 'dynamic':
            return
        
        
        # Dynamics only

        # print(f'Game Prog: {game_progession}')
        if len(tileDeck) < 12:
            self.profile['mode'] = 3
        elif len(tileDeck) < 32:
            self.profile['mode'] = 2
        # elif len(tileDeck) < 48 and self.hand_score < 8.0:
        #     self.profile['mode'] = 2
        # elif len(tileDeck) < 62 and self.hand_score < 5.0:
        #     self.profile['mode'] = 1
        else:
            self.profile['mode'] = 0
        return

    def determine_goal(self) -> None:
        # Determines the goal for the player
        if len(self.inner_hand) == 0:
            return "Failed to determine starting goal: Did you initialise the draw?"
        elif self.hand_score == -1.0:
            return "Failed to determine starting goal: Did you evaluate your hand?\n call {object}.evalhand() before running this function"
        
        if self.profile["skill"] == 'dynamic':
            # Dont change goal if skillset is dynamic
            return
        
        # By default the goal is "normal" see self.profile dictionary default values
        if len(self.outer_hand) > 0:
            self.profile["goal"] = "normal"
            return
        
        startingLT = list(filter(lambda x: x>40, self.inner_hand))
        numStartingLT:int = len(set(startingLT))

        if self.hand_score <= self.profile["bdThreshold"][numStartingLT]:
            self.profile["goal"] = "buddha"
            return
        
        init_pairs = find_occurence(self.inner_hand, 2)
        init_trips = find_occurence(self.inner_hand, 3)
        init_quads = find_occurence(self.inner_hand, 4)
        init_pc: int = len(init_pairs) + len(init_trips) + 2*len(init_quads)

        # Check if hand score is smaller or equal to MAX threshold laid out
        if self.hand_score <= self.profile["liguThreshold"][init_pc]:
            self.profile["goal"] = "ligu"
            return
        
    def checkLT_availability(self, known_pile:list) -> None:
        # Checks if any LT is dead (all 4 gonzo)
        for i in range(41,48):
            if known_pile.count(i) == 4:
                self.profile["goal"] = "normal"
                break
        
        return

    def draw(self, deck:list) -> None:
        # Draws from the deck
        self.inner_hand, self.flowers, out_deck = playerdraw(self.inner_hand, self.flowers, deck)
        # playerdraw adds a string if deck runs of tiles

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
    
    def playturn(self, deck: list, discard:list, known_pile:list, **kwargs) -> list:
        # Plays the turn of the player
        # Draws a tile from the deck first
        self.draw(deck)

        if type(self.inner_hand[-1]) is str:
            # Last tile of inner_hand is 'DRAW' (str) if the deck runs out of tiles
            # Exception occured with no tiles remaining
            return []
            # Forces the game to proceed to next round and exit via draw
        # Player hand and flowers are automatically updated
        # known pile updated here as well

        # Returns a string to see if you win!

        # see if won
        if self.inner_hand[-1] in self.calling:
            winningTile = self.inner_hand[-1]
            self.inner_hand.pop(-1)
            
            return self.score_count(winningTile, self_drawn=1)

        if self.profile["goal"] == "buddha":
            # Set goal to normal is buddha is no longer possible
            self.checkLT_availability(known_pile)
            
        # Model depends on the goal
        match self.profile["goal"]:
            case 'normal':
                if self.profile["skill"] == "dynamic":
                    try:
                        CDF = kwargs["CDF_gamma"]
                    except KeyError:
                        CDF = []
                    discardTile = findOptimalDiscard_dynamic(self.profile['mode'], self.inner_hand, self.outer_hand, 
                                                     known_pile, discard, deck, CDF_gamma=CDF)
                else:
                    discardTile = findOptimalDiscard(self.inner_hand, known_pile + self.inner_hand, self.skill)
            case 'buddha':
                discardTile = buddha_findBestDiscard(self.inner_hand, known_pile + self.inner_hand)
            case 'ligu':
                discardTile = findOptimalDiscardLigu(self.inner_hand, known_pile + self.inner_hand)
            case _:
                discardTile = findOptimalDiscard(self.inner_hand, known_pile + self.inner_hand)
                # Failsafe

        self.disc(discardTile, discard, known_pile)


        # Re-eval hand
        self.evalhand(deck)
        # Return empty list if not won
        return []
    

    
    def up(self, partial:list[int], discard:list, known_pile:list, deck=[], **kwargs) -> None:
        # Commiting up (chow) on the previous discard tile
        fullSet:list = partial + discard[-1:]
        fullSet.sort()
        # pop from the discard to simulate what actually happens in the middle
        discard.pop(-1)
        known_pile.pop(-1)
        # Adds the full set to the outer hand
        self.outer_hand[:] = self.outer_hand + fullSet
        
        # Update the publicly known knownPile with the full set
        known_pile[:] = known_pile + fullSet

        # Remove the tiles from inner hand
        for q in partial:
            self.inner_hand.remove(q)

        if self.playerID == 'me':
            try:
                CDF = kwargs['CDF_gamma']
            except KeyError:
                CDF = []
            helper = findOptimalDiscard_dynamic(self.profile['mode'], self.inner_hand, self.outer_hand, 
                                                known_pile, discard, deck, CDF_gamma=CDF)

            print(f'Helper: {helper}')
            print(self)

            discardTile = askdiscard(self.inner_hand)  # noqa: F405
        elif self.profile['skill'] == 'dynamic':
            try:
                CDF = kwargs['CDF_gamma']
            except KeyError:
                CDF = []
            
            discardTile = findOptimalDiscard_dynamic(self.profile['mode'], self.inner_hand, self.outer_hand, 
                                                     known_pile, discard, deck, CDF_gamma=CDF)

            # discardTile = findOptimalDiscard_enhanced(self.inner_hand, self.outer_hand, known_pile, discard, deck, CDF_gamma=CDF)
        else:
            discardTile = findOptimalDiscard(self.inner_hand, known_pile + self.inner_hand, full_eval_mode=self.skill)

        self.disc(discardTile, discard, known_pile)
            
        # Re-eval hand
        self.evalhand(deck)

        return
    
    def determine_up(self, discard:list, known_pile:list) -> list:
        if self.profile["goal"] != "normal":
            return []
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
        if up_feasible is False:
            return []
               
        
        # Determine whether it is worth it to up
        comp_dict = {}
        for method in ps:
            innerHandAfterUp = self.inner_hand.copy()
            outerHandAfterUp = self.outer_hand.copy() + [tile]
            
            for pt in method:
                innerHandAfterUp.remove(pt)
                outerHandAfterUp.append(pt)
            
            nextDiscard = findOptimalDiscard(innerHandAfterUp, outerHandAfterUp, full_eval_mode=self.skill)

            if type(nextDiscard) is str:
                print(self)
                print('Exception happened at line 322 @ determine_UP')
                quit()

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
          
    
    def pong(self, pair:list, discard:list, known_pile:list, deck=[], **kwargs) -> None:
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
            try:
                CDF:list = kwargs['CDF_gamma']
            except KeyError:
                CDF:list = []
                
            helper = findOptimalDiscard_dynamic(self.profile['mode'], self.inner_hand, self.outer_hand, 
                                                     known_pile, discard, deck, CDF_gamma=CDF)

            print(f'Helper: {helper}')
            print(self)
            
            discardTile = askdiscard(self.inner_hand)

        elif self.profile['skill'] == 'dynamic':
            try:
                CDF:list = kwargs['CDF_gamma']
            except KeyError:
                CDF:list = []
            discardTile = findOptimalDiscard_dynamic(self.profile['mode'], self.inner_hand, self.outer_hand, 
                                                     known_pile, discard, deck, CDF_gamma=CDF)
        
        else:
            discardTile = findOptimalDiscard(self.inner_hand, known_pile + self.inner_hand, full_eval_mode=self.skill)

        self.disc(discardTile, discard, known_pile)

        # Re-eval hand
        self.evalhand(deck)

        return
    
    def determine_pong(self, discard:list, known_pile:list) -> list:
        if self.profile["goal"] != "normal":
            return []
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
        if type(nextDiscard) is str:
            print(self)
            print('Exception happened at line 296 @ determine_pong')
            quit()
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
        return
                
    def score_count(self, winningTile, self_drawn=0) -> list:
        # Returns the scores and accolades
        scoreResult = mj_scorecount([winningTile], self.outer_hand, self.inner_hand, self_drawn, 1, 1, self.flowers)
        return list(scoreResult)




if __name__ == '__main__':
    # Set up a test game
    # initialise the gamblers
<<<<<<< HEAD
    me = gambler('a0__ME', {"skill": 1})
    deck = [25, 26, 27]
    pd = []
    disc =[]
    me.inner_hand = [25]
    me.outer_hand = [21, 22, 23, 17, 18, 19, 21, 21, 21, 31, 31, 31, 37, 38, 39]
=======
    me = gambler('me', 1)
    deck = [41, 37]
    discards = [35, 42, 42, 42, 42]
    me.inner_hand = [11, 14, 17, 25, 28, 22, 36, 33, 39, 41, 41, 43, 44, 45, 46, 47]
    me.outer_hand = []
>>>>>>> bd021757faba91682694bdcbbbc6d350f4c13939

    me.evalhand()
    me.determine_goal()

    playturn = me.playturn(deck, disc, pd)

    print(playturn)
    print(me)
    print(me.score_count(25))

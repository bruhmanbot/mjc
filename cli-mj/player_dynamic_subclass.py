from hand_situation import hand_eval_adv
from player_class import gambler
from check_calling import check_calling_tiles, check_calling_tiles_bd, check_calling_tiles_ligu
from dynamic_playstyle import findOptimalDiscard_dynamic
from optimalDiscard_defense import loss_probability
from buddhastrats import buddha_findBestDiscard
from liguStrats import findOptimalDiscardLigu
import pandas as pd

class gambler_dynamic(gambler):

    def __init__(self, id_input, player_profile: dict = None) -> None:
        # Configs the settings in the superclass
        super().__init__(id_input, player_profile)
        # Skillful mode
        self.profile['skill'] = 1

        gamma_dist_LUT = pd.read_csv('./script_data/gamma-dist.csv')
        self.game_progression_CDF: tuple = tuple(gamma_dist_LUT['CDF'])

        # Sets the evaluation mode for the functions
        # 0: Normal (speed); 1: Balanced; 2: Defensive (Quite good); 3: Ultra-defensive (not really good)
        self.eval_mode: int = 0

    def evalhand(self, tileDeck: list[int]) -> None:
        self.hand_score, self.partial_sets, temp = hand_eval_adv(self.inner_hand, self.outer_hand) 

        # Update calling tiles:
        self.calling = []
        if self.hand_score >= 8.5:
            callers = check_calling_tiles(self.inner_hand, self.outer_hand, output_score=False)
            self.calling = list(callers.keys())
    
        elif self.hand_score <= 0.5:
            # buddha
            callers = check_calling_tiles_bd(self.inner_hand, self.outer_hand, output_score=False)
            self.calling = self.calling + list(callers.keys())

        # Ligu only has less than 8 types of tiles [4,8]
        if len(self.outer_hand) == 0:
            callers = check_calling_tiles_ligu(self.inner_hand, self.outer_hand, output_score=False)
            self.calling = self.calling + list(callers.keys())

        # tileDecks , set to defensive mode near the end of the game
        if len(tileDeck) < 20:
            # Indicating defense !
            self.eval_mode = 2
        else:
            self.eval_mode = 0


        return
    
    def playturn(self, deck: list, discard: list, known_pile: list) -> list:
        # Same playturn stuff but uses the dynamic evaluations
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

        match self.profile['goal']:
            case 'buddha':
                if self.eval_mode < 2:
                    dcTile = buddha_findBestDiscard(self.inner_hand, known_pile)

                elif self.eval_mode == 3:
                    dcTile = findOptimalDiscard_dynamic(self.eval_mode, self.inner_hand, self.outer_hand,
                                                    known_pile, discard, deck, CDF_gamma=self.game_progression_CDF)
                    
                else:
                    # Defensive mode (but its somehow a little attacking)
                    dcTileList: list[int] = buddha_findBestDiscard(self.inner_hand, known_pile, return_all=True)

                    min_p:float = 100
                    optimal_dc: float = 0

                    for dc in set(dcTileList):
                        p_loss: float = loss_probability(dc, known_pile, deck, discard, self.game_progression_CDF)
                        if p_loss < min_p:
                            optimal_dc = dc
                            min_p = p_loss

                    dcTile = optimal_dc


            case 'ligu':
                if self.eval_mode < 2:
                    dcTile = findOptimalDiscardLigu(self.inner_hand, known_pile)

                elif self.eval_mode == 3:
                    dcTile = findOptimalDiscard_dynamic(self.eval_mode, self.inner_hand, self.outer_hand,
                                                    known_pile, discard, deck, CDF_gamma=self.game_progression_CDF)
                else:
                    # Defensive mode 2
                    dcTileList: list[int] = findOptimalDiscardLigu(self.inner_hand, known_pile, return_all=True)

                    min_p:float = 100
                    optimal_dc: float = 0

                    for dc in set(dcTileList):
                        p_loss: float = loss_probability(dc, known_pile, deck, discard, self.game_progression_CDF)
                        if p_loss < min_p:
                            optimal_dc = dc
                            min_p = p_loss

                    dcTile = optimal_dc

            # Default mode, includes normal
            case _:
                dcTile = findOptimalDiscard_dynamic(self.eval_mode, self.inner_hand, self.outer_hand,
                                                    known_pile, discard, deck, CDF_gamma=self.game_progression_CDF)
                

        self.disc(dcTile, discard, known_pile)

        # Re-eval hand
        self.evalhand(deck)
        # Return empty list if not won
        return []

    def up(self, partial: list[int], discard: list, known_pile: list, deck: list= []) -> None:

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

        # Can also pass in discardTile to save time
        discardTile = findOptimalDiscard_dynamic(0, self.inner_hand, self.outer_hand,
                                                known_pile, discard, deck, CDF_gamma=self.game_progression_CDF)

        self.disc(discardTile, discard, known_pile)
            
        # Re-eval hand
        self.evalhand(deck)
        return
    
    def determine_up(self, discard: list, known_pile: list, tileDeck:list) -> list:
        bestPS: list[int] = super().determine_up(discard, known_pile)

        if self.eval_mode < 2:
            return bestPS
        
        # Additional evaluation for safety
        # Using the most aggressive algo, or else UPPING would be pretty useless
        new_inner_hand = self.inner_hand.copy()
        new_outer_hand = self.outer_hand.copy()
        for q in bestPS:
            new_inner_hand.remove(q)
            new_outer_hand.append(q)

        new_outer_hand.append(0) # just add an extra tile to give the score


        discardTile: int = findOptimalDiscard_dynamic(0, new_inner_hand, new_outer_hand,
                                                known_pile, discard, tileDeck, CDF_gamma=self.game_progression_CDF)
        
        p_loss: float = loss_probability(discardTile, known_pile, tileDeck, discard, self.game_progression_CDF)

        if p_loss > 0.5:
            return []
        else:
            return bestPS

    
    def pong(self, pair: list, discard: list, known_pile: list, deck: list= []) -> None:
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

        discardTile = findOptimalDiscard_dynamic(0, self.inner_hand, self.outer_hand,
                                                known_pile, discard, deck, CDF_gamma=self.game_progression_CDF)

        self.disc(discardTile, discard, known_pile)

        # Re-eval hand
        self.evalhand(deck)

        return
    
    def determine_pong(self, discard: list, known_pile: list, tileDeck: list) -> list:
        bestPS = super().determine_pong(discard, known_pile)
    
        if self.eval_mode < 2 or bestPS == []:
            return bestPS
        
        # Simulating the new inner hand --> With the pair removed
        
        new_inner_hand = self.inner_hand.copy()
        new_inner_hand.remove(bestPS[0])
        new_inner_hand.remove(bestPS[0])

        # New outer hand
        new_outer_hand = self.outer_hand.copy() + [bestPS[0]] * 3

        # Additional evaluation for safety
        # Using the most aggressive algo, or else UPPING would be pretty useless
        discardTile: int = findOptimalDiscard_dynamic(0, new_inner_hand, new_outer_hand,
                                                known_pile, discard, tileDeck, CDF_gamma=self.game_progression_CDF)
        
        p_loss: float = loss_probability(discardTile, known_pile, tileDeck, discard, self.game_progression_CDF)

        if p_loss > 0.5:
            return []
        else:
            return bestPS



if __name__ == '__main__':
    me = gambler_dynamic('me')

    print(type(me) is gambler_dynamic)
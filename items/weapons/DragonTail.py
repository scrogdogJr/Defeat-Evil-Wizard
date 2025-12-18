from typing import TYPE_CHECKING
from .Weapon import Weapon
import AreaOfEffect

if TYPE_CHECKING:
    from characters import Character

class DragonTail(Weapon):

    def __init__(self):
        super().__init__(range=10, ap_modifier=7)

    def attack(self, attacker: 'Character', defender: 'Character'):
        aof = AreaOfEffect()
        if aof.inRange(self.range, attacker, defender):
            
            defender.max_movement = defender.max_movement * -1

            self.assign_damage(attacker, defender, ap_modifier=self.ap_modifier)
            print(f'{defender} is knocked down and cannot move next turn!')
            return True
        else:
            print(f"{defender.name} is out of range!")
            return False
        
    def print_stats(self):
        super().print_stats()
        print('Special Effect: Knocks down target where they cannot move on their next turn.')
        
    def __str__(self):
        return "Dragon Tail"
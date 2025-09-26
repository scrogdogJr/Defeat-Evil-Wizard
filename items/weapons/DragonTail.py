import Weapon
from characters import Character
import AreaOfEffect

class DragonTail(Weapon):

    aof = AreaOfEffect()

    def __init__(self):
        super().__init__(range=10, ap_modifier=7)

    def attack(self, attacker: Character, defender: Character):
        if self.aof.inRange(self.range, attacker, defender):
            
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
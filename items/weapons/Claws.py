import Weapon
from characters import Character
import AreaOfEffect

class Claws(Weapon):

    aof = AreaOfEffect()

    def __init__(self):
        super().__init__(ap_modifier=5)
    
    def attack(self, attacker: Character, defender: Character):
        if self.aof.isMelee(attacker, defender): 
            self.assign_damage(attacker, defender, ap_modifier=self.ap_modifier)
            return True

        else:
            print(f"{defender.name} is out of range!")
            return False

    def __str__(self):
         return "Claws"
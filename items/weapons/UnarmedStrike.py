import Weapon
from characters import Character
import AreaOfEffect
from craftingMaterials import LadyBug

class UnarmedStrike(Weapon):

    aof = AreaOfEffect()

    # No added modifiers or bonuses
    def __init__(self):
        super().__init__(char='👊', craft_cost={LadyBug: 1})

    def attack(self, attacker: Character, defender: Character):
        if self.aof.isMelee(attacker, defender):
            self.assign_damage(attacker, defender)
            return True

        else:
            print(f"{defender.name} is out of range!")
            return False
    
    def __str__(self):
        return "Unarmed Strike"
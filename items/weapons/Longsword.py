import Weapon
import AreaOfEffect
from craftingMaterials import Stone

class Longsword(Weapon):
    # Setting Attributes
    def __init__(self):
        super().__init__('🗡️ ', craft_cost={Stone: 2}, ap_modifier=15) # This is how the weapon affects the attack and is unique to each weapon

    def attack(self, attacker: Character, defender: Character):
        aof = AreaOfEffect()
        if aof.isMelee(attacker, defender): 

            self.assign_damage(attacker, defender, ap_modifier=self.ap_modifier)
            return True
        else:
            print(f"{defender.name} is out of range!")
            return False

    def __str__(self):
         return "Longsword"
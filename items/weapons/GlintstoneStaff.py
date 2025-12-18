from typing import TYPE_CHECKING
from .Weapon import Weapon

if TYPE_CHECKING:
    from characters import Character

import universal
from items.craftingMaterials.Wood import Wood
from items.craftingMaterials.Gem import Gem
from items.craftingMaterials.Stone import Stone

class GlintstoneStaff(Weapon):

    

    def __init__(self):
        super().__init__(char='🪄 ', craft_cost={Wood: 2, Gem: 1, Stone: 1}, range=14, bonus_damage=10)

    def attack(self, attacker: 'Character', defender: 'Character'):

        aof = universal.AOF

        if aof.inRange(self.range, attacker, defender):
            self.ranged_animation(char='💎', attacker=attacker, defender=defender)
            self.assign_damage(attacker, defender, bonus_damage=self.bonus_damage)
            #TODO: Reduce attack power of the defender
            return True

        else:
            print(f"{defender.name} is out of range!")
            return False
        
    def __str__(self):
        return 'Glintstone Staff'
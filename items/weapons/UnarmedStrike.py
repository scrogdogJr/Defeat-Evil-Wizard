from typing import TYPE_CHECKING
from .Weapon import Weapon
import AreaOfEffect
from items.craftingMaterials import Ladybug

if TYPE_CHECKING:
    from characters import Character

class UnarmedStrike(Weapon):

    # No added modifiers or bonuses
    def __init__(self):
        super().__init__(char='👊', craft_cost={Ladybug: 1})

    def attack(self, attacker: 'Character', defender: 'Character'):
        aof = AreaOfEffect.AreaOfEffect()
        if aof.isMelee(attacker, defender):
            self.assign_damage(attacker, defender)
            return True

        else:
            print(f"{defender.name} is out of range!")
            return False
    
    def __str__(self):
        return "Unarmed Strike"
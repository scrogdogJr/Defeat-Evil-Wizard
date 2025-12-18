from typing import TYPE_CHECKING
from .Weapon import Weapon
import AreaOfEffect

if TYPE_CHECKING:
    from characters import Character

class FireBreath(Weapon):

    def __init__(self):
        super().__init__(range=20, bonus_damage=25)

    def attack(self, attacker: 'Character', defender: 'Character'):
        aof = AreaOfEffect.AreaOfEffect()
        if aof.inRange(self.range, attacker=attacker, defender=defender):
            self.ranged_animation('🔥', attacker=attacker, defender=defender)

            self.assign_damage(attacker, defender, bonus_damage=self.bonus_damage)
            return True

        else:
            print(f"{defender.name} is out of range!")
            return False

    def __str__(self):
         return "Fire Breath"
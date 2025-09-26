import Weapon
from characters import Character
import AreaOfEffect
from craftingMaterials import Wood, Gem, Stone

class GlintstoneStaff(Weapon):

    aof = AreaOfEffect()

    def __init__(self):
        super().__init__(char='🪄 ', craft_cost={Wood: 2, Gem: 1, Stone: 1}, range=14, bonus_damage=10)

    def attack(self, attacker: Character, defender: Character):
        if self.aof.inRange(attacker, defender):
            self.ranged_animation(char='💎', attacker=attacker, defender=defender)
            self.assign_damage(attacker, defender, bonus_damage=self.bonus_damage)
            #TODO: Reduce attack power of the defender
            return True

        else:
            print(f"{defender.name} is out of range!")
            return False
        
    def __str__(self):
        return 'Glintstone Staff'
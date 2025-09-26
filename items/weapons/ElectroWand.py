import Weapon
from characters import Character
from craftingMaterials import Gem, Wood, Sunflower
import AreaOfEffect

class ElectroWand(Weapon):

    aof = AreaOfEffect()

    # Setting Attributes
    def __init__(self):
        super().__init__('⚡', craft_cost={Gem: 1, Wood: 1, Sunflower: 2}, range=16, bonus_damage=13)

    def attack(self, attacker: Character, defender: Character):
        
        if self.aof.inRange(self.range, attacker, defender):
            self.ranged_animation('⚡', attacker=attacker, defender=defender) 

            self.assign_damage(attacker, defender, bonus_damage=self.bonus_damage)
            return True
        
        else:
            print(f"{defender.name} is out of range!")
            return False

    def __str__(self):
         return "Electro Wand"
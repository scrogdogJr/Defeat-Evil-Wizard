import Weapon
from characters import Character
import AreaOfEffect
from craftingMaterials import Dirt, Ice

class IceDart(Weapon):

    aof = AreaOfEffect()

    def __init__(self):
        super().__init__(char='❄️ ', craft_cost={Dirt: 1, Ice: 2}, range=10, bonus_damage=4)

    def attack(self, attacker: Character, defender: Character):
        if self.aof.inRange(attacker, defender):
            self.ranged_animation(char='❄️ ', attacker=attacker, defender=defender)
            self.assign_damage(attacker, defender, bonus_damage=self.bonus_damage)
            defender.movement = (defender.max_movement * 1.5) * -1
            print(f'{defender.name}\'s movement is reduced to {defender.max_movement/2}')
            attacker.weapon = None
            return True

        else:
            print(f"{defender.name} is out of range!")
            return False

    def print_stats(self):
        super().print_stats()
        print('Special Effect: Reduces the target\'s movement by half')  
        
    def __str__(self):
        return 'Ice Dart'
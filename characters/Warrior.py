from .Character import Character
from items import Longsword

# Warrior class (inherits from Character)
class Warrior(Character):
    def __init__(self, name):
        self.shield_uses = 0
        super().__init__(name, char='🥷 ', health=140, attack_power=25, weapon=Longsword(), movement=6)  # Boost health and attack power

    #Must have a special take_damage method to allow for the shield to be used
    def take_damage(self, damage):
        if self.shield_uses > 0:
            damage *= 0.25
            super().take_damage(damage)
            print(f'Reduced by {damage * 3} with shield!')
            self.shield_uses -= 1
        
        else:
            super().take_damage(damage)

        return damage

    # SPECIAL ABILITIES:

    # Shield (Can be stacked)
    def special_ability_1(self):
        if (self.special_ability_charge >= 40):
            self.shield_uses += 1
            self.special_ability_charge -= 40
            self.action_points -= 1
            print("Shield Engaged!")
            return True
        else:
            print("Not enough ability charge! Pick a different action.")
            return False
        
    # Extra Action
    def special_ability_2(self):
        if (self.special_ability_charge >= 90):
            self.action_points += 2
            self.special_ability_charge -= 90
            print("Extra Action Added!")
            return True
        else:
            print("Not enough ability charge! Pick a different action.")
            return False
        
    def display_abilities(self):
        print('\n== Special Abilities ==')
        print('1. Shield (40 AC)')
        print('2. Extra Action (90 AC)')
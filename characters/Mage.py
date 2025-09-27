from .Character import Character
from items.weapons.GlintstoneStaff import GlintstoneStaff

# Mage class (inherits from Character)
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, char='🧝', health=100, attack_power=35, weapon=GlintstoneStaff(), movement=5)  # Boost attack power

    # SPECIAL ABILITIES
        
    #Teleport
    def special_ability_1(self):
        old_movement = self.movement
        if (self.special_ability_charge >= 35):
            self.movement = 150
            self.move()
            self.special_ability_charge -= 35
            self.movement = old_movement
            return True
        else:
            print("Not enough ability charge! Pick a different action.")
            return False
        
    #Invisibility
    def special_ability_2(self):

        if (self.special_ability_charge >= 80):
            self.invisible += 2
            self.special_ability_charge -= 80
            print(f'{self} is now invisible for two rounds and cannot be attacked!')
            return True
        else:
            print("Not enough ability charge! Pick a different action.")
            return False

    def display_abilities(self):
        print('\n== Special Abilities ==')
        print('1. Teleport (35 AC)')
        print('2. Invisibility (80 AC)')
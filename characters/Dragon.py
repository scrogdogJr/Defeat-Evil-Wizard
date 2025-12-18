from .Character import Character
from items.weapons.Claws import Claws
from items.weapons.DragonTail import DragonTail
from items.weapons.FireBreath import FireBreath

# Dragon (inherits from Character)
class Dragon(Character):
    def __init__(self, name):
        super().__init__(name, char='🐲', health=200, attack_power=45, weapon=Claws(), movement=9)

    
    #SPECIAL ABILITIES:
    
    # Tail Swipe
    def special_ability_1(self): 
        if (self.special_ability_charge >= 50):
            self.weapon = DragonTail()
            if (self.attack()):
                self.special_ability_charge -= 50
                self.weapon = Claws()
                return True
            else:
                print("Not enough ability charge! Pick a different action.")
                return False

    # Fire Breath     
    def special_ability_2 (self):

        if (self.special_ability_charge >= 70):
            self.weapon = FireBreath()
            if (self.attack()):
                self.special_ability_charge -= 70
                self.weapon = Claws()
                return True
            else:
                self.weapon = Claws()
                return False
        else:
            print("Not enough ability charge! Pick a different action.")
            return False

    def display_abilities(self):
        print('\n== Special Abilities ==')
        print('1. Tail Swipe (50 AC)')
        print('2. Fire Breath (70 AC)') 


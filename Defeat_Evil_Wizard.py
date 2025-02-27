import random
import re
import math
from abc import ABC, abstractmethod
import time

class Item:
    # Items will be stored in a character's backpack which is a dictionary.
    # Each key will be the char (emoji representaiton) of the item
    # The value will represent how many of that item a character has
    def __init__(self, char):
        self.char = char

    
class Stone(Item):
    def __init__(self):
        super().__init__('🪨 ')

class Gem(Item):
    def __init__(self):
        super().__init__('💎')

class Wood(Item):
    def __init__(self):
        super().__init__('🪵 ')

class Herb(Item):
    def __init__(self):
        super().__init__('🌿')

# MapTile class that holds all the necessary data and methods for an individual tile
class MapTile:
    def __init__(self, y, x, character = None, item = None):
        self.item = item
        self.character = character

        self.update_char()

    def remove_character(self):
        self.character = None
        self.update_char()

    def add_character(self, character):
        self.character = character
        self.update_char()

    def update_char(self, char=' •'):
        if (self.character != None): self.tile_char = self.character.char
        # elif (self.item != None): self.tile_char = self.item.char
        else: self.tile_char = char

# Map class manages a list of MapTile objects
class Map:
    raw_materials = (Stone(), Gem(), Wood(), Herb(), None)
    weights = (15, 5, 20, 10, 50)

    def __init__(self):
        # BE CAREFUL! The y coordinate goes first when this becomes a 2D list
        self.map_tiles = []


    # Creates and prints the map with the characters. Each map tile's coordinate is stored as the index in the 2D string    
    def createMap(self, player, evil_wizard):
        spaces = '  '

        # Makes sure the two characters are not on the same tile
        while player.isPositionEqual(evil_wizard.getx(), evil_wizard.gety):
            player.setPosition(random.randint(0, 29), random.randint(0, 29))

        # Print the spaces to account for y coordinate numbers
        print('\n\n   ', end='')

        # Prints the x coordinate numbers
        for x in range(30):
            if x >= 10: spaces = ' '
            print(f"{x}", end=spaces)
    
        spaces = ' '
        # Nested for loops to print out the map (30 x 30 tiles) and store in a 2D list in coordinate form
        for y in range(30):
            self.map_tiles.append([])
            if y >= 10: spaces = ''
            print(f'\n{y}', end=spaces)

            for x in range(30):

                item = random.choices(self.raw_materials, self.weights, k=1)

                random.choice
                # Checks if this is the coordinate of the player. If so, puts the character in that MapTile
                if player.isPositionEqual(y, x):
                    self.map_tiles[y].append(MapTile(x, y, player, item[0]))

                # Checks if this is the coordinate of the evil_wizard. If so, puts the evil wizard in that MapTile
                elif evil_wizard.isPositionEqual(y, x):
                    self.map_tiles[y].append(MapTile(x, y, evil_wizard, item[0]))

                # If there are no characters or items on the coordinate, just makes it a normal tile space.
                else:
                    self.map_tiles[y].append(MapTile(x, y, item=item[0]))

                # Be CAREFUL! The y coordinate goes first
                print(f"{self.map_tiles[y][x].tile_char} ", end='')
        print("\n\n")

    # Only Prints the map
    def printMap(self):
        spaces = '  '
        # Print the spaces to account for y coordinate numbers
        print('\n\n   ', end='')

        # Prints the x coordinate numbers
        for x in range(30):
            if x >= 10: spaces = ' '
            print(f"{x}", end=spaces)
    
        spaces = ' '
        # Nested for loops to print out the map (30 x 30 tiles) and store in a 2D list in coordinate form
        for y in range(30):
            if y >= 10: spaces = ''
            print(f'\n{y}', end=spaces)

            for x in range(30):
                # Be CAREFUL! The y coordinate goes first
                print(f"{self.map_tiles[y][x].tile_char} ", end='')
        print("\n\n")

'''THIS IS THE ONE MAP OF THE GAME!!!! It is global because so many things need to access it'''
map = Map()


# Base Character class
class Character:
    def __init__(self, name, char, health, attack_power, weapon, armor = False, movement = 6,):
        self.name = name
        self.char = char
        self.health = health
        self.attack_power = attack_power
        self.weapon = weapon
        self.armor = armor
        self.movement = movement
        self.max_health = health  # Store the original health for maximum limit
        self.max_movement = movement # Store the original movement to allow for a reset
        self.action_points = 1
        self.special_ability_charge = 100
        self.__y = random.randint(0, 29)
        self.__x = random.randint(0, 29)
        self.backpack = {}
        self.right_hand = None # Stores what left hand is holding
        self.leftHand = None # Stores what right hand is holding

    def attack(self, opponent):
        self.weapon.attack(self, opponent)

        
    # Restores 5 health up to the maximum
    def heal(self):
        self.health += 5
        if self.health > self.max_health:
            self.health = self.max_health

    def take_damage(self, damage):

        if self.armor:
            damage *= 0.75
            self.health -= round(damage)

        else:
            self.health -= damage

        return damage

    


    # Move function that moves the character from one MapTile object to another within the characters max movement
    def move(self):

        while True:
            # Finds only the coordinates separated by anything
            newTile = re.search(r'(?P<x>\d+)[\D]*(?P<y>\d+)', input("Enter the coordinate pair you would like to move to: "))

            x = int(newTile.group('x'))
            y = int(newTile.group('y'))

            # Finds the distance of the movement and rounds it to the nearest int
            distance = round(math.hypot(x - self.__x, y - self.__y))

            if x not in range(0, 30) and y not in range(0, 30):
                print("Coordinates not in range! Please enter numbers in range 0-29.")

            elif x not in range(0, 30):
                print("x coordinate not in range! Please enter numbers in range 0-29.")

            elif y not in range(0, 30):
                print("y coordinate not in range! Please enter numbers in range 0-29.")
            
            elif distance > self.movement:
                print(f"You tried to move {distance} spaces, but your max movement is {self.movement} spaces. PLease enter a coordinate in range.")

            # Alters the correct MapTile objects to complete the movement
            elif map.map_tiles[y][x].character == None:
                map.map_tiles[self.__y][self.__x].remove_character()
                map.map_tiles[y][x].add_character(self)
                self.__x = x
                self.__y = y
                self.movement -= distance
                break

            else:
                print("Cannot move onto another character! Please enter new coordinates!")

        map.printMap()

    # TODO: ADD OTHER STATS
    def display_stats(self):
        print(f"{self.name}'s Stats - Health: {self.health}/{self.max_health}, Attack Power: {self.attack_power}")

    # Checks if the coordinates are equal to another set
    def isPositionEqual(self, y, x):
        if self.__y == y and self.__x == x:
            return True
        else:
            return False
        
    def gety(self):
        return self.__y
    
    def getx(self):
        return self.__x
    
    def setPosition(self, y, x):
        self.__y == y
        self.__x == x


class AreaOfEffect:

    # Checks if an attacker is in melee range to a defender
    def isMelee(self, attacker: Character, defender: Character):
        if attacker.getx() == defender.getx() - 1 or attacker.getx() == defender.getx() + 1 or attacker.gety() == defender.gety() - 1 or attacker.gety() == defender.gety() + 1:
            return True
        else:
            return False
        
    def inRange(self, range, attacker: Character, defender: Character):
        distance = round(math.hypot(attacker.getx() - defender.getx(), attacker.gety() - defender.gety()))

        if distance <= range:
            return True
        else:
            return False
        
class Weapon:
    # Larger scope because only one is needed among all weapons
    aof = AreaOfEffect()

    def __init__(self, range="Melee", ap_modifier=0, bonus_damage=0):
        # Range will be assumed to be melee unless changed for the particular weapon
        self.range = range
        self.ap_modifier = ap_modifier
        self.bonus_damage = bonus_damage
    @abstractmethod
    def attack(self, attacker: Character, defender: Character):
        pass

    @abstractmethod
    def __str__(self):
        return "<Weapon name>"
    
    def print_stats(self):
        print(f"\n{self.__str__()}:")
        print(f"Attack Power Modifier = +{self.ap_modifier}")
        print(f"Bonus Damage = +{self.bonus_damage}")
        print(f"Range: {self.range}")
    
    def assign_damage(self, attacker: Character, defender: Character, ap_modifier=0, bonus_damage=0):
        attack_power = attacker.attack_power + ap_modifier #Modifies the attack power if a weapon provides a modification

        # Randomizes the damage with the attack power as a modifier and adds any bonus damage from a weapon
        # 0-200 because that makes the attack_power the average damage
        damage = round(random.randint(0, 200) * (attack_power*0.01)) + bonus_damage
        print(f"{attacker.name} attacks {defender.name} with {attacker.weapon} for {defender.take_damage(damage)} damage!") 

class Longsword(Weapon):
    # Setting Attributes
    def __init__(self):
        super().__init__(ap_modifier=15) # This is how the weapon affects the attack and is unique to each weapon

    def attack(self, attacker: Character, defender: Character):
        if self.aof.isMelee(attacker, defender): 

            self.assign_damage(attacker, defender, ap_modifier=self.ap_modifier)
        else:
            print(f"{defender.name} is out of range!")

    def __str__(self):
         return "Longsword"

class ElectroWand(Weapon):
    # Setting Attributes
    def __init__(self):
        super().__init__(range=18, bonus_damage=13)

    def attack(self, attacker: Character, defender: Character):
        if self.aof.inRange(self.range, attacker, defender):

            x = attacker.getx()
            y = attacker.gety()

            x_distance = defender.getx() - attacker.getx()
            y_distance = defender.gety() - attacker.gety()

            try:
                x_inc = int(x_distance/abs(x_distance))
            except ZeroDivisionError:
                x_inc = 0
            try:
                y_inc = int(y_distance/abs(y_distance))
            except ZeroDivisionError:
                y_inc = 0

            # Changes the distances to absolute values for the rest of the function
            x_distance = abs(x_distance)
            y_distance = abs(y_distance)

            offset = x_distance - y_distance

            if offset == 0:
                for i in range(0, y_distance - 1):
                    y += y_inc
                    x+= x_inc
                    map.map_tiles[y][x].update_char('⚡')

            elif offset < 0:

                # This finds how many more steps y needs to make in addition to the diagonal steps
                # It subtracts 1 form the y distance so that the lightning will stop just before the character
                y_steps = (y_distance - 1) - x_distance

                # This finds how many diadonal steps are needed for each y step
                diags_per_y_step = math.floor(x_distance / y_steps)

                # This finds if there any excess diagonal steps needed that do not distibute evenly amoungst the y steps
                excess_steps = x_distance % y_steps

                if excess_steps != 0:
                    # This finds how often those excess steps must be added in each cycle
                    excess_cycle_size = math.ceil(y_steps / excess_steps)

                else:
                    # Sets this to 1 because it should NEVER be 1. If it were 1, that would mean an extra step would need
                    # to be added every cycle. If that were the case, they would be evenly disributed amoungest the y steps
                    excess_cycle_size = 1

                # Loop that iterates through just the y steps
                for i in range(0, y_steps):
                    y += y_inc # Adds extra steps
                    map.map_tiles[y][x].update_char('⚡')

                    # Checks if excess steps are needed and if it is the right time in the cycle
                    if (excess_cycle_size != 1 and i % excess_cycle_size == 0):
                        diags_per_y_step += 1 #Adds the excess step

                    # Prints the map after each step to look like an animation
                    time.sleep(0.03)
                    map.printMap()

                    # Loop that iterates through the diagonal steps that are needed in between the x steps
                    for j in range(0, diags_per_y_step):
                        y += y_inc
                        x += x_inc
                        map.map_tiles[y][x].update_char('⚡')

                    # Checks if an excess step was added.
                    if (excess_cycle_size != 1 and i % excess_cycle_size == 0):
                        diags_per_y_step -= 1

                     # Prints the map after each step to look like an animation
                    time.sleep(0.03)
                    map.printMap()
            elif offset > 0:

                # This finds how many more steps x needs to make in addition to the diagonal steps
                # It subtracts 1 form the x distance so that the lightning will stop just before the character
                x_steps = (x_distance - 1) - y_distance

                # This finds how many diadonal steps are needed for each x step
                diags_per_x_step = math.floor(y_distance / x_steps)

                # This finds if there any excess diagonal steps needed that do not distibute evenly amoungst the x steps
                excess_steps = y_distance % x_steps

                if excess_steps != 0:
                    # This finds how often those excess steps must be added in each cycle
                    excess_cycle_size = math.ceil(x_steps / excess_steps)

                else:
                    # Sets this to 1 because it should NEVER be 1. If it were 1, that would mean an extra step would need
                    # to be added every cycle. If that were the case, they would be evenly disributed amoungest the y steps
                    excess_cycle_size = 1

                # Loop that iterates through just the x steps
                for i in range(0, x_steps):
                    x += x_inc # Adds extra steps
                    map.map_tiles[y][x].update_char('⚡')

                    # Checks if excess steps are needed and if it is the right time in the cycle
                    if (excess_cycle_size != 1 and i % excess_cycle_size == 0):
                        diags_per_x_step += 1 #Adds the excess step

                    # Prints the map after each step to look like an animation
                    time.sleep(0.03)
                    map.printMap()

                    # Loop that iterates through the diagonal steps that are needed in between the x steps
                    for j in range(0, diags_per_x_step):
                        y += y_inc
                        x += x_inc
                        map.map_tiles[y][x].update_char('⚡')

                    # Checks if an excess step was added.
                    if (excess_cycle_size != 1 and i % excess_cycle_size == 0):
                        diags_per_x_step -= 1 # Sets the variable back to its original value so that excess steps don't stack

                    # Prints the map after each step to look like an animation
                    time.sleep(0.03)
                    map.printMap()

            self.assign_damage(attacker, defender, bonus_damage=self.bonus_damage)
        else:
            print(f"{defender.name} is out of range!")

        map.printMap()

    def __str__(self):
         return "Electro Wand"
    
class Claws(Weapon):
    def __init__(self):
        super().__init__(ap_modifier=5)
    
    def attack(self, attacker: Character, defender: Character):
        if self.aof.isMelee(attacker, defender): 
            self.assign_damage(attacker, defender, ap_modifier=self.ap_modifier)

        else:
            print(f"{defender.name} is out of range!")

    def __str__(self):
         return "Claws"
    
class UnarmedStrike(Weapon):
    # No added modifiers or bonuses

    def attack(self, attacker: Character, defender: Character):
        if self.aof.isMelee(attacker, defender):
            self.assign_damage(attacker, defender)

        else:
            print(f"{defender.name} is out of range!")
    
    def __str__(self):
        return "Unarmed Strike"
    

# CHARACTER SUBCLASSES


# Warrior class (inherits from Character)
class Warrior(Character):
    def __init__(self, name):
        self.shield_uses = 0
        super().__init__(name, char='🥷 ', health=140, attack_power=25, weapon=Longsword(), movement=6)  # Boost health and attack power

    def take_damage(self, damage):
        if self.shield_uses > 0:
            damage = 0
            self.shield_uses -= 1
        
        else:
            super().take_damage(damage)

        return damage

    # SPECIAL ABILITIES:

    # This ability allows the Warrior to block the next attack...it can be stacked
    def shield(self):
        if (self.special_ability_charge >= 40):
            self.shield_uses += 1
            self.special_ability_charge -= 40
            self.action_points -= 1
            print("Shield Engaged!")
            return True
        else:
            print("Not enough ability charge! Pick a different action.")
            return False
        
    # This ability gives the Warrior an extra action
    def extra_action(self):
        if (self.special_ability_charge >= 90):
            self.action_points += 1
            self.special_ability_charge -= 90
            print("Extra Action Added!")
            return True
        else:
            print("Not enough ability charge! Pick a different action.")
            return False

# Mage class (inherits from Character)
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, char='🧝', health=100, attack_power=35, weapon=Longsword(), movement=5)  # Boost attack power

    # Add your cast spell method here

# Dragon (inherits from Character)
class Dragon(Character):
    def __init__(self, name):
        super().__init__(name, char='🐲', health=200, attack_power=45, weapon=Claws(), movement=9)


# Artificer (inherits from Character)
class Artificer(Character):
    def __init__(self, name):
        super().__init__(name, char='🧑‍🏭', health=170, attack_power=30, weapon=UnarmedStrike(), movement=8)


# EvilWizard class (inherits from Character)
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, char='🧙', health=150, attack_power=15, weapon=ElectroWand(), movement=7)  # Lower attack power
    
    # Evil Wizard's special ability: it can regenerate health
    def regenerate(self):
        self.health += 5  # Lower regeneration amount
        print(f"{self.name} regenerates 5 health! Current health: {self.health}")                         

# Function to create player character based on user input
def create_character():
    print("Choose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Archer")  # Add Archer
    print("4. Paladin")  # Add Paladin
    
    class_choice = input("Enter the number of your class choice: ")
    name = input("Enter your character's name: ")

    if class_choice == '1':
        return Warrior(name)
    elif class_choice == '2':
        return Mage(name)
    elif class_choice == '3':
        # Add Archer class here
        pass
    elif class_choice == '4':
        # Add Paladin class here
        pass
    else:
        print("Invalid choice. Defaulting to Warrior.")
        return Warrior(name)



# Battle function with user menu for actions
def battle(player: Character, wizard: Character):
    while wizard.health > 0 and player.health > 0:
        choice = None
        print("\n--- Your Turn ---")
        while choice == None:
            choice = re.match(r'[yYnN]', input("Would you like to move? Y/N: "))
            if choice == None:
                print("Please type either Y or N ONLY")

        if choice.group(0).upper() == 'Y':
            map.printMap()
            player.move()
        else:
            print("Skipping movement!")

        print("\nAction Options:")
        print("1. Attack (1 action point)")
        print("2. Use Special Ability (1 action point)")
        print("3. Heal (1 action point)")
        print("4. View Stats (0 action points)")
        print(f"\nAction points = {player.action_points}")
        
        while player.action_points > 0:
            choice = input("Choose an action: ")

            if choice == '1':
                player.attack(wizard)
            elif choice == '2':
                # Call the special ability here
                pass  # Implement this
            elif choice == '3':
                player.heal()
            elif choice == '4':
                player.display_stats()
            else:
                print("Invalid choice, try again.")
                continue

        # Evil Wizard's turn to attack and regenerate
        if wizard.health > 0:
            wizard.regenerate()
            wizard.attack(player)

        if player.health <= 0:
            print(f"{player.name} has been defeated!")
            break

    if wizard.health <= 0:
        print(f"The wizard {wizard.name} has been defeated by {player.name}!")

# Main function to handle the flow of the game
def main():

  artificer = Artificer('Clank')
  evil_wizard = EvilWizard('Merlock')

  map.createMap(artificer, evil_wizard)

  #9.2battle(warrior, evil_wizard)

  artificer.move()

  artificer.attack(evil_wizard)

  evil_wizard.attack(artificer)
    # Character creation phase
   # player = create_character()

    # Evil Wizard is created
  #  wizard = EvilWizard("The Dark Wizard")

    # Start the battle
  #  battle(player, wizard)
      

if __name__ == "__main__":
    main()
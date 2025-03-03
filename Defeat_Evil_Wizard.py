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
        self.char = ' ' + char

    
class Stone(Item):
    def __init__(self):
        super().__init__('🪨 ')

    def __str__(self):
        return "🪨  (Stone)"

class Gem(Item):
    def __init__(self):
        super().__init__('💎')

    def __str__(self):
        return "💎 (Diamond)"

class Wood(Item):
    def __init__(self):
        super().__init__('🪵 ')

    def __str__(self):
        return "🪵  (Wood)"

class Herb(Item):
    def __init__(self):
        super().__init__('🌿')

    def __str__(self):
        return "🌿 (Herb)"

class Maple(Item):
    def __init__(self):
        super().__init__('🍁')

    def __str__(self):
        return "🍁 (Maple Leaf)"

class Ice(Item):
    def __init__(self):
        super().__init__('🧊')

    def __str__(self):
        return "🧊 (Ice)"

class Water(Item):
    def __init__(self):
        super().__init__('💧')

    def __str__(self):
        return "💧 (Water)"

class LadyBug(Item):
    def __init__(self):
        super().__init__('🐞')

    def __str__(self):
        return "🐞 (Lady Bug)"

class Dirt(Item):
    def __init__(self):
        super().__init__('🟤')

    def __str__(self):
        return "🟤 (Dirt)"

class Sunflower(Item):
    def __init__(self):
        super().__init__('🌻')

    def __str__(self):
        return "🌻 (Sunflower)"
    
class AreaOfEffect:

    # Checks if an attacker is in melee range to a defender
    def isMelee(self, attacker, defender):
        if attacker.getx() == defender.getx() - 1 or attacker.getx() == defender.getx() + 1 or attacker.gety() == defender.gety() - 1 or attacker.gety() == defender.gety() + 1:
            return True
        else:
            return False
        
    def inRange(self, range, attacker, defender):
        distance = round(math.hypot(attacker.getx() - defender.getx(), attacker.gety() - defender.gety()))

        if distance <= range:
            return True
        else:
            return False
        
    def findSightRange(self, character, sight_radius=1):
        x_start = max(character.getx() - sight_radius, 0)
        x_end = min(character.getx() + sight_radius, 29)
        y_start = max(character.gety() - sight_radius, 0)
        y_end = min(character.gety() + sight_radius, 29)

        return x_start, x_end, y_start, y_end

    def inSight(self, x, y, character, sight_radius=1):
        # Creates a rannge of coordinates around the intended character with the defined radius
        x_start, x_end, y_start, y_end = self.findSightRange(character, sight_radius) 

        # If the coordinate is within both the x and y range, then the coordinate is in sight
        if x in range(x_start, x_end + 1) and y in range(y_start, y_end + 1):
            return True

        # Else, the coordinate is not in sight
        else:
            return False
        
'''There is one AreaOfEffect object because so many classes need to access it'''
aof = AreaOfEffect()


# MapTile class that holds all the necessary data and methods for an individual tile
class MapTile:
    def __init__(self, x, y , character = None, item = None, showItem=False):
        self.tile_char = ' •'
        self.item = item
        self.character = character
        self.x = x
        self.y = y

        self.update_char(showItem=showItem)

    def remove_character(self):
        self.character = None
        self.update_char()

    def add_character(self, character):
        self.character = character
        self.update_char()


    def update_char(self, char=' •', showItem=False):
        if (self.character != None): 
            if isinstance(self.character, Artificer) and self.item != None:
                self.tile_char = self.character.char[1:] + self.item.char[1:]
            else:
                self.tile_char = self.character.char
        elif (self.item != None and showItem == True):
            self.tile_char = self.item.char
        else: self.tile_char = ' ' + char

# Map class manages a list of MapTile objects
class Map:

    raw_materials = (Stone(), Gem(), Wood(), Herb(), Maple(), Ice(), Water(), LadyBug(), Dirt(), Sunflower(),  None)
    weights = (7, 0.5, 7.5, 3, 3, 2, 4, 3.5, 5.5, 3, 60)

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
        print('\n\n    ', end='')

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
                showItem = isinstance(player, Artificer) and aof.inSight(x, y, player) 

                random.choice
                # Checks if this is the coordinate of the player. If so, puts the character in that MapTile
                if player.isPositionEqual(y, x):
                    self.map_tiles[y].append(MapTile(x, y, player, item[0], showItem))
                    player_item = item[0]

                # Checks if this is the coordinate of the evil_wizard. If so, puts the evil wizard in that MapTile
                elif evil_wizard.isPositionEqual(y, x):
                    self.map_tiles[y].append(MapTile(x, y, evil_wizard, item[0], showItem))

                # If there are no characters or items on the coordinate, just makes it a normal tile space.
                else:
                    self.map_tiles[y].append(MapTile(x, y, item=item[0], showItem=showItem))

                # Checks if the player is an Artificer, if the current tile is to the right of the player, and if
                # there is an item on the players tile. If so, it takes away the leading space of the tile to the 
                # right of the artificer for formatting purposes
                if showItem and player.isPositionEqual(y, x - 1) and player_item != None:
                    self.map_tiles[y][x].tile_char = self.map_tiles[y][x].tile_char[1:]

                print(f"{self.map_tiles[y][x].tile_char}", end='')
        print("\n\n")

    def updateMap(self, player):
        # Checks if the player is the Artificer. If so, it will check if items are in sight
        if isinstance(player, Artificer):
            for y in range(30):
                for x in range(30):
                    # Will update the char on the map and show the item if it is in sight of the Artificer
                    self.map_tiles[y][x].update_char(showItem=aof.inSight(x, y, player))
        else:
            for y in range(30):
                for x in range(30):
                    # Be CAREFUL! The y coordinate goes first
                    self.map_tiles[y][x].update_char()

    # Only Prints the map
    def printMap(self, player):
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

                if isinstance(player, Artificer) and player.isPositionEqual(y, x - 1) and self.map_tiles[y][x - 1].item != None:
                    self.map_tiles[y][x].tile_char = self.map_tiles[y][x].tile_char[1:]

                # Be CAREFUL! The y coordinate goes first
                print(f"{self.map_tiles[y][x].tile_char}", end='')
        print("\n\n")

'''THIS IS THE ONE MAP OF THE GAME!!!! It is global because so many things need to access it'''
map = Map()


# Base Character class
class Character:
    def __init__(self, name, char, health, attack_power, weapon, armor = False, movement = 6):
        self.name = name
        self.char = ' ' + char
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
        self.backpack = dict()
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

                if isinstance(self, Artificer): map.updateMap(player=self)
                break

            else:
                print("Cannot move onto another character! Please enter new coordinates!")

        map.printMap(player=self)

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

        
class Weapon:

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
        if aof.isMelee(attacker, defender): 

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
        # Figures out who the player is for map purposes
        if isinstance(attacker, EvilWizard): player = defender
        else: player = attacker

        if aof.inRange(self.range, attacker, defender):

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
                    map.printMap(player=player)

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
                    map.printMap(player)
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
                    map.printMap(player)

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
                    map.printMap(player)

            self.assign_damage(attacker, defender, bonus_damage=self.bonus_damage)
        else:
            print(f"{defender.name} is out of range!")

        time.sleep(5)
        map.updateMap(player)

        map.printMap(player)

    def __str__(self):
         return "Electro Wand"
    
class Claws(Weapon):
    def __init__(self):
        super().__init__(ap_modifier=5)
    
    def attack(self, attacker: Character, defender: Character):
        if aof.isMelee(attacker, defender): 
            self.assign_damage(attacker, defender, ap_modifier=self.ap_modifier)

        else:
            print(f"{defender.name} is out of range!")

    def __str__(self):
         return "Claws"
    
class UnarmedStrike(Weapon):
    # No added modifiers or bonuses

    def attack(self, attacker: Character, defender: Character):
        if aof.isMelee(attacker, defender):
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
            self.action_points += 2
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

    def pick_up_item(self):
        x_start, x_end, y_start, y_end = aof.findSightRange(self)
        available_items = dict()
        item = None

        # Loops through the items in sight and adds them to a dictionary
        # The keys are the items and the values are how many there are
        for y in range(y_start, y_end + 1):
             for x in range(x_start, x_end + 1):
                 item =  map.map_tiles[y][x].item
                 if item != None:
                    if item not in available_items:
                        available_items[item] = 1
                    else:
                        available_items[item] += 1

        print("\nWhat item would you like to pick up?")
        for key, value in available_items.items():
            print(f"• {key}: x{value}")
             



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
    print("3. Dragon")  # Add Dragon
    print("4. Artificer")  # Add Artificer
    
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
            map.printMap(player)
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

  artificer.pick_up_item()

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
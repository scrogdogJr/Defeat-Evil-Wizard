import random
import re
import math
from abc import ABC, abstractmethod
import time

class Item:
    # Items will be stored in a character's backpack which is a dictionary.
    # Each key will be the char (emoji representaiton) of the item
    # The value will represent how many of that item a character has
    def __init__(self, char, x=0, y=0, craft_cost: dict=None):
        self.char = ' ' + char
        self.craft_cost = craft_cost
        self.x = x
        self.y = y

    @abstractmethod
    def useItem(self, player):
        pass

    @abstractmethod
    def __str__(self):
        pass

class CraftableItem(Item):
    @abstractmethod
    def useItem(self, player):
        pass

    
class Stone(Item):
    def __init__(self, x=0, y=0):
        super().__init__('🪨 ', x, y)

    def __str__(self):
        return "Stone"

class Gem(Item):
    def __init__(self, x=0, y=0):
        super().__init__('💎', x, y)

    def __str__(self):
        return "Diamond"

class Wood(Item):
    def __init__(self, x=0, y=0):
        super().__init__('🪵 ', x, y)

    def __str__(self):
        return "Wood"

class Herb(Item):
    def __init__(self, x=0, y=0):
        super().__init__('🌿', x, y)

    def __str__(self):
        return "Herb"

class Maple(Item):
    def __init__(self, x=0, y=0):
        super().__init__('🍁', x, y)

    def __str__(self):
        return "Maple Leaf"

class Ice(Item):
    def __init__(self, x=0, y=0):
        super().__init__('🧊', x, y)

    def __str__(self):
        return "Ice"

class Water(Item):
    def __init__(self, x=0, y=0):
        super().__init__('💧', x, y)

    def __str__(self):
        return "Water"

class LadyBug(Item):
    def __init__(self, x=0, y=0):
        super().__init__('🐞', x, y)

    def __str__(self):
        return "Ladybug"

class Dirt(Item):
    def __init__(self, x=0, y=0):
        super().__init__('🟤', x, y)

    def __str__(self):
        return "Dirt"

class Sunflower(Item):
    def __init__(self, x=0, y=0):
        super().__init__('🌻', x, y)

    def __str__(self):
        return "Sunflower"

class SpeedPotion(Item):
    def __init__(self):
        super().__init__('🍾', craft_cost={Water: 2, LadyBug: 1})

    def useItem(self, player):
        player.max_movement += 6
        player.movement += 6
        print(f'Drank speed potion! {player}\'s max movement increased to {player.max_movement}\nCurrent movement = {player.movement}')
        player.item = None

    def print_stats(self):
        print('Increases the player\'s movement and maximum movement by 6.')

    def __str__(self):
        return 'Speed Potion'
    
class AttackPowerPotion(CraftableItem):
    def __init__(self):
        super().__init__('🧪', craft_cost={Water: 2, Maple: 1})

    def useItem(self, player):
        player.ap_modifier += 10
        print(f'Drank Attack Power Potion! {player}\'s attack power is increased to {player.ap_modifier}')
        player.item = None

    def print_stats(self):
        print('Increases the player\'s attack power by 10.')

    def __str__ (self):
        return  'Attack Power Potion'
    
class HealthPotion(CraftableItem):
    def __init__(self):
        super().__init__('🍼', craft_cost={Water: 2, Dirt: 1, Herb: 1})

    def useItem(self, player):
        player.max_health += 15
        player.health += 15
        print(f'Drank Health Potion! {player}\'s max health is increased to {player.max_health}\nCurrent health = {player.health}')
        player.item = None

    def print_stats(self):
        print('Increases the player\'s health and maximum health by 15.')

    def __str__(self):
        return 'Health Potion'
    
class InvisibilityPotion(CraftableItem):
    def __init__(self):
        super().__init__('🥛', craft_cost={Water: 2, Gem: 1, Herb: 1})

    def useItem(self, player):
        player.invisible += 2
        print(f'Drank Invisibility Potion! {player} is now invisible for two rounds and cannot be attacked!')
        player.item = None

    def print_stats(self):
        print('Makes the player invisible for two rounds where they cannot be attacked.')

    def __str__(self):
        return 'Invisibility Potion'


    
class AreaOfEffect:

    # Checks if an attacker is in melee range to a defender
    def isMelee(self, attacker, defender):
        if ((attacker.getx() == defender.getx() - 1 or attacker.getx() == defender.getx() + 1 or attacker.gety() == defender.gety() - 1 or attacker.gety() == defender.gety() + 1) and defender.invisible <= 0):
            return True
        else:
            return False
        
    def inRange(self, range, attacker, defender):
        distance = round(math.hypot(attacker.getx() - defender.getx(), attacker.gety() - defender.gety()))

        if (distance <= range and defender.invisible <= 0):
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

    def remove_item(self):
        self.item = None
        self.update_char()

    #Updates the char on the map. Shows a character if it is on the space. And, shows the item AND Artificer if they share a space. Allows a parameter
    #to dictate whether an item is shown elsewhere
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

    raw_materials = (Stone, Gem, Wood, Herb, Maple, Ice, Water, LadyBug, Dirt, Sunflower, None)
    weights = (7, 0.5, 6.5, 3, 3, 2, 5, 3.5, 5.5, 3, 60)

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
                if item[0] != None:
                    item[0] = item[0](x, y)
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
                    print(self.map_tiles[y][x].tile_char[1:], end='')

                else:
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
        print('\n\n    ', end='')

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

                #Same logic as in createMap()
                if isinstance(player, Artificer) and player.isPositionEqual(y, x - 1) and self.map_tiles[y][x - 1].item != None:
                    print(self.map_tiles[y][x].tile_char[1:], end='')

                else:
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
        self.invisible = 0
        self.item = None
        self.right_hand = None # Stores what left hand is holding
        self.leftHand = None # Stores what right hand is holding

    def attack(self, opponent):
        if (self.weapon == None):
            print('No weapon equipped. Please equip a weapon.')
            return False

        elif (self.weapon.attack(self, opponent)):
            return True

        else:
            return False
        
    def useItem(self):
        try:
            self.item.useItem(self)
            return True
        except AttributeError:
            print(f'No item in hand! Please equip an item.')
            return False

        
    # Restores 5 health up to the maximum
    def heal(self):
        heal = 7
        if self.health + heal > self.max_health:
            heal = self.max_health - self.health

        self.health += heal
        print(f"{self.char} {self.name} healed {heal} to {self.health}/{self.max_health} health")
        time.sleep(3)

    def take_damage(self, damage):

        if self.armor:
            damage *= 0.75
            self.health -= round(damage)

        else:
            self.health -= damage

        return damage
    

    # Move function that moves the character from one MapTile object to another within the characters max movement
    def move(self, teleport=False):

        while True:
            # Finds only the coordinates separated by anything
            newTile = re.search(r'(?P<x>\d+)[\D]*(?P<y>\d+)', input("Enter the coordinate pair you would like to " + ("teleport to: " if teleport else "move to: ")))

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
        print(f"{self.name} " + ("teleported " if teleport else "moved " + f"to ({x}, {y})"))
        time.sleep(1)

    # TODO: ADD OTHER STATS
    def display_stats(self):
        capital_name = self.name.upper()
        print(f"\n=={self.char} {capital_name}'S STATS ==\n")
        print(f"• Health: {self.health}/{self.max_health}")
        print(f"• Attack Power: {self.attack_power}")
        print(f'• Ability Charge (AC): {self.special_ability_charge}/100')
        print(f"• Weapon:" + (f"{self.weapon.char}" if self.weapon != None else "") + f" {self.weapon}")
        print(f"• Item:" + (f"{self.item.char}" if self.item != None else "") + f" {self.item}")
        
        if self.weapon != None:
            self.weapon.print_stats()
 
        if self.item != None:
            print(f'\n    --{self.item.char} {self.item} --')
            self.item.print_stats()

        if len(self.backpack) > 0:
            
            print("\n    -- Backpack Items --")

            for key, value in self.backpack.items():
                item = key()
                print(f'    • {item.char}   {item} x{value}')

        if isinstance(self, Artificer):
            craftable_items = (Longsword, GlintstoneStaff, ElectroWand, SpeedPotion, AttackPowerPotion, HealthPotion, InvisibilityPotion, IceDart)
            print('\n    --Craftable Items--')

            for i in craftable_items:
                item = i()
                print(f'\n    {item.char} {item}')

        print('\n\n' + '-' * 100 + '\n\n')


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
        self.__y = y
        self.__x = x

    @abstractmethod
    def special_ability_1(self):
        pass
    

    @abstractmethod
    def special_ability_2(self):
        pass
        
class Weapon(Item):

    def __init__(self, char='', craft_cost: dict=None, range="Melee", ap_modifier=0, bonus_damage=0):
        super().__init__(char, craft_cost=craft_cost)
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
        print(f"\n    --{self.char} {self.__str__()} --")
        print(f"    • Attack Power Modifier: +{self.ap_modifier}")
        print(f"    • Bonus Damage: +{self.bonus_damage}")
        print(f"    • Range: {self.range}")
    
    def assign_damage(self, attacker: Character, defender: Character, ap_modifier=0, bonus_damage=0):
        attack_power = attacker.attack_power + ap_modifier #Modifies the attack power if a weapon provides a modification

        # Randomizes the damage with the attack power as a modifier and adds any bonus damage from a weapon
        # 0-200 because that makes the attack_power the average damage
        damage = round(random.randint(0, 200) * (attack_power*0.01)) + bonus_damage
        attacker.special_ability_charge += round(damage * 0.25)
        print(f"{attacker.name} attacks {defender.name} with {attacker.weapon} for {defender.take_damage(damage)} damage!")
        print(f'Ability Charge increased by {round(damage * 0.25)}!')

    def ranged_animation (self, char: str, attacker: Character, defender: Character):
        # Figures out who the player is for map purposes
        if isinstance(attacker, EvilWizard): player = defender
        else: player = attacker

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
                map.map_tiles[y][x].update_char(char)

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
                map.map_tiles[y][x].update_char(char)

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
                    map.map_tiles[y][x].update_char(char)

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
                map.map_tiles[y][x].update_char(char)

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
                    map.map_tiles[y][x].update_char(char)

                # Checks if an excess step was added.
                if (excess_cycle_size != 1 and i % excess_cycle_size == 0):
                    diags_per_x_step -= 1 # Sets the variable back to its original value so that excess steps don't stack

                # Prints the map after each step to look like an animation
                time.sleep(0.03)
                map.printMap(player)

class Longsword(Weapon):
    # Setting Attributes
    def __init__(self):
        super().__init__('🗡️ ', craft_cost={Stone: 2}, ap_modifier=15) # This is how the weapon affects the attack and is unique to each weapon

    def attack(self, attacker: Character, defender: Character):
        if aof.isMelee(attacker, defender): 

            self.assign_damage(attacker, defender, ap_modifier=self.ap_modifier)
            return True
        else:
            print(f"{defender.name} is out of range!")
            return False

    def __str__(self):
         return "Longsword"
    

class ElectroWand(Weapon):
    # Setting Attributes
    def __init__(self):
        super().__init__('⚡', craft_cost={Gem: 1, Wood: 1, Sunflower: 2}, range=16, bonus_damage=13)

    def attack(self, attacker: Character, defender: Character):
        
        if aof.inRange(self.range, attacker, defender):
            self.ranged_animation('⚡', attacker=attacker, defender=defender) 

            self.assign_damage(attacker, defender, bonus_damage=self.bonus_damage)
            return True
        
        else:
            print(f"{defender.name} is out of range!")
            return False

    def __str__(self):
         return "Electro Wand"
    
    
class Claws(Weapon):
    def __init__(self):
        super().__init__(ap_modifier=5)
    
    def attack(self, attacker: Character, defender: Character):
        if aof.isMelee(attacker, defender): 
            self.assign_damage(attacker, defender, ap_modifier=self.ap_modifier)
            return True

        else:
            print(f"{defender.name} is out of range!")
            return False

    def __str__(self):
         return "Claws"
    
class FireBreath(Weapon):
    #Setting attributes
    def __init__(self):
        super().__init__(range=20, bonus_damage=25)

    def attack(self, attacker: Character, defender: Character):
        if aof.inRange(self.range, attacker=attacker, defender=defender):
            self.ranged_animation('🔥', attacker=attacker, defender=defender)

            self.assign_damage(attacker, defender, bonus_damage=self.bonus_damage)
            return True

        else:
            print(f"{defender.name} is out of range!")
            return False

    def __str__(self):
         return "Fire Breath"
    
class DragonTail(Weapon):
    def __init__(self):
        super().__init__(range=10, ap_modifier=7)

    def attack(self, attacker: Character, defender: Character):
        if aof.inRange(self.range, attacker, defender):
            
            defender.max_movement = defender.max_movement * -1

            self.assign_damage(attacker, defender, ap_modifier=self.ap_modifier)
            print(f'{defender} is knocked down and cannot move next turn!')
            return True
        else:
            print(f"{defender.name} is out of range!")
            return False
        
    def print_stats(self):
        super().print_stats()
        print('Special Effect: Knocks down target where they cannot move on their next turn.')
        
    def __str__(self):
        return "Dragon Tail"
    
    
class UnarmedStrike(Weapon):
    # No added modifiers or bonuses
    def __init__(self):
        super().__init__(char='👊', craft_cost={LadyBug: 1})

    def attack(self, attacker: Character, defender: Character):
        if aof.isMelee(attacker, defender):
            self.assign_damage(attacker, defender)
            return True

        else:
            print(f"{defender.name} is out of range!")
            return False
    
    def __str__(self):
        return "Unarmed Strike"
    
class GlintstoneStaff(Weapon):

    def __init__(self):
        super().__init__(char='🪄 ', craft_cost={Wood: 2, Gem: 1, Stone: 1}, range=14, bonus_damage=10)

    def attack(self, attacker: Character, defender: Character):
        if aof.inRange(attacker, defender):
            self.ranged_animation(char='💎', attacker=attacker, defender=defender)
            self.assign_damage(attacker, defender, bonus_damage=self.bonus_damage)
            #TODO: Reduce attack power of the defender
            return True

        else:
            print(f"{defender.name} is out of range!")
            return False
        
    def __str__(self):
        return 'Glintstone Staff'
    
class IceDart(Weapon):

    def __init__(self):
        super().__init__(char='❄️ ', craft_cost={Dirt: 1, Ice: 2}, range=10, bonus_damage=4)

    def attack(self, attacker: Character, defender: Character):
        if aof.inRange(attacker, defender):
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
    

# CHARACTER SUBCLASSES


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

# Mage class (inherits from Character)
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, char='🧝', health=100, attack_power=35, weapon=GlintstoneStaff(), movement=5)  # Boost attack power

    # Add your cast spell method here

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


# Artificer (inherits from Character)
class Artificer(Character):
    def __init__(self, name):
        super().__init__(name, char='👷', health=170, attack_power=30, weapon=UnarmedStrike(), movement=10)


    # SPECIFIC ACTIONS
    def pick_up_two_items(self):
        x_start, x_end, y_start, y_end = aof.findSightRange(self)
        available_items = dict()
        item = None

        # Loops through the items in sight and adds them to a dictionary
        # The keys are the items and the values are how many there are
        for y in range(y_start, y_end + 1):
             for x in range(x_start, x_end + 1):
                 item =  map.map_tiles[y][x].item
                 if item != None:
                    if str(item) not in available_items:
                        available_items[str(item)] = {item}
                    else:
                        available_items[str(item)].add(item)

        count = 0
        while count < 2:

            if not available_items:
                if count == 0: 
                    print("No items in sight! Pick a differnt action. Returning to main menu...")
                    time.sleep(3)
                    return False

                else: 
                    print("No more items in sight! Returning to main menu...")
                    time.sleep(3)
                    return True

            #Loops through the items in sight and prints them out for the user to see
            print("\n==ITEMS NEARBY==")

            for key, value in available_items.items():
                print(f"{next(iter(value)).char}   {key}   x{len(value)}") 

            if count == 0:
                item_choice = input("\nType the name of an item to pick it up: ")

            else:
                item_choice = input("\nType the name of another item to pick it up: ")

            found = False

            # Loops through the keys and checks if any match the item chosen
            for key in available_items.keys():
                if (item_choice.lower() == key.lower()):

                    found = True

                    #Subtracts it from the available items in the dictionary
                    item_choice = available_items[key].pop()

                    #Checks if there are no more items of that type. If so, deletes the key
                    if not available_items[key]:
                        del available_items[key]

                    #Adds it to the backpack dictionary
                    if type(item_choice) not in self.backpack:
                        self.backpack[type(item_choice)] = 1
                    else:
                        self.backpack[type(item_choice)] += 1

                    #Subtracts it from the map
                    map.map_tiles[item_choice.y][item_choice.x].remove_item()
                
                    print(f"\n{item_choice.char}    {item_choice} picked up!")
                    count += 1
                    time.sleep(2)
                    break

            if not found:
                print(f"\n{item_choice} not in sight. Please check your spelling and try again.")
                time.sleep(3)

        map.printMap(player=self)
        time.sleep(1)
        return True

    
    def equip(self):
        available_items = {}
        print('\n==Items to Equip==\n')
        for key, value in self.backpack.items():

            if issubclass(key, CraftableItem) or issubclass(key, Weapon):
                item_to_equip = key()
                available_items.add(item_to_equip)
                print(f'{item_to_equip.char}   {item_to_equip} x{value}')

        if not available_items:
            print('No items or weapons available to equip in your backpack. Returning to Main Menu...')
            return False
        
        found = False
        while not found:
            item_to_equip = input('Please enter the name of the weapon or item you would like to equip: ')

            for i in available_items:

                if item_to_equip.lower() == (str(i)).lower():
                    if isinstance(i, Weapon):
                        self.weapon = i
                        print(f'\n{self.weapon.char}   {self.weapon} equipped as weapon.')

                    else:
                        self.item = i
                        print(f'\n{self.weapon.char}   {self.item} equipped as item.')

                    self.backpack[type(i)] -= 1

                    if self.backpack[type(i)] <= 0:
                        del self.backpack[type(i)]

                    found = True
                    return True

                else:
                    print(f'{item_to_equip} is not in your backpack. Please check your spelling and try again.')


    # SPECIAL ABILITIES

    # Craft
    def special_ability_1(self):
        if self.special_ability_charge >= 30:

            craftable_items = (Longsword, GlintstoneStaff, ElectroWand, SpeedPotion, AttackPowerPotion, HealthPotion, InvisibilityPotion, IceDart)

            length = len(craftable_items)
            first_run = True

            print('\n==Craftable Items==                                                 ==Items in Backpack==', end='')

            for i in range(0,length):
                item = craftable_items[i]()
                name = f'{item.char}   {item}: '
                name_length = len(name)
                if type(item) == Longsword: name_length -= 1
                elif type(item) == GlintstoneStaff: name_length += 1
                print(f'\n\n{name}', end='')

                atStart = True
                cost_length = 0
                for key, value in item.craft_cost.items():

                    cost = None
                    if atStart:
                        cost = f'{value if value > 1 else ""}{key().char[1:]}'
                        atStart = False

                    else:
                        cost = f' + {value if value > 1 else ""}{key().char[1:]}'

                    cost_length += len(cost)
                    if key == Wood or key == Stone: cost_length -= 1
                    print(f'{cost}', end='')

                count = 0
                #Adjusts spacing to account for the different lengths of names and costs
                extra_spaces = 68 - (name_length + cost_length)
                print(' ' * extra_spaces, end='')
            
                if i < math.ceil(len(self.backpack.items()) / 2): 
                
                    cost = None
                    start = False
                    for key, value in self.backpack.items():

                        if count < 3 and start == True: start_key = key

                        start = False

                        if first_run or (start_key == key and count < 2):
                            start = True
                            first_run = False

                        if start:
                            cost = (f'{value if value > 1 else ' '}{key().char[1:]}')
                            count +=1
                            print(cost, end='')

            found = False
            while found == False:
                item_to_craft = input(f'\n\nPlease type the name of the item you want to craft: ')

                for i in craftable_items:
                
                    item = i()

                    if item_to_craft.lower() == str(item).lower():
                        found = True
                        item_to_craft = item
                        break
                
                if not found:
                    print(f'{item_to_craft} not available to craft. Please check your spelling and try again.')
                    time.sleep(3)

            afford = True
            for key, value in item_to_craft.craft_cost.items():
            
                if key in self.backpack.keys():
                    if value > self.backpack[key]:
                        afford = False
                        print(f'\nNot enough resources to craft the {item_to_craft}...')
                        time.sleep(3)
                        return False

                else:
                    afford = False
                    print(f'\nNot enough resources to craft the {item_to_craft}...')
                    time.sleep(3)
                    return False

            if afford:
                for key, value in item_to_craft.craft_cost.items():

                    self.backpack[key] -= value

                    if self.backpack[key] <= 0:
                        del self.backpack[key]

                print(f'\n{item_to_craft.char}   {item_to_craft} has been crafted!')

                choice = None

                while choice == None:
                    choice = re.match(r'.', input(f'\nPress \'e\' and enter to equip the {item_to_craft} \nPress \'b\' and enter to place the {item_to_craft} into your backpack\n'))

                    if choice[0].lower() == 'b':

                        if type(item_to_craft) in self.backpack:
                            self.backpack[type(item_to_craft)] += 1

                        else:
                            self.backpack[type(item_to_craft)] = 1

                        print(f'\n{item_to_craft.char}   {item_to_craft} plcaed in backpack!') #TODO tell how to acess backpack when you figure that out

                    elif choice[0].lower() ==  'e':
                        if (isinstance(item_to_craft, Weapon)):
                            self.weapon = item_to_craft
                            print(f'{item_to_craft.char}   {item_to_craft} equipped as weapon!')

                        else:
                            self.item = item_to_craft
                            print(f'{item_to_craft.char}   {item_to_craft} equipped as item!')

                    else:
                        choice = None
                        print('Not a valid response. Please check your selection and try again.')
                return True

            else:
                print("Not enough ability charge! Pick a different action.")
                return False


    # Use Item
    def special_ability_2(self):
        if (self.special_ability_charge >= 10):
            if (super().useItem()):
                self.special_ability_charge -= 10
                return True
            else:
                return False
        else:
            print("Not enough ability charge! Pick a different action.")
            return False
        
    
    def display_abilities(self):
        print('\n== Special Abilities ==')
        print('1. Craft (30 AC)')
        print('2. Use Item (10 AC)') 



# EvilWizard class (inherits from Character)
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, char='🧙', health=150, attack_power=15, weapon=ElectroWand(), movement=8)  # Lower attack power
    
    # Evil Wizard's special ability: it can regenerate health
    def regenerate(self):
        self.health += 5  # Lower regeneration amount
        print(f"{self.name} regenerates 5 health! Current health: {self.health}")

    def find_move_target(self, defender):
        distance_traveled = 0

        x = self.getx()
        y = self.gety()

        x_distance = defender.getx() - self.getx()
        y_distance = defender.gety() - self.gety()

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
                distance_traveled += math.sqrt(2) # Makes distance accurate according to Pythagorean Theorem
                if round(distance_traveled) >= self.movement:
                    print('1')
                    return x, y
                print(f'old x{x}, old y{y}') 
                y += y_inc
                x += x_inc
                print(f'newx{x}, newy{y}')
                                

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
                distance_traveled += 1
                if round(distance_traveled) >= self.movement:
                    print('2')
                    return x, y
                print(f'old x{x}, old y{y}')
                y += y_inc # Adds extra steps
                print(f'newx{x}, newy{y}')

                # Checks if excess steps are needed and if it is the right time in the cycle
                if (excess_cycle_size != 1 and i % excess_cycle_size == 0):
                    diags_per_y_step += 1 #Adds the excess step


                # Loop that iterates through the diagonal steps that are needed in between the x steps
                for j in range(0, diags_per_y_step):
                    distance_traveled += math.sqrt(2) # Makes distance accurate according to Pythagorean Theorem
                    if round(distance_traveled) >= self.movement:
                        print('3')
                        return x, y 
                    print(f'old x{x}, old y{y}')                   
                    y += y_inc
                    x += x_inc
                    print(f'newx{x}, newy{y}')

                # Checks if an excess step was added.
                if (excess_cycle_size != 1 and i % excess_cycle_size == 0):
                    diags_per_y_step -= 1


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
                distance_traveled += 1
                if round(distance_traveled) >= self.movement:
                    print('4')
                    return x, y
                print(f'old x{x}, old y{y}')
                x += x_inc # Adds extra steps
                print(f'newx{x}, newy{y}')

                # Checks if excess steps are needed and if it is the right time in the cycle
                if (excess_cycle_size != 1 and i % excess_cycle_size == 0):
                    diags_per_x_step += 1 #Adds the excess step


                # Loop that iterates through the diagonal steps that are needed in between the x steps
                for j in range(0, diags_per_x_step):
                    distance_traveled += math.sqrt(2) # Makes distance accurate according to Pythagorean Theorem
                    if round(distance_traveled) >= self.movement:
                        print('5')
                        return x, y  
                    print(f'old x{x}, old y{y}')
                    y += y_inc
                    x += x_inc
                    print(f'newx{x}, newy{y}')

                # Checks if an excess step was added.
                if (excess_cycle_size != 1 and i % excess_cycle_size == 0):
                    diags_per_x_step -= 1 # Sets the variable back to its original value so that excess steps don't stack

    def move(self, defender):
        mytTuple = tuple()
        x = 0
        y = 0
        mytTuple = self.find_move_target(defender)
        x = mytTuple[0]
        y = mytTuple[1]
        print(f'{x}, {y}')

        if map.map_tiles[y][x].character == None:
            print('Character not at target')
            map.map_tiles[self.gety()][self.getx()].remove_character()
            map.map_tiles[y][x].add_character(self)
            self.setPosition(y, x)
            map.updateMap(defender)
            map.printMap(defender)
            print(f'{self.name} moved to ({x}, {y})!')
            time.sleep(2)
        print('end movement')



                             

# Function to create player character based on user input
def create_character():
    print("\nChoose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Dragon")  # Add Dragon
    print("4. Artificer")  # Add Artificer
    
    class_choice = input("\nEnter the number of your class choice: ")
    name = input("Enter your character's name: ")

    if class_choice == '1':
        return Warrior(name)
    elif class_choice == '2':
        return Mage(name)
    elif class_choice == '3':
        return Dragon(name)
    elif class_choice == '4':
        return Artificer(name)
    else:
        print("Invalid class choice. Defaulting to Warrior.")
        return Warrior(name)


# Battle function with user menu for actions
def battle(player: Character, wizard: Character):
    while wizard.health > 0 and player.health > 0:

        #Resets all necessary data
        if player.invisible > 0: player.invisible -= 1

        player.movement += player.max_movement
        if player.movement > player.max_movement: player.movement = player.max_movement

        player.action_points = 1


        choice = None
        print("\n--- Your Turn ---")
        while choice == None:
            choice = re.match(r'.', input(f"Would you like to move at the start of your turn? (Movement: {player.movement}/{player.max_movement}) Y/N: "))
            if choice == None:
                print("Please type either Y or N ONLY")

        if choice.group(0).upper() == 'Y':
            map.printMap(player)
            player.move()
        else:
            print("Skipping movement!")

        print("\nAction Options:")
        print("1. Attack (1 Action Point)")
        print("2. Use Special Ability (1 Action Point)")
        print("3. Heal (1 Action Point)")
        if isinstance(player, Artificer): 
            print("4. Pick Up Two Items (1 Action Point)")
            print("5. Equip Item or Weapon (0 Action Points)")
            print("6. View Stats (0 Actions Points)")
        else:
            print("4. View Stats (0 Action Points)")
        print(f"\nAction points = {player.action_points}")
        
        while player.action_points > 0:
            choice = input("Choose an action: ")

            if choice == '1':
                player.attack(wizard)
                player.action_points -= 1

            elif choice == '2':
                player.display_abilities()
                choice = input('Choose a special ability: ')

                if choice == '1':
                    if player.special_ability_1():
                        player.action_points -= 1
                elif choice == '2':
                    if player.special_ability_2():
                        player.action_points -= 1
                
            elif choice == '3':
                player.heal()
                player.action_points -= 1

            elif isinstance(player, Artificer):
                if choice == '4':
                    if player.pick_up_two_items():
                        player.action_points -= 1
                elif choice == '5':
                    player.equip()
                elif choice == '6':
                    player.display_stats()
                else:
                    print("Invalid choice, try again.")
                    continue

            elif not isinstance(player, Artificer):
                if choice == '4':
                    player.display_stats()
                else:
                    print("Invalid choice, try again.")
                    continue

        choice = None
        while choice == None:
            choice = re.match(r'.', input(f"Would you like to move at the end of your turn? (Movement: {player.movement}/{player.max_movement}) Y/N: "))
            if choice == None:
                print("Please type either Y or N ONLY")

        if choice.group(0).upper() == 'Y':
            map.printMap(player)
            player.move()
        else:
            print("Skipping movement!")
            time.sleep(1)

        # Evil Wizard's turn to attack and regenerate
        if wizard.health > 0:
            map.printMap(player)
            print(f"\n{wizard.name}\'s turn!")
            time.sleep(2)

            wizard.regenerate()

            time.sleep(2)

            #Checks if the wizard needs to move
            if not aof.inRange(wizard.weapon.range, wizard, player):
                print('not in range')
                wizard.move(player)
                time.sleep(2)

            print('In range')

            wizard.attack(player)
            time.sleep(5)
            map.updateMap(player)
            map.printMap(player)

    if player.health <= 0:
        print(f"{player.name} has been defeated!")
        

    if wizard.health <= 0:
        print(f"The wizard {wizard.name} has been defeated by {player.name}!")

# Main function to handle the flow of the game
def main():

    print("\n\nWELCOME TO DEFEAT THE EVIL WIZARD!!! \n\nIn this game, you will choose from four character classes with their own unique abilities \n" \
    "" \
    "to battle the Evil Wizard. May the odds be ever in your favor...")
    input("\n\nPress Enter to continue...")

    # Character creation phase
    player = create_character()

    # Evil Wizard is created
    wizard = EvilWizard("The Dark Wizard Merlock")

    print(f"\n\n{player.char} {player.name} VS{wizard.char} {wizard.name} \n\nLET THE BATTLE COMMENCE!!!")
    time.sleep(3)

    map.createMap(player, wizard)

    # Start the battle
    battle(player, wizard)
      

if __name__ == "__main__":
    main()
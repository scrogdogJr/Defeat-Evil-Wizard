# Base Character class
import random
import time
import re
import math
from abc import abstractmethod
import config

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
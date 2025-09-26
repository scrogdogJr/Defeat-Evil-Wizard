import time
import re
import math
from .Character import Character
import config
from items import Longsword, GlintstoneStaff, ElectroWand, SpeedPotion, AttackPowerPotion, HealthPotion, InvisibilityPotion, IceDart, UnarmedStrike
from items import CraftableItem, Weapon, Wood, Stone
import AreaOfEffect

# Artificer (inherits from Character)
class Artificer(Character):

    aof = AreaOfEffect()
    def __init__(self, name):
        super().__init__(name, char='👷', health=170, attack_power=30, weapon=UnarmedStrike(), movement=10)

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

                map.updateMap(player=self)
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

        craftable_items = (Longsword, GlintstoneStaff, ElectroWand, SpeedPotion, AttackPowerPotion, HealthPotion, InvisibilityPotion, IceDart)
        print('\n    --Craftable Items--')

        for i in craftable_items:
            item = i()
            print(f'\n    {item.char} {item}')

        print('\n\n' + '-' * 100 + '\n\n')


    # SPECIFIC ACTIONS
    def pick_up_two_items(self):
        x_start, x_end, y_start, y_end = self.aof.findSightRange(self)
        available_items = dict()
        item = None

        # Loops through the items in sight and adds them to a dictionary
        # The keys are the items and the values are how many there are
        for y in range(y_start, y_end + 1):
             for x in range(x_start, x_end + 1):
                 item =  config.MAP.map_tiles[y][x].item
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
                    config.MAP.map_tiles[item_choice.y][item_choice.x].remove_item()
                
                    print(f"\n{item_choice.char}    {item_choice} picked up!")
                    count += 1
                    time.sleep(2)
                    break

            if not found:
                print(f"\n{item_choice} not in sight. Please check your spelling and try again.")
                time.sleep(3)

        config.MAP.printMap(player=self)
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
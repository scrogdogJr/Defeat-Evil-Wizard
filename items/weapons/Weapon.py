from typing import TYPE_CHECKING
from items.Item import Item
import time
import random
from abc import abstractmethod
import math

if TYPE_CHECKING:
    from characters.Character import Character
    from characters.EvilWizard import EvilWizard


class Weapon(Item):

    def __init__(self, char='', craft_cost: dict=None, range="Melee", ap_modifier=0, bonus_damage=0):
        super().__init__(char, craft_cost=craft_cost)
        # Range will be assumed to be melee unless changed for the particular weapon
        self.range = range
        self.ap_modifier = ap_modifier
        self.bonus_damage = bonus_damage

    @abstractmethod
    def attack(self, attacker: 'Character', defender: 'Character'):
        pass

    @abstractmethod
    def __str__(self):
        return "<Weapon name>"
    
    def print_stats(self):
        print(f"\n    --{self.char} {self.__str__()} --")
        print(f"    • Attack Power Modifier: +{self.ap_modifier}")
        print(f"    • Bonus Damage: +{self.bonus_damage}")
        print(f"    • Range: {self.range}")
    
    def assign_damage(self, attacker: 'Character', defender: 'Character', ap_modifier=0, bonus_damage=0):
        attack_power = attacker.attack_power + ap_modifier #Modifies the attack power if a weapon provides a modification

        # Randomizes the damage with the attack power as a modifier and adds any bonus damage from a weapon
        # 0-200 because that makes the attack_power the average damage
        damage = round(random.randint(0, 200) * (attack_power*0.01)) + bonus_damage
        attacker.special_ability_charge += round(damage * 0.25)
        print(f"{attacker.name} attacks {defender.name} with {attacker.weapon} for {defender.take_damage(damage)} damage!")
        print(f'Ability Charge increased by {round(damage * 0.25)}!')

    def ranged_animation (self, char: str, attacker: 'Character', defender: 'Character'):
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
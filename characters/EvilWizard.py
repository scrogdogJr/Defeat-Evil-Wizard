import time
import math
from .Character import Character
from items.weapons.ElectroWand import ElectroWand

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
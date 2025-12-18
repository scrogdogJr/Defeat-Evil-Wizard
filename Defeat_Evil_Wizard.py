import random
import re
import math
from abc import ABC, abstractmethod
import time
import universal
from characters.Character import Character
from characters.Warrior import Warrior
from characters.Mage import Mage
from characters.Dragon import Dragon
from characters.Artificer import Artificer
from characters.EvilWizard import EvilWizard

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
            universal.MAP.printMap(player)
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
            universal.MAP.printMap(player)
            player.move()
        else:
            print("Skipping movement!")
            time.sleep(1)

        # Evil Wizard's turn to attack and regenerate
        if wizard.health > 0:
            universal.MAP.printMap(player)
            print(f"\n{wizard.name}\'s turn!")
            time.sleep(2)

            wizard.regenerate()

            time.sleep(2)

            #Checks if the wizard needs to move
            if not universal.AOF.inRange(wizard.weapon.range, wizard, player):
                print('not in range')
                wizard.move(player)
                time.sleep(2)

            print('In range')

            wizard.attack(player)
            time.sleep(5)
            universal.MAP.updateMap(player)
            universal.MAP.printMap(player)

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

    universal.MAP.createMap(player, wizard)

    # Start the battle
    battle(player, wizard)
      

if __name__ == "__main__":
    main()
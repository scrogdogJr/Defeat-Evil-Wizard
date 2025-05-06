# About the Project
This game is a functional RPG game with a 30x30 game board. A player can pick from four character classes (Warrior, Mage, Dragon, and Artificer) each with their own unique abilities and traits to battle the Evil Wizard. The game is won by killing the Evil Wizard.

# Getting Started
## Installation
#### 1. Clone the repo
  `git clone https://github.com/scrogdogJr/Defeat-Evil_Wizard.git`
#### 2. Change git remote url to avoid accidental pushes to the base project
  ```
  git remote set-url origin github_username/repo_name
  git remote -v # confirm the changes
```

## Running
- Run in the terminal
- Press cmd + space on Mac, then search for "Terminal". Or, find "Windows Terminal" in the start menu on Windows
- On Mac, type:
    `python3 <file directory>.py`
- On Windows, type:
    `python <file directory>.py`

## Features
- Character class choice
- Character name choice
- Map board functionality
  - Tracks characters on tiles
  - Tracks items on tiles
  - Prints the map in a grid
  - Shows an item on a tile if it is visible to the character
- Move method
- Heal method
- View character stats method
- Attack method with randomized damage based on weapons and character stats
- Range checking for the melee or long-range weapons
- Different Character abilities and weapons:
- Warrior:
  - Weapon: Longsword
  - Special ability 1: Shield (Reduces damage taken by 75%)
  - Special ability 2: Extra Action (Allows for two actions in a turn)
- Dragon:
  - Weapon: Claws
  - Special ability 1: Tail Swipe (Deals damage and knocks down opponent)
  - Special ability 2: Fire Breath
- Mage:
  - Weapon: Glintstone Staff
  - Special ability 1: Teleport (Can move anywhere on the map)
  - Special ability 2: Invisibility (Becomes invisible for two rounds and cannot be attacked)
- Artificer:
  - Weapon: Unarmed Strike
  - Other action: Pick up two items (Can pick up two items in range and place them in the backpack)
  - Other action: Can equip a weapon or a valid item from the backpack
  - Special ability 1: Craft (Makes items or weapons from the material items picked up)
  - Special ability 2: Use Item (Can use an equipped item)
- Craftable Item List:
  - Speed Potion (Boosts total movement points)
  - Attack Power Potion (Boosts the attack power of the character)
  - Health Potion (Heals the character and boosts the max health)
  - Invisibility Potion (Same as invisibility special ability)
- Craftable Weapon List:
  - Electro Wand
  - Longsword
  - GLintstone Staff
  - Ice Dart (Consumable: deals damage and reduces the movement of the opponent by half of their max movement)
- Evil Wizard:
  - Weapon: Electro Wand
  - Special ability: Regenerate (Heals 5 health every turn with no maximum)
  - Seeking ability (If the player is out of range of the Evil Wizard, he will move his maximum movement to get as close to the player as possible)
  - After moving, the Evil Wizard attacks
### Highlighted Feature: 
- Animation for ranged weapons that shows the respective emoji for the weapon type going from the attacker to the defender. It always finds the path.

## Contact 
Email - anthony7101@cox.net/
Project link: https://github.com/scrogdogJr/Defeat-Evil_Wizard.git

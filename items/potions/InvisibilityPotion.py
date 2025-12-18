from items.CraftableItem import CraftableItem
from items.craftingMaterials import Water, Gem, Herb

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
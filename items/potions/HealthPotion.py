from items.CraftableItem import CraftableItem
from items.craftingMaterials import Water, Dirt, Herb

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
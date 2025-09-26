import CraftableItem
from craftingMaterials import Water, Maple

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
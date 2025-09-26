import CraftableItem
from craftableItems import Water, LadyBug

class SpeedPotion(CraftableItem):
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
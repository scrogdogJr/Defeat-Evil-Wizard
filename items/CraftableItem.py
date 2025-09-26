import Item
from abc import abstractmethod

class CraftableItem(Item):
    @abstractmethod
    def useItem(self, player):
        pass
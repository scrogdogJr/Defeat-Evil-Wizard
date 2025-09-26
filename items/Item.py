from abc import abstractmethod

class Item:
    # Items will be stored in a character's backpack which is a dictionary.
    # Each key will be the char (emoji representaiton) of the item
    # The value will represent how many of that item a character has
    def __init__(self, char, x=0, y=0, craft_cost: dict=None):
        self.char = ' ' + char
        self.craft_cost = craft_cost
        self.x = x
        self.y = y

    @abstractmethod
    def useItem(self, player):
        pass

    @abstractmethod
    def __str__(self):
        pass
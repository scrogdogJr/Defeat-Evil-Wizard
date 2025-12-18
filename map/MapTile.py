from typing import TYPE_CHECKING
from characters.Artificer import Artificer
    


# MapTile class that holds all the necessary data and methods for an individual tile
class MapTile:
    def __init__(self, x, y , character = None, item = None, showItem=False):
        self.tile_char = ' •'
        self.item = item
        self.character = character
        self.x = x
        self.y = y

        self.update_char(showItem=showItem)

    def remove_character(self):
        self.character = None
        self.update_char()

    def add_character(self, character):
        self.character = character
        self.update_char()

    def remove_item(self):
        self.item = None
        self.update_char()

    #Updates the char on the map. Shows a character if it is on the space. And, shows the item AND Artificer if they share a space. Allows a parameter
    #to dictate whether an item is shown elsewhere
    def update_char(self, char=' •', showItem=False):
        if (self.character != None): 
            if isinstance(self.character, Artificer) and self.item != None:
                self.tile_char = self.character.char[1:] + self.item.char[1:]
            else:
                self.tile_char = self.character.char
        elif (self.item != None and showItem == True):
            self.tile_char = self.item.char
        else: self.tile_char = ' ' + char
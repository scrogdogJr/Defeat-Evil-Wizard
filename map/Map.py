import random
from items.craftingMaterials import Stone, Gem, Wood, Herb, Maple, Ice, Water, Ladybug, Dirt, Sunflower
from characters.Artificer import Artificer
from AreaOfEffect import AreaOfEffect
from .MapTile import MapTile

# Map class manages a list of MapTile objects
class Map:

    raw_materials = (Stone, Gem, Wood, Herb, Maple, Ice, Water, Ladybug, Dirt, Sunflower, None)
    weights = (7, 0.5, 6.5, 3, 3, 2, 5, 3.5, 5.5, 3, 60)

    def __init__(self):
        # BE CAREFUL! The y coordinate goes first when this becomes a 2D list
        self.map_tiles = []


    # Creates and prints the map with the characters. Each map tile's coordinate is stored as the index in the 2D string    
    def createMap(self, player, evil_wizard):
        aof = AreaOfEffect()
        spaces = '  '

        # Makes sure the two characters are not on the same tile
        while player.isPositionEqual(evil_wizard.getx(), evil_wizard.gety):
            player.setPosition(random.randint(0, 29), random.randint(0, 29))

        # Print the spaces to account for y coordinate numbers
        print('\n\n    ', end='')

        # Prints the x coordinate numbers
        for x in range(30):
            if x >= 10: spaces = ' '
            print(f"{x}", end=spaces)
    
        spaces = ' '
        # Nested for loops to print out the map (30 x 30 tiles) and store in a 2D list in coordinate form
        for y in range(30):
            self.map_tiles.append([])
            if y >= 10: spaces = ''
            print(f'\n{y}', end=spaces)

            for x in range(30):

                item = random.choices(self.raw_materials, self.weights, k=1)
                if item[0] != None:
                    item[0] = item[0](x, y)
                showItem = isinstance(player, Artificer) and aof.inSight(x, y, player)

                random.choice
                # Checks if this is the coordinate of the player. If so, puts the character in that MapTile
                if player.isPositionEqual(y, x):
                    self.map_tiles[y].append(MapTile(x, y, player, item[0], showItem))
                    player_item = item[0]

                # Checks if this is the coordinate of the evil_wizard. If so, puts the evil wizard in that MapTile
                elif evil_wizard.isPositionEqual(y, x):
                    self.map_tiles[y].append(MapTile(x, y, evil_wizard, item[0], showItem))

                # If there are no characters or items on the coordinate, just makes it a normal tile space.
                else:
                    self.map_tiles[y].append(MapTile(x, y, item=item[0], showItem=showItem))

                # Checks if the player is an Artificer, if the current tile is to the right of the player, and if
                # there is an item on the players tile. If so, it takes away the leading space of the tile to the 
                # right of the artificer for formatting purposes
                if showItem and player.isPositionEqual(y, x - 1) and player_item != None:
                    print(self.map_tiles[y][x].tile_char[1:], end='')

                else:
                    print(f"{self.map_tiles[y][x].tile_char}", end='')
        print("\n\n")

    def updateMap(self, player):
        aof = AreaOfEffect()
        # Checks if the player is the Artificer. If so, it will check if items are in sight
        if isinstance(player, Artificer):
            for y in range(30):
                for x in range(30):
                    # Will update the char on the map and show the item if it is in sight of the Artificer
                    self.map_tiles[y][x].update_char(showItem=aof.inSight(x, y, player))
        else:
            for y in range(30):
                for x in range(30):
                    # Be CAREFUL! The y coordinate goes first
                    self.map_tiles[y][x].update_char()

    # Only Prints the map
    def printMap(self, player):
        spaces = '  '
        # Print the spaces to account for y coordinate numbers
        print('\n\n    ', end='')

        # Prints the x coordinate numbers
        for x in range(30):
            if x >= 10: spaces = ' '
            print(f"{x}", end=spaces)
    
        spaces = ' '
        # Nested for loops to print out the map (30 x 30 tiles) and store in a 2D list in coordinate form
        for y in range(30):
            if y >= 10: spaces = ''
            print(f'\n{y}', end=spaces)

            for x in range(30):

                #Same logic as in createMap()
                if isinstance(player, Artificer) and player.isPositionEqual(y, x - 1) and self.map_tiles[y][x - 1].item != None:
                    print(self.map_tiles[y][x].tile_char[1:], end='')

                else:
                    # Be CAREFUL! The y coordinate goes first
                    print(f"{self.map_tiles[y][x].tile_char}", end='')
        print("\n\n")
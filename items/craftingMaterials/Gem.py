from items.Item import Item

class Gem(Item):
    def __init__(self, x=0, y=0):
        super().__init__('💎', x, y)

    def __str__(self):
        return "Diamond"
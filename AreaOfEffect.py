import math

class AreaOfEffect:

    # Checks if an attacker is in melee range to a defender
    def isMelee(self, attacker, defender):
        if ((attacker.getx() == defender.getx() - 1 or attacker.getx() == defender.getx() + 1 or attacker.gety() == defender.gety() - 1 or attacker.gety() == defender.gety() + 1) and defender.invisible <= 0):
            return True
        else:
            return False
        
    def inRange(self, range, attacker, defender):
        distance = round(math.hypot(attacker.getx() - defender.getx(), attacker.gety() - defender.gety()))

        if (distance <= range and defender.invisible <= 0):
            return True
        else:
            return False
        
    def findSightRange(self, character, sight_radius=1):
        x_start = max(character.getx() - sight_radius, 0)
        x_end = min(character.getx() + sight_radius, 29)
        y_start = max(character.gety() - sight_radius, 0)
        y_end = min(character.gety() + sight_radius, 29)

        return x_start, x_end, y_start, y_end

    def inSight(self, x, y, character, sight_radius=1):
        # Creates a rannge of coordinates around the intended character with the defined radius
        x_start, x_end, y_start, y_end = self.findSightRange(character, sight_radius) 

        # If the coordinate is within both the x and y range, then the coordinate is in sight
        if x in range(x_start, x_end + 1) and y in range(y_start, y_end + 1):
            return True

        # Else, the coordinate is not in sight
        else:
            return False
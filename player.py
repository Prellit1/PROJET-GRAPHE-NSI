from base import distance2
from math import sqrt
from tile import Tileset

RENT = 30


class Player:
    def __init__(self, home_node):
        self.endurance = 100
        self.max_endurance = 100
        self.money = 100
        self.score = 100
        self.gains = 10
        self.home_node = home_node
        self.current_node = home_node
        self.x = self.current_node.x
        self.y = self.current_node.y
        self.play_count = 0
        self.tileset = Tileset("graphics/Character.png")

    def increase_stat(self, item):
        stat = item[0].lower()
        if stat == "endurance":
            self.max_endurance += item[1]
        elif stat == "gains":
            self.gains += item[1]

    def move(self, target_node, map):
        distances, _ = map.dijkstra(self.current_node)
        distance = distances[target_node]
        self.endurance -= distance // 10
        if self.endurance < 0:
            self.money -= distance // 20
            if self.money < 0: 
                self.money = 0
            self.current_node = self.home_node
            self.endurance = 100
        else:
            self.current_node = target_node

        
        self.x = self.current_node.x
        self.y = self.current_node.y

    def get_node_type(self):
        retval = "H"
        if self.current_node.value == 0:
            retval = "F"
        elif self.current_node.value == 1:
            retval = "U"
        elif self.current_node.value == 2:
            retval = "B"

        if retval != "H":
            self.play_count = (self.play_count + 1) % 5
            if not self.play_count:
                self.money -= RENT
                if self.money < 0:
                    self.status = "G_O"
                else:
                    self.score += RENT

        return retval
    
    def get_pay(self):
        addition = self.gains + sqrt(distance2((self.current_node.x, self.current_node.y), (self.home_node.x, self.home_node.y))) // 25
        self.score += addition
        self.money += addition
    
    def render(self, screen, OffsX = 0, OffsY = 0):
        screen.blit(self.tileset.get_tile(0,0), (self.x + OffsX, self.y + OffsY - 32))
        screen.blit(self.tileset.get_tile(0,1), (self.x + OffsX, self.y + OffsY))

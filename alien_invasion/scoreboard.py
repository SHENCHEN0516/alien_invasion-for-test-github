from pygame.sprite import Group
from pygame.sprite import Sprite
from ship import Ship

class Scoreboard:
    def __init__(self,ai_game):
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.stats=ai_game.stats
       
        self.ai_game=ai_game
        self.prep_ships()

    def prep_ships(self):
        """显示剩余飞船数量"""
        self.ships=Group()
        for ship_number in range(self.stats.ships_left):
            ship=Ship(self.ai_game)
            ship.rect.x=10+ship_number*ship.rect.width
            ship.rect.y=10
            self.ships.add(ship)

    def show_score(self):
        self.ships.draw(self.screen)
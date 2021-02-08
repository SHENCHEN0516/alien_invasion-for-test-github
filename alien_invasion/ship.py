import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船的类"""
    def __init__(self,ai_game):
        """初始化飞船和位置"""
        super().__init__()
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.settings=ai_game.settings

        #加载飞船图像并获取矩形
        self.image=pygame.image.load("images/ship.bmp")
        self.rect=self.image.get_rect()

        #新飞船放在屏幕底部中央
        self.rect.midbottom=self.screen_rect.midbottom

        #飞船x坐标存储小数(fail?)
        #self.x=float(self.rect.x)
        
        #移动flag
        self.moving_right=False
        self.moving_left=False
        self.moving_up=False
        self.moving_down=False

    def update(self):
        """根据flag调整飞船位置"""
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        if self.moving_left and self.rect.left>0:
            self.rect.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top>0:
            self.rect.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom<self.screen_rect.bottom:
            self.rect.y += self.settings.ship_speed

        #self.rect.x=self.x

    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def reset_ship(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)
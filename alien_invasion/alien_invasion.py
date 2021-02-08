import sys
import pygame
from random import randint
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard

class AlienInvasion:
    """管理游戏资源和行为"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init() #初始化

        self.settings=Settings()
        self.screen=pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion") #程序标题
        self.stats=GameStats(self) 
        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()
        self.sb=Scoreboard(self)


    def run_game(self):
        """游戏主循环"""
        while True:  
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            #self._create_fleet() #写在这里会卡顿


    def _check_events(self):
        """按键响应"""
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        """按键响应"""
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_UP:
            self.ship.moving_up=True
        elif event.key==pygame.K_DOWN:
            self.ship.moving_down=True
        elif event.key==pygame.K_ESCAPE: #快捷键按esc退出游戏
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
        elif event.key==pygame.K_p:
            self._game_replay()
    
    def _check_keyup_events(self,event):
        """松开响应"""
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False
        elif event.key==pygame.K_UP:
            self.ship.moving_up=False
        elif event.key==pygame.K_DOWN:
            self.ship.moving_down=False
        

    def _fire_bullet(self):
        """创建新子弹并加入编组"""
        new_bullet=Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹位置并删除消失的子弹""" 
        self.bullets.update()
        #删除消失的子弹
        for bullet_a in self.bullets.copy():
            if bullet_a.rect.bottom<=0:
                self.bullets.remove(bullet_a) 
        ###书里的bullet_a是bullet，会报错

        #检查子弹和外星人的碰撞
        collsions=pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,True)

        if not self.aliens: #空编组相当于false
        #删除现有子弹并且重新生成外星人
            self.bullets.empty()
            self._create_fleet()


    def _update_aliens(self):
        """更新外星人位置"""
        self._check_fleet_edges()
        self.aliens.update()
        #检测外星人和飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()


    def _create_fleet(self):
        """创建外星人群"""
        alien=Alien(self)
        alien_width=alien.rect.width
        alien_height=alien.rect.height
        #计算一行可容纳的外星人数量
        available_space_x=self.settings.screen_width-(2*alien_width)
        number_aliens_x=available_space_x//(2*alien_width)
        #计算可容纳外星人行数
        ship_height=self.ship.rect.height
        available_space_y=(self.settings.screen_height-
            (3*alien_height)-ship_height)
        number_rows=available_space_y//(2*alien_height)

        #随机创建外星人
        # number_aliens=randint(0,10)
        # for alien_a in range(number_aliens):
        #     row_number= randint(0,number_rows)
        #     column_number=randint(0,number_aliens_x)
        #     self._create_alien(column_number,row_number)
        #创建外星人
        for row_number in range(number_rows):
            for column_number in range(number_aliens_x):
                self._create_alien(column_number,row_number)

    def _create_alien(self,column_number,row_number):
        """创建一个外星人,放在指定位置"""
        alien=Alien(self)
        alien_width=alien.rect.width
        alien_height=alien.rect.height
        alien.x=alien_width+2*alien_width*column_number
        alien.rect.x=alien.x
        alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """外星人到达屏幕边缘的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _ship_hit(self):
        """飞船与外星人碰撞的响应"""
        if self.stats.ships_left>0:
            self.stats.ships_left-=1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.reset_ship()
            sleep(1.0)
        else:
            self.stats.game_active=False

    def _check_aliens_bottom(self):
        """检查外星人到达屏幕底端"""
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                self._ship_hit()
                break

    def _game_replay(self):
        """重新开始游戏"""
        self.stats.reset_stats()
        self.stats.game_active=True
        self.sb.prep_ships()
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.reset_ship()

    def _update_screen(self):
        """更新屏幕图像，刷新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        #让屏幕可见
        pygame.display.flip()

    

if __name__=="__main__":
    #创建游戏实例并运行
    ai=AlienInvasion()
    ai.run_game()
from plane_sprites import *
import pygame
import warnings

BA = 0

class PlaneGame(object):

    def __init__(self):
        pygame.init()
        print("游戏初始化...")
        #1.创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        #2.创建游戏时钟
        self.clock = pygame.time.Clock()
        #3.调用私有方法,精灵和精灵组创建
        self.__create_sprites()
        #4.设置定时器时间 - 创建敌机 1s一架
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)
        pygame.time.set_timer(BOOMSUPPLY_EVENT, 10000)

    def __create_sprites(self):
        #绘制背景
        bg1 = Background()
        bg2 = Background(True)

        self.back_group = pygame.sprite.Group(bg1,bg2)

        #创建敌机精灵组
        self.enemy = Enemy()
        self.enemy_group = pygame.sprite.Group()

        #创建英雄
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

        #创建炸弹掉落精灵组
        self.boomsupply_group = pygame.sprite.Group()

        #炸弹图标
        self.BoomIcon = BoomIcon()
        self.boomIcon_group = pygame.sprite.Group(self.BoomIcon)

    def start_game(self):
        print("游戏开始！")


        while True:
            #1.设置刷新率
            self.clock.tick(FRAME_PER_SEC)
            #2.事件监听
            self.__event_handler()
            #3.碰撞检测
            self.__check_collide()
            #4.更新/检测精灵组
            self.__update_sprites()

            self.BoomActive()
            #5.显示更新
            pygame.display.update()

    def BoomActive(self):
        global BA
        if BA > 0:
            for event in pygame.event.get():
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_SPACE]:
                    BA = BA - 1
                    print(BA)
                    self.enemy_group.remove(self.enemy,self.enemy_group)


    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                print("敌机出场...")
                #创建敌机精灵
                enemy = Enemy()
                #将敌机精灵添加到低级精灵组
                self.enemy_group.add(enemy)
            elif event.type == BOOMSUPPLY_EVENT:
                print("炸弹掉落...")
                boom = BoomSupply()
                self.boomsupply_group.add(boom)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):
        #1.子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        #2.英雄拾取炸弹
        Boom_collect = pygame.sprite.groupcollide(self.hero_group, self.boomsupply_group,False,True)
        #判断列表是否有内容
        global BA
        if len(Boom_collect) > 0:
            if BA <= 2:
                BA = BA + 2
                print(BA)
        #3.敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group,True)
        #判断列表时候有内容
        if len(enemies) > 0:
            self.hero.kill()

            #结束游戏
            PlaneGame.__game_over()

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

        self.boomsupply_group.update()
        self.boomsupply_group.draw(self.screen)

        self.boomIcon_group.update()
        self.boomIcon_group.draw(self.screen)

    @staticmethod
    def __game_over():
        print("游戏结束")
        print("英雄牺牲！")

        pygame.quit()
        exit()
        warnings.filterwarnings("ignore")

if __name__ == '__main__':
    game = PlaneGame()

    game.start_game()

import pygame
import random

#屏幕大小的常量
SCREEN_RECT = pygame.Rect(0,0,480,700)
#刷新的帧率
FRAME_PER_SEC = 60
#创建敌机定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
#英雄发射子弹的事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1
#炸弹发射时机
BOOMSUPPLY_EVENT = pygame.USEREVENT + 2

BA = 0

class GameSprite(pygame.sprite.Sprite):

    def __init__(self,image_name,speed=1):

        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class Background(GameSprite):

    def __init__(self, is_alt=False):

        #1.调用父类方法实现精灵的创建
        super().__init__("./images/background.png")

        #2.判断是否是交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        #1.调用父类方法实现
        super().update()

        #2.判断图像是否移出屏幕，并将图片调到屏幕上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):

    def __init__(self):

        #1.调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__("./images/enemy1.png")

        #2.指定敌机的初始随机速度
        self.speed = random.randint(1,3)
        #3.指定敌机的初始随机位置
        self.rect.bottom = 0

        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):

        #1.调用父类方法，保持垂直方向的飞行
        super().update()
        #2.判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            print("飞出屏幕，删除敌机...")
        #kill方法将飞机从精灵组中移除
            self.kill()


class BoomSupply(GameSprite):

    def __init__(self):
        # 1.调用父类方法，创建炸弹精灵，同时指定炸弹图片
        super().__init__("./images/bomb_supply.png",7)

        # 2.指定炸弹的初始随机位置
        self.rect.bottom = 0

        #3.随机指定炸弹位置
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):

        #1.调用父类方法，保持垂直方向的飞行
        super().update()
        #2.判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            print("飞出屏幕，删除炸弹...")
        #kill方法将飞机从精灵组中移除
            self.kill()


class Hero(GameSprite):

    def __init__(self):

        #1.调用父类方法，设置image&speed
        super().__init__("./images/fighter.png", 0)
        #2.设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        #3.创建子弹的精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):

        #英雄水平方向移动
        self.rect.x += self.speed

        #控制英雄移动边界
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        print("发射子弹...")

        # 1.创建子弹精灵
        bullet = Bullet()

        # 2.设置精灵的位置
        bullet.rect.bottom = self.rect.y
        bullet.rect.centerx = self.rect.centerx

        # 3.将精灵添加到精灵组
        self.bullets.add(bullet)


class Bullet(GameSprite):

    def __init__(self):

        #调用父类方法，设置子弹图片，设置初始速度
        super().__init__("./images/bullet1.png", -2)

    def update(self):

        #调用父类方法，让子弹沿垂直方向飞行
        super().update()

        #判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        print("子弹被销毁...")


class BoomIcon(GameSprite):

    def __init__(self):

        super().__init__("./images/bomb.png",0)

        # 炸弹图标位置
        self.rect.x = 400
        self.rect.y = 600

    def update(self):

        pass

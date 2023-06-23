import pygame
import random
import unittest

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.Surface((WIDTH, HEIGHT))
player_image = pygame.Surface((32, 32))
pygame.draw.rect(player_image, (255, 255, 255), pygame.Rect(0, 0, 32, 32))
meteor_image = pygame.Surface((32, 32))
pygame.draw.rect(meteor_image, (255, 255, 255), pygame.Rect(0, 0, 32, 32))
bullet_image = pygame.Surface((8, 16))
pygame.draw.rect(bullet_image, (255, 255, 255), pygame.Rect(0, 0, 8, 16))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = meteor_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (
            self.rect.top > HEIGHT + 10
            or self.rect.left < -25
            or self.rect.right > WIDTH + 22
        ):
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.player = Player()

    def test_initial_position(self):
        self.assertEqual(self.player.rect.centerx, WIDTH // 2)
        self.assertEqual(self.player.rect.bottom, HEIGHT - 10)

    def test_update_move_left(self):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
        self.player.update()
        self.assertEqual(self.player.speed_x, -5)
        self.assertEqual(self.player.rect.x, WIDTH // 2 - 5)

    def test_update_move_right(self):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
        self.player.update()
        self.assertEqual(self.player.speed_x, 5)
        self.assertEqual(self.player.rect.x, WIDTH // 2 + 5)

    def test_update_stop_moving(self):
        self.player.speed_x = 5
        self.player.update()
        self.assertEqual(self.player.speed_x, 0)
        self.assertEqual(self.player.rect.x, WIDTH // 2 + 0)


class MeteorTestCase(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.meteor = Meteor()

    def test_initial_position(self):
        self.assertLessEqual(self.meteor.rect.x, WIDTH - self.meteor.rect.width)
        self.assertGreaterEqual(self.meteor.rect.y, -100)
        self.assertLessEqual(self.meteor.rect.y, -40)

    def test_update(self):
        initial_x = self.meteor.rect.x
        initial_y = self.meteor.rect.y
        self.meteor.update()
        self.assertNotEqual(self.meteor.rect.x, initial_x)
        self.assertNotEqual(self.meteor.rect.y, initial_y)


class BulletTestCase(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.bullet = Bullet(WIDTH // 2, HEIGHT - 10)

    def test_initial_position(self):
        self.assertEqual(self.bullet.rect.y, HEIGHT - 10)
        self.assertEqual(self.bullet.rect.centerx, WIDTH // 2)

    def test_update(self):
        initial_y = self.bullet.rect.y
        self.bullet.update()
        self.assertNotEqual(self.bullet.rect.y, initial_y)
        self.assertLess(self.bullet.rect.bottom, HEIGHT)


if __name__ == "__main__":
    all_sprites = pygame.sprite.Group()
    meteor_list = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for _ in range(8):
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    unittest.main()


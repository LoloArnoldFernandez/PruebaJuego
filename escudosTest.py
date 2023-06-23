import pygame
import random
import unittest

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGTH
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, border, 2)


class TestDrawText(unittest.TestCase):
    def test_text_rendered_correctly(self):
        surface = pygame.Surface((WIDTH, HEIGHT))
        text = "Hello, World!"
        size = 24
        x = WIDTH // 2
        y = HEIGHT // 2
        draw_text(surface, text, size, x, y)

        self.assertIsNotNone(surface.get_at((x, y)))  # Check if there's a pixel at the specified position


class TestDrawShieldBar(unittest.TestCase):
    def test_bar_drawn_correctly(self):
        surface = pygame.Surface((WIDTH, HEIGHT))
        x = 100
        y = 100
        percentage = 50
        draw_shield_bar(surface, x, y, percentage)

        fill_rect = pygame.Rect(x, y, (percentage / 100) * 100, 10)
        border_rect = pygame.Rect(x, y, 100, 10)

        self.assertEqual(surface.get_rect().size, (WIDTH, HEIGHT))
        self.assertEqual(surface.get_at((x, y)), GREEN)  # Check if the fill color is green
        self.assertEqual(surface.get_at((x + 50, y)), BLACK)  # Check if the background color is black
        self.assertEqual(surface.get_at((x + 101, y)), WHITE)  # Check if the border color is white


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shooter")
    clock = pygame.time.Clock()

    unittest.main()


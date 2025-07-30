import pygame
import game


# Maybe inherit from Actor?
class Tile:
    def __init__(self, sprite: pygame.Surface, walkable: bool = True, effects = []):
        self.sprite = sprite
        self.walkable = walkable
        self.effects = effects
    
    def give_effects(self, actor: game.GameActor):
        pass
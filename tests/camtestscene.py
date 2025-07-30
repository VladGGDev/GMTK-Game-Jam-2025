from engine import DrawPass, Scene
import engine
import pygame
import random
from engine.spritesheet import SpriteSheet


class CameraTestScene(Scene):
    def __init__(self, num_squares = 30, max_dist = 256, max_size = 100):
        super().__init__([])
        self.squares = list[pygame.Rect]()
        for _ in range(num_squares):
            self.squares.append(pygame.Rect(
                (random.randrange(-max_dist, max_dist), random.randrange(-max_dist, max_dist)),
                (random.randrange(10, max_size), random.randrange(10, max_size))))
        self.sprite_sheet = SpriteSheet("tests/sprites/SpriteSheetTestSprite.png", (8, 8), (1, 1), (1, 1))
    
    def update(self):
        if engine.get_key_down(pygame.K_ESCAPE):
            engine.running = False
        
        # WASD controls
        cammove = (engine.get_key(pygame.K_d) - engine.get_key(pygame.K_a), engine.get_key(pygame.K_s) - engine.get_key(pygame.K_w))
        engine.draw_passes["Main"].camera.position += pygame.Vector2(cammove)
        
        if engine.get_key_down(pygame.K_SPACE):
            engine.draw_passes["Main"].camera.resolution = (128, 128)
        if engine.get_key_up(pygame.K_SPACE):
            engine.draw_passes["Main"].camera.resolution = (256, 256)
        
        # Zoom in and out
        engine.draw_passes["Main"].camera.height += engine.get_key(pygame.K_q) - engine.get_key(pygame.K_e)
    
    def draw(self):
        engine.draw_passes["Main"].blit(99, DrawPass.get_pixel(pygame.Color("red")), (0, 0))
        engine.draw_passes["Main"].blit(1, self.sprite_sheet.texture, (0, 0), (3, 1), engine.total_time * 20, (0, 0.5), self.sprite_sheet.get_rect(5))
        # engine.draw_passes["Main"].blit(1, DrawPass.get_pixel(pygame.Color("cornflowerblue")), (0, 0), (100, 100), engine.total_time * 20, (0.75, 0.5))
        # engine.draw_passes["Main"].blit(1, DrawPass.get_pixel(pygame.Color("cornflowerblue"), (100, 100)), (0, 0), (1, 1), engine.total_time * 20, (0.75, 0.5))
        # engine.draw_passes["Main"].blit(1, DrawPass.get_pixel(pygame.Color("cornflowerblue"), (10, 10)), (0, 0), (10, 10), engine.total_time * 20, (0.75, 0.5))
        for sq in self.squares:
            engine.draw_passes["Main"].blit(0, DrawPass.get_pixel(pygame.Color(255, 255, 255, 128)), sq.center, sq.size)
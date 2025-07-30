from engine import DrawPass, Scene
import engine, pygame, random
from engine.spritesheet import SpriteSheet
from game.actors.car import Car


class CarTestScene(Scene):
    def __init__(self, num_squares = 30, max_dist = 256, max_size = 100):
        super().__init__([Car()])
        self.squares = list[pygame.Rect]()
        for _ in range(num_squares):
            self.squares.append(pygame.Rect(
                (random.randrange(-max_dist, max_dist), random.randrange(-max_dist, max_dist)),
                (random.randrange(10, max_size), random.randrange(10, max_size))))
        self.sprite_sheet = SpriteSheet("tests/sprites/SpriteSheetTestSprite.png", (8, 8), (1, 1), (1, 1))
    
    def update(self):
        if engine.get_key_down(pygame.K_ESCAPE):
            engine.running = False
        super().update()
        
        # # WASD controls
        # cammove = (engine.get_key(pygame.K_d) - engine.get_key(pygame.K_a), engine.get_key(pygame.K_s) - engine.get_key(pygame.K_w))
        # engine.draw_passes["Main"].camera.position += pygame.Vector2(cammove)
        
        # if engine.get_key_down(pygame.K_SPACE):
        #     engine.draw_passes["Main"].camera.resolution = (128, 128)
        # if engine.get_key_up(pygame.K_SPACE):
        #     engine.draw_passes["Main"].camera.resolution = (256, 256)
        
        # # Zoom in and out
        # engine.draw_passes["Main"].camera.height += engine.get_key(pygame.K_q) - engine.get_key(pygame.K_e)
    
    def draw(self):
        engine.draw_passes["Main"].blit(99, DrawPass.get_pixel(pygame.Color("red")), (0, 0))
        for sq in self.squares:
            engine.draw_passes["Main"].blit(0, DrawPass.get_pixel(pygame.Color(255, 255, 255, 128)), sq.center, sq.size)
        
        super().draw()
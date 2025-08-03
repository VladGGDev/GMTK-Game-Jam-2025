import engine, pygame
from engine.spritesheet import SpriteSheet
import engine.collider as collider
from game.utility.circlecollidersolver import solve_all_circle_collisions
import random

class Enemy(engine.Actor):

    graphic = SpriteSheet("game/sprites/Zombie.png", (8, 8))
    MAX_SPEED = 40
    MIN_SPEED = 30
    
    def __init__(self,
                 position : pygame.Vector2,
                 speed : int):
        self.speed = speed
        self.position = position
        self.source = random.randint(0,1)

    def start(self):
        self.collider = collider.CircleCollider(self.position,4,"Enemy")

    def fixed_update(self, car_pos:pygame.Vector2):
        direction  = car_pos - self.collider.position

        if direction.length_squared() != 0:
            direction = direction.normalize()
            self.collider.position = direction * self.speed * engine.delta_time()
        
    def draw(self):
        engine.draw_passes["Main"].blit(
            self.collider.position.y,Enemy.graphic.texture,self.collider.position,source_rect=self.source
        )


    

    
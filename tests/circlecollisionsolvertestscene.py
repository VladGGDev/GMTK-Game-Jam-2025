import engine, pygame
from engine.collider import CircleCollider, all_colliders
from game.utility.circlecollidersolver import *


class CircleCollisionSolverTestScene(engine.Scene):
    def __init__(self):
        super().__init__([])
    
    def start(self):
        super().start()
        self.colliders = [
            CircleCollider(pygame.Vector2(0, -100), 10),
            CircleCollider(pygame.Vector2(0, -100), 10),
            
            CircleCollider(pygame.Vector2(-10, -50), 10),
            CircleCollider(pygame.Vector2(10, -50), 10),
            
            CircleCollider(pygame.Vector2(-5, 0), 10),
            CircleCollider(pygame.Vector2(5, 0), 10),
            
            CircleCollider(pygame.Vector2(0, 50), 10),
            CircleCollider(pygame.Vector2(5, 50), 10),
            
            CircleCollider(pygame.Vector2(-10, 100), 10),
            CircleCollider(pygame.Vector2(10, 100), 30, "unmovable"),
        ]
    
    def update(self):
        if engine.get_key_down(pygame.K_ESCAPE):
            engine.running = False

        if engine.get_key_down(pygame.K_SPACE):
            solve_all_circle_collisions({"unmovable"})
    
    def draw(self):
        for coll in self.colliders:
            engine.draw_passes["Main"].blit(
                0,
                engine.DrawPass.get_circle(pygame.Color("gray"), coll.radius),
                coll.position
            )
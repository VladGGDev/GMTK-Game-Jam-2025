import engine, pygame, engine.collider as colliders
from math import pi, sin, cos, degrees


class Car(engine.Actor):
    def __init__(self):
        # Constants
        self.MAX_SPEED = 256
        self.MIN_SPEED = 64
        self.ACCELERATION = self.MAX_SPEED / 0.25
        self.DECELERATION = self.MAX_SPEED / 1
        self.FRICTION_DECELERATION = self.MAX_SPEED / 5
        self.TURN_SPEED = 160 * pi / 180 # radians per second
        self.DRIFT_TURN_SPEED = 450 * pi / 180 # radians per second
        
        # Collider initialization
        super().__init__(colliders.CircleCollider(pygame.Vector2(0, 0), 4, "Car"))
        
        # Dynamic values
        self.direction = 0
        self.speed = self.MIN_SPEED
    
    def update(self):
        # key_down = engine.get_key_down
        key_held = engine.get_key
        
        if key_held(pygame.K_w) or key_held(pygame.K_UP):
            self.speed += self.ACCELERATION * engine.delta_time()
        elif key_held(pygame.K_s) or key_held(pygame.K_DOWN):
            self.speed -= self.DECELERATION * engine.delta_time()
        else:
            self.speed -= self.FRICTION_DECELERATION * engine.delta_time()
        self.speed = pygame.math.clamp(self.speed, self.MIN_SPEED, self.MAX_SPEED)            
        
        dir = int(key_held(pygame.K_a) or key_held(pygame.K_LEFT)) - int(key_held(pygame.K_d) or key_held(pygame.K_RIGHT))
        turn = self.DRIFT_TURN_SPEED if key_held(pygame.K_SPACE) else self.TURN_SPEED
        self.direction += dir * turn * engine.delta_time() * (self.speed / self.MAX_SPEED)
        
        engine.draw_passes["Main"].camera.position = self.collider.position
    
    def fixed_update(self):
        move = self.speed * engine.delta_time()
        self.collider.position += pygame.Vector2(
            move * -sin(self.direction),
            move * -cos(self.direction)
        )
    
    def draw(self):
        engine.draw_passes["Main"].blit(
            99,
            engine.DrawPass.get_pixel(pygame.Color("red"), (8, 12)),
            self.collider.position,
            (1, 1),
            degrees(self.direction + (pi / 1.75 if engine.get_key(pygame.K_SPACE) else 0))
        )
import engine, pygame, engine.collider as colliders, engine.tweening.lerpfuncs as lerputil, engine.tweening.easingfuncs as easings
from math import pi, sin, cos, degrees


class Car(engine.Actor):
    def __init__(self):
        # Constants
        self.MAX_SPEED = 150
        self.MAX_DRIFT_SPEED = 200
        self.MIN_SPEED = 80
        self.ACCELERATION = self.MAX_SPEED / 0.25
        self.DECELERATION = self.MAX_SPEED / 1
        self.FRICTION_DECELERATION = self.MAX_SPEED / 5
        self.TURN_SPEED = 120 * pi / 180 # radians per second
        self.DRIFT_TURN_SPEED = 270 * pi / 180 # radians per second
        self.MAX_DRIFT_ENERGY = 1 # Seconds of drift
        
        # Other initialization
        super().__init__(colliders.CircleCollider(pygame.Vector2(0, 0), 4, "Car"))
        self.texture = pygame.image.load("game/sprites/Masina.png")
        
        # Dynamic values
        self.direction = 0
        self.speed = self.MIN_SPEED
        self.drift_energy = 0
        self.last_dir = 0
    
    def update(self):
        pressed = engine.get_key
        
        dir = int(pressed(pygame.K_a) or pressed(pygame.K_LEFT)) - int(pressed(pygame.K_d) or pressed(pygame.K_RIGHT))
        if dir != 0: self.last_dir = dir
        max_sp = lerputil.lerp(self.MAX_SPEED, self.MAX_DRIFT_SPEED, easings.ease_out_cubic(self.drift_energy / self.MAX_DRIFT_ENERGY))
        turn_sp = self.TURN_SPEED if not pressed(pygame.K_SPACE) else self.DRIFT_TURN_SPEED
        
        # Drift energy
        self.drift_energy = max(self.drift_energy - engine.delta_time(), 0)
        if pressed(pygame.K_SPACE) and dir != 0:
            self.drift_energy = self.MAX_DRIFT_ENERGY
        
        
        # Acceleration controls
        if pressed(pygame.K_w) or pressed(pygame.K_UP) or self.drift_energy > 0:
            self.speed += self.ACCELERATION * engine.delta_time()
        elif pressed(pygame.K_s) or pressed(pygame.K_DOWN):
            self.speed -= self.DECELERATION * engine.delta_time()
        else:
            self.speed -= self.FRICTION_DECELERATION * engine.delta_time()
        self.speed = pygame.math.clamp(self.speed, self.MIN_SPEED, max_sp)            
        
        # Steering controls
        self.direction += dir * turn_sp * engine.delta_time() * (self.speed / max_sp)
        
        # Move camera to position
        # engine.draw_passes["Main"].camera.position = self.collider.position
        # Framerate-independent damping
        engine.draw_passes["Main"].camera.position = lerputil.vector2_lerp(
            pygame.Vector2(engine.draw_passes["Main"].camera.position),
            self.collider.position,
            1 - 0.005**engine.delta_time())
    
    def fixed_update(self):
        move = self.speed * engine.fixed_delta_time()
        self.collider.position += pygame.Vector2(
            move * -sin(self.direction),
            move * -cos(self.direction)
        )
    
    def draw(self):
        engine.draw_passes["Main"].blit(
            self.collider.position.y,
            self.texture,
            # engine.DrawPass.get_pixel(pygame.Color("red" if self.drift_energy > 0 else "blue"), (8, 12)),
            self.collider.position,
            (1, 1),
            degrees(self.direction + (pi / 2.5 * self.last_dir if self.drift_energy / self.MAX_DRIFT_ENERGY > 0.5 else 0))
        )
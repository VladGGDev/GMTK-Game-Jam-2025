import engine, pygame, engine.collider as colliders, engine.tweening.lerpfuncs as lerputil, engine.tweening.easingfuncs as easings
from math import pi, sin, cos, degrees
import random

class CameraManager(engine.Actor):
    
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)
        self.target_offset = pygame.Vector2(0, 0)
        self.shake_duration = 0
        self.shake_intensity = 0
        self.lerp_speed = 0.5
        super().__init__()


    def update(self):
        if self.shake_duration > 0:
            self.offset.x = random.randint(-self.shake_intensity, self.shake_intensity)
            self.offset.y = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_duration -= engine.delta_time()
        else:
            self.offset = pygame.Vector2(0, 0)

        self.offset = lerputil.vector2_lerp(self.offset, self.target_offset, self.lerp_speed)
        

        # Move camera to position
        # engine.draw_passes["Main"].camera.position = self.collider.position
        # Framerate-independent damping

        camera = engine.draw_passes["Main"].camera
        target_pos = self.collider.position + self.offset
        camera.position = lerputil.vector2_lerp(
            camera.position,
            target_pos,
            1 - 0.005 ** engine.delta_time()
        )

    def start_shake(self,duration:float,intensity:float):
        self.shake_duration = duration
        self.shake_intensity = intensity


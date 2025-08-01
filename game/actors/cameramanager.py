import engine
import pygame
import engine.tweening.lerpfuncs as lerp
from engine.shake import BaseShake


class CameraManager(engine.Actor):
    
    def __init__(self):
        self.shake_list : list[BaseShake] = []
        self.offset = pygame.Vector2(0,0)
        self.offset_target = pygame.Vector2(0,0)
        self.lerp_speed = 0.5
        super().__init__()


    def update(self):
        blended = pygame.Vector2(0,0)
        for shake in self.shake_list:
            blended += shake.update()
        shake_list = [shake for shake in self.shake_list if not shake.is_done()]
        # if shake_list:
        #     blended /= len(shake_list)
        self.offset_target = blended

        # Move camera to position
        # engine.draw_passes["Main"].camera.position = self.collider.position
        # Framerate-independent damping
    
        self.offset = lerp.vector2_lerp(self.offset, self.offset_target, self.lerp_speed)
 
        camera = engine.draw_passes["Main"].camera
        camera.position = lerp.vector2_lerp(
            camera.position,
            self.collider.position,
            1 - 0.005 ** engine.delta_time()
        )
        camera.position = lerp.vector2_lerp(
            camera.position,
            self.offset,
            1 - 0.005 ** engine.delta_time()
        )

    def add_shake(self, shake: BaseShake):
        self.shake_list.append(shake)
    

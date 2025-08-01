import engine,pygame
from game.actors.cameramanager import CameraManager
from engine.shake import SineShake,RandomShake

class ShakeTest(engine.Scene):
    def __init__(self):
        self.position = pygame.Vector2(0,0)
        self.CameraManager = CameraManager()
        super().__init__([self.CameraManager])
    
    def update(self):
        super().update()
        if engine.get_key_down(pygame.K_ESCAPE):
            engine.running = False

        if engine.get_key_down(pygame.K_SPACE):
            self.CameraManager.add_shake(SineShake(5,5,10))

        if engine.get_key_down(pygame.K_c):
            self.CameraManager.add_shake(RandomShake(5,5))
            
    
    def draw(self):
            engine.draw_passes["Main"].blit(
                0,
                engine.DrawPass.get_circle(pygame.Color("gray"), 9),
                self.position 
            )
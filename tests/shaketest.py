import engine,pygame
from game.actors.cameramanager import CameraManager

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
            self.CameraManager.start_shake(5,5)

        if engine.get_key_down(pygame.K_c):
            self.CameraManager.start_shake(1,100)
            
    
    def draw(self):
            engine.draw_passes["Main"].blit(
                0,
                engine.DrawPass.get_circle(pygame.Color("gray"), 9),
                self.position 
            )
import engine, engine.collider, pygame, math
from game.actors.ui import Text

class ScoreManager(engine.Actor):
    def __init__(self) -> None :
        super().__init__()
        self.score: int = 0
        self.total_distance: float = 0
        self.drift_distance: float = 0
        self.total_loops: int = 0
        self.font = pygame.font.Font("game/fonts/DigitalDisco.ttf", 32)
    
    def draw(self):
        position = Text.get_position("UI", (0.5, 0.1))
        engine.draw_passes["UI"].blit(
            -1,
            self.font.render(str(self.score), False, pygame.Color("black")),
            (position[0] + math.sin(engine.total_time * 1.5) * 5, position[1] + math.sin(engine.total_time * 3) * 5),
        )
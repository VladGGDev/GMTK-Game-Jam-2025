import engine, pygame
from engine.tweening import Tween, TweenSequence, easingfuncs
from game.actors.ui import Button, Text
from game.actors.scoremanager import ScoreManager


class GameEndMenu(engine.Actor):
    def __init__(self):
        super().__init__()
        
        # Constants
        self.PANEL_SIZE = (150, 185)
        self.ELEMENT_DISTANCE = 25
        self.ELEMENT_START = -self.PANEL_SIZE[1] / 2 + 32
        
        self.ADD_DELAY = 0.0
        self.add_delay = self.ADD_DELAY
    
    def start(self):
        self.score_manager_ref = engine.scene_manager.current_scene.get_actor(ScoreManager)
        self.MIDDLE = Text.get_position("UI", (0.5, 0.5))
        self.pos_tween = TweenSequence()\
            .start_delay(1, (self.MIDDLE[0], -self.PANEL_SIZE[1] / 2))\
            .add(Tween((self.MIDDLE[0], -self.PANEL_SIZE[1] / 2), self.MIDDLE, 0.75, easingfuncs.ease_in_out_back))
        self.text_font = pygame.font.Font("game/fonts/EnterCommand.ttf", 16)
        PANEL_OUTLINE = 1
        PANEL_BORDER_RADIUS = 8
        self.ui_values = [0, 0, 0, 0]
        
        # UI setup
        self.title = Text((self.MIDDLE[0], self.ELEMENT_START - 8),
                   pygame.font.Font("game/fonts/DigitalDisco.ttf", 32),
                   "Results",
                   pygame.Color("black"))
        self.score = Text((self.MIDDLE[0], self.ELEMENT_START + self.ELEMENT_DISTANCE),
                   self.text_font,
                   "Score: 0",
                   pygame.Color("black"))
        self.distance = Text((self.MIDDLE[0], self.ELEMENT_START + self.ELEMENT_DISTANCE * 2),
                   self.text_font,
                   "Distance driven: 0m",
                   pygame.Color("black"))
        self.drift = Text((self.MIDDLE[0], self.ELEMENT_START + self.ELEMENT_DISTANCE * 3),
                   self.text_font,
                   "Distance drifted: 0m",
                   pygame.Color("black"))
        self.loops = Text((self.MIDDLE[0], self.ELEMENT_START + self.ELEMENT_DISTANCE * 4),
                   self.text_font,
                   "Loops: 0",
                   pygame.Color("black"))
        self.continue_button = Button((self.MIDDLE[0], self.MIDDLE[1] + self.ELEMENT_START + self.ELEMENT_DISTANCE * 5.5),
                   pygame.font.Font("game/fonts/EnterCommand-Bold.ttf", 16),
                   "Retry",
                   pygame.Color("black"),
                   None,
                   pygame.Color("black"),
                   pygame.Color((0, 0, 0, 64)),
                   lambda : engine.scene_manager.change_scene("Car"),
                   padding=(10, 10))
        
        # Create back panel
        self.panel = pygame.Surface(self.PANEL_SIZE, pygame.SRCALPHA)
        pygame.draw.rect(self.panel, pygame.Color(184, 111, 80), pygame.Rect((0, 0), self.PANEL_SIZE), 0, PANEL_BORDER_RADIUS)
        pygame.draw.rect(self.panel, pygame.Color(116, 63, 57), pygame.Rect((0, 0), self.PANEL_SIZE), PANEL_OUTLINE, PANEL_BORDER_RADIUS)
    
    def update(self):
        res = self.pos_tween.result()[1]
        self.title.position = (self.MIDDLE[0], res + self.ELEMENT_START - 8)
        self.score.position = (self.MIDDLE[0], res + self.ELEMENT_START + self.ELEMENT_DISTANCE)
        self.distance.position = (self.MIDDLE[0], res + self.ELEMENT_START + self.ELEMENT_DISTANCE * 2)
        self.drift.position = (self.MIDDLE[0], res + self.ELEMENT_START + self.ELEMENT_DISTANCE * 3)
        self.loops.position = (self.MIDDLE[0], res + self.ELEMENT_START + self.ELEMENT_DISTANCE * 4)
        self.continue_button.position = (self.MIDDLE[0], res + self.ELEMENT_START + self.ELEMENT_DISTANCE * 5.5)
        
        if not self.pos_tween.running():
            # Increment UI values and update ui
            self.add_delay -= engine.delta_time()
            if self.add_delay <= 0:
                self.add_delay = self.ADD_DELAY
                def increment():
                    self.ui_values[0] += self.what_to_add(self.ui_values[0], self.score_manager_ref.score)
                    self.ui_values[1] += self.what_to_add(self.ui_values[1], int(self.score_manager_ref.total_distance))
                    self.ui_values[2] += self.what_to_add(self.ui_values[2], int(self.score_manager_ref.drift_distance))
                    self.ui_values[3] += self.what_to_add(self.ui_values[3], self.score_manager_ref.total_loops)
                increment()
                increment()
                increment()
                self.score.text = f"Score: {self.ui_values[0]:.0f}"
                self.distance.text = f"Distance driven: {self.ui_values[1]:.0f}m"
                self.drift.text = f"Distance drifted: {self.ui_values[2]:.0f}m"
                self.loops.text = f"Loops: {self.ui_values[3]:.0f}"
            
            # Continue button
            self.continue_button.update()
            if engine.get_key_down(pygame.K_SPACE) or engine.get_key_down(pygame.K_RETURN):
                self.continue_button.on_clicked()
    
    def draw(self):
        engine.draw_passes["UI"].blit(0, self.panel, self.pos_tween.result())
        self.title.draw()
        self.score.draw()
        self.distance.draw()
        self.drift.draw()
        self.loops.draw()
        self.continue_button.draw()
    
    
    def what_to_add(self, current: int, target: int) -> int:
        if current >= target:
            return 0
        p10 = 0
        while current + 10**(p10 + 1) < target:
            p10 += 1
        p10 -= 1
        return 10**p10
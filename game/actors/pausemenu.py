import engine, pygame
from game.actors.ui import Text, Button, SelectableButton
from engine.tweening import Tween, easingfuncs
from game.actors.car import Car


class PauseMenu(engine.Actor):
    def __init__(self):
        super().__init__()
        
        # Constants
        self.PANEL_SIZE = (100, 60)
        self.BUTTON_OFFSET = (25, 10)
    
    def start(self):
        self.open = False
        self.MIDDLE = Text.get_position("UI", (0.5, 0.5))
        self.tween = Tween((self.MIDDLE[0], -self.PANEL_SIZE[1] / 2), self.MIDDLE, 0.75, easingfuncs.ease_in_out_back, use_unscaled_time=True)
        self.tween.reverse()
        self.tween.restart_at(1)
        self.font = pygame.font.Font("game/fonts/EnterCommand-Bold.ttf", 16)
        self.last_mouse_pos = engine.get_mouse_pos("UI")
        PANEL_OUTLINE = 1
        PANEL_BORDER_RADIUS = 8
        # UI setup
        self.question = Text((self.MIDDLE[0], -self.BUTTON_OFFSET[1]),
                   self.font,
                   "Exit to title?",
                   pygame.Color("black"))
        self.yes_button = SelectableButton((self.MIDDLE[0] + self.BUTTON_OFFSET[0], self.MIDDLE[1] + self.BUTTON_OFFSET[1]),
                   self.font,
                   "Yes",
                   pygame.Color("black"),
                   None,
                   pygame.Color("black"),
                   pygame.Color((0, 0, 0, 64)),
                   lambda : engine.scene_manager.change_scene("Main Menu"),
                   padding=(10, 10))
        self.no_button = SelectableButton((self.MIDDLE[0] - self.BUTTON_OFFSET[0], self.MIDDLE[1] + self.BUTTON_OFFSET[1]),
                   self.font,
                   "No",
                   pygame.Color("black"),
                   None,
                   pygame.Color("black"),
                   pygame.Color((0, 0, 0, 64)),
                   self.no_button_pressed,
                   padding=(15, 10))
        
        # Create back panel
        self.panel = pygame.Surface(self.PANEL_SIZE, pygame.SRCALPHA)
        pygame.draw.rect(self.panel, pygame.Color(184, 111, 80), pygame.Rect((0, 0), self.PANEL_SIZE), 0, PANEL_BORDER_RADIUS)
        pygame.draw.rect(self.panel, pygame.Color(116, 63, 57), pygame.Rect((0, 0), self.PANEL_SIZE), PANEL_OUTLINE, PANEL_BORDER_RADIUS)
    
    def update(self):
        res = self.tween.result()
        self.question.position = ((res[0], res[1] - self.BUTTON_OFFSET[1]))
        self.yes_button.position = (res[0] + self.BUTTON_OFFSET[0], res[1] + self.BUTTON_OFFSET[1])
        self.no_button.position = (res[0] - self.BUTTON_OFFSET[0], res[1] + self.BUTTON_OFFSET[1])
        if not self.open:
            if engine.get_key_down(pygame.K_ESCAPE):
                self.open = True
                self.tween = Tween((self.MIDDLE[0], -self.PANEL_SIZE[1] / 2), self.MIDDLE, 0.75, easingfuncs.ease_in_out_back, use_unscaled_time=True)
                self.tween.restart()
                engine.time_scale = 0
            return
        else:
            if engine.get_key_down(pygame.K_ESCAPE):
                self.no_button_pressed()
            self.no_button.update()
            self.yes_button.update()
        
        if engine.get_key_down(pygame.K_a) or engine.get_key_down(pygame.K_LEFT):
            self.yes_button.selected = False
            self.no_button.selected = True
        if engine.get_key_down(pygame.K_d) or engine.get_key_down(pygame.K_RIGHT):
            self.yes_button.selected = True
            self.no_button.selected = False
        
        if self.last_mouse_pos != engine.get_mouse_pos("UI"):
            self.yes_button.selected = False
            self.no_button.selected = False
        self.last_mouse_pos = engine.get_mouse_pos("UI")
    
    def draw(self):
        engine.draw_passes["UI"].blit(0, self.panel, self.tween.result())
        self.question.draw()
        self.no_button.draw()
        self.yes_button.draw()
    
    def no_button_pressed(self):
        self.open = False
        self.tween = Tween(self.MIDDLE, (self.MIDDLE[0], -self.PANEL_SIZE[1] / 2), 0.75, easingfuncs.ease_in_out_back, use_unscaled_time=True)
        engine.time_scale = 1
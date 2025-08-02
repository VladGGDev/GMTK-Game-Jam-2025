import engine, pygame
from game.actors.ui import Text, Button, SelectableButton


class MainMenuScene(engine.Scene):
    def __init__(self):
        super().__init__([])
    
    def start(self):
        middle_x = Text.get_position("UI", (0.5, 0))[0]
        self.last_mouse_pos = engine.get_mouse_pos("UI")
        self.play_button =  SelectableButton((middle_x, 175),
                   pygame.font.Font(None, 32),
                   "Play",
                   pygame.Color("black"),
                   None,
                   pygame.Color("black"),
                   pygame.Color((0, 0, 0, 64)),
                   lambda : engine.scene_manager.change_scene("Car"),
                   padding=(10, 10))
        self.how_button = SelectableButton((middle_x, 220),
                   pygame.font.Font(None, 32),
                   "How to play",
                   pygame.Color("black"),
                   None,
                   pygame.Color("black"),
                   pygame.Color((0, 0, 0, 64)),
                   lambda : engine.scene_manager.change_scene("Car"),
                   padding=(10, 10))
        
        self.actors.extend([Text((middle_x, 65),
                   pygame.font.Font(None, 72),
                   "Game Title",
                   pygame.Color("black")),
                   
                   self.play_button,
                   self.how_button
        ])
        super().start()
    
    def update(self):
        if engine.get_key_down(pygame.K_w) or engine.get_key_down(pygame.K_UP):
            self.play_button.selected = True
            self.how_button.selected = False
        if engine.get_key_down(pygame.K_s) or engine.get_key_down(pygame.K_DOWN):
            self.play_button.selected = False
            self.how_button.selected = True
        
        if self.last_mouse_pos != engine.get_mouse_pos("UI"):
            self.play_button.selected = False
            self.how_button.selected = False
        self.last_mouse_pos = engine.get_mouse_pos("UI")
        
        return super().update()
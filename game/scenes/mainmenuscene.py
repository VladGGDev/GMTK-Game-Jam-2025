import engine, pygame
from game.actors.ui import Text, Button, SelectableButton


class MainMenuScene(engine.Scene):
    def __init__(self):
        super().__init__([])
        self.selected_button = 0
        self.NUM_BUTTONS = 3
    
    def start(self):
        middle_x = Text.get_position("UI", (0.5, 0))[0]
        self.last_mouse_pos = engine.get_mouse_pos("UI")
        self.play_button =  SelectableButton((middle_x, 155),
                   pygame.font.Font(None, 32),
                   "Play",
                   pygame.Color("black"),
                   None,
                   pygame.Color("black"),
                   pygame.Color((0, 0, 0, 64)),
                   lambda : engine.scene_manager.change_scene("Car"),
                   padding=(10, 10))
        self.play_button.selected = True
        self.how_button = SelectableButton((middle_x, 195),
                   pygame.font.Font(None, 32),
                   "How to play",
                   pygame.Color("black"),
                   None,
                   pygame.Color("black"),
                   pygame.Color((0, 0, 0, 64)),
                   lambda : print("How to play"),
                   padding=(10, 10))
        self.quit_button = SelectableButton((middle_x, 235),
                   pygame.font.Font(None, 32),
                   "Quit",
                   pygame.Color("black"),
                   None,
                   pygame.Color("black"),
                   pygame.Color((0, 0, 0, 64)),
                   lambda : engine.quit(),
                   padding=(10, 10))
        
        self.actors.extend([
            Text((middle_x, 65),
                pygame.font.Font(None, 72),
                "Game Title",
                pygame.Color("black")),
                
            self.play_button,
            self.how_button,
            self.quit_button
        ])
        super().start()
    
    def update(self):
        def deselect_buttons():
            self.play_button.selected = False
            self.how_button.selected = False
            self.quit_button.selected = False
        
        if engine.get_key_down(pygame.K_w) or engine.get_key_down(pygame.K_UP):
            deselect_buttons()
            if self.selected_button > 0:
                self.selected_button -= 1
        if engine.get_key_down(pygame.K_s) or engine.get_key_down(pygame.K_DOWN):
            deselect_buttons()
            if self.selected_button < self.NUM_BUTTONS - 1:
                self.selected_button += 1
        
        if self.selected_button == 0:
            self.play_button.selected = True
        elif self.selected_button == 1: 
            self.how_button.selected = True
        elif self.selected_button == 2: 
            self.quit_button.selected = True
        
        if self.last_mouse_pos != engine.get_mouse_pos("UI"):
            deselect_buttons()
            self.selected_button = -1
        self.last_mouse_pos = engine.get_mouse_pos("UI")
        
        return super().update()
import engine, pygame
from game.actors.ui import Text, Button, SelectableButton


class MainMenuScene(engine.Scene):
    def __init__(self):
        super().__init__([])
        self.selected_button = 0
        self.NUM_BUTTONS = 3
        self.how_texture = pygame.image.load("game/sprites/Controls.png")
        self.show_controls = False
    
    def start(self):
        middle_x = Text.get_position("UI", (0.5, 0))[0]
        self.title_font = pygame.font.Font("game/fonts/DigitalDisco.ttf", 64)
        self.button_font = pygame.font.Font("game/fonts/EnterCommand-Bold.ttf", 32)
        self.last_mouse_pos = engine.get_mouse_pos("UI")
        self.play_button =  SelectableButton((middle_x, 155),
                    self.button_font,
                    "Play",
                    pygame.Color("black"),
                    None,
                    pygame.Color("black"),
                    pygame.Color((0, 0, 0, 64)),
                    lambda : engine.scene_manager.change_scene("Car"),
                    padding=(10, 10))
        self.play_button.selected = True
        self.how_button = SelectableButton((middle_x, 195),
                    self.button_font,
                    "How to play",
                    pygame.Color("black"),
                    None,
                    pygame.Color("black"),
                    pygame.Color((0, 0, 0, 64)),
                    on_click=lambda : self.toggle_show_controls(True),
                    on_deselected=lambda : self.toggle_show_controls(False),
                    padding=(10, 10))
        self.quit_button = SelectableButton((middle_x, 235),
                    self.button_font,
                    "Quit",
                    pygame.Color("black"),
                    None,
                    pygame.Color("black"),
                    pygame.Color((0, 0, 0, 64)),
                    lambda : engine.quit(),
                    padding=(10, 10))
        
        self.actors.extend([
            Text((middle_x, 65),
                self.title_font,
                "Dune Drifter",
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
            pass
        elif self.selected_button == 2: 
            self.quit_button.selected = True
        
        if self.last_mouse_pos != engine.get_mouse_pos("UI"):
            deselect_buttons()
            self.selected_button = -1
        self.last_mouse_pos = engine.get_mouse_pos("UI")
        
        return super().update()
    
    def draw(self):
        if self.show_controls:
            engine.draw_passes["UI"].blit(1, self.how_texture, (0, 0), pivot=(0, 0))
        return super().draw()
    
    def toggle_show_controls(self, toggle: bool):
        self.show_controls = toggle
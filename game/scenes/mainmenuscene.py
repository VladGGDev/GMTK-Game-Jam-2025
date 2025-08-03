import engine, pygame
from game.actors.ui import Text, Button, SelectableButton


class MainMenuScene(engine.Scene):
    ui_sound_channel = pygame.mixer.Channel(5)
    ui_sound_channel.set_volume(0.25)
    select_sound = pygame.mixer.Sound("game/sounds/UI Click.wav")
    select_sound.set_volume(0.2)
    click_sound = pygame.mixer.Sound("game/sounds/Button Press.wav")
    
    def __init__(self):
        super().__init__([])
        self.selected_button = 0
        self.NUM_BUTTONS = 3
        self.how_texture = pygame.image.load("game/sprites/Controls.png")
        self.show_controls = False
        self.background = pygame.image.load("game/sprites/Menu Background.png")
        self.background.set_alpha(195)
    
    def start(self):
        middle_x = Text.get_position("UI", (0.5, 0))[0]
        self.title_font = pygame.font.Font("game/fonts/DigitalDisco.ttf", 48)
        self.button_font = pygame.font.Font("game/fonts/EnterCommand-Bold.ttf", 32)
        self.last_mouse_pos = engine.get_mouse_pos("UI")
        
        # Lambdas
        def play_sound(i: int):
            if i == 1:
                MainMenuScene.select_sound.play()
            else:
                MainMenuScene.click_sound.play()
        
        def how_button_click():
            self.toggle_show_controls(True)
            play_sound(0)
        
        def how_button_deselect():
            if self.show_controls:
                play_sound(0)
            self.toggle_show_controls(False)
        
            
        self.play_button =  SelectableButton((middle_x, 155),
                    self.button_font,
                    "Play",
                    pygame.Color("black"),
                    None,
                    pygame.Color("black"),
                    pygame.Color((0, 0, 0, 64)),
                    lambda : engine.scene_manager.change_scene("Car"),
                    lambda : play_sound(1),
                    padding=(10, 10))
        # self.play_button.selected = True
        self.how_button = SelectableButton((middle_x, 195),
                    self.button_font,
                    "How to play",
                    pygame.Color("black"),
                    None,
                    pygame.Color("black"),
                    pygame.Color((0, 0, 0, 64)),
                    on_click=how_button_click,
                    on_selected=lambda : play_sound(1),
                    on_deselected=how_button_deselect,
                    padding=(10, 10))
        self.quit_button = SelectableButton((middle_x, 235),
                    self.button_font,
                    "Quit",
                    pygame.Color("black"),
                    None,
                    pygame.Color("black"),
                    pygame.Color((0, 0, 0, 64)),
                    lambda : engine.quit(),
                    lambda : play_sound(1),
                    padding=(10, 10))
        
        self.actors.extend([
            Text((middle_x, 60),
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
        engine.draw_passes["UI"].blit(-1, self.background, (0, 0), pivot=(0, 0))
        return super().draw()
    
    def toggle_show_controls(self, toggle: bool):
        self.show_controls = toggle
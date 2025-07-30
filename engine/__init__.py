import pygame
from .camera import Camera
from .drawpass import DrawPass
from .scene import SceneManager, Scene
from .actor import Actor
from pygame._sdl2.video import Window


# ////////////////////////
# //////// Input /////////
# ////////////////////////
# Keyboard
_keys_pressed = dict[int, bool]()
__keys_pressed_last = dict[int, bool]()


def get_key(keycode: int) -> bool:
    return _keys_pressed.get(keycode, False)

def get_key_down(keycode: int) -> bool:
    return _keys_pressed.get(keycode, False) and not __keys_pressed_last.get(keycode, False)

def get_key_up(keycode: int) -> bool:
    return not _keys_pressed.get(keycode, False) and __keys_pressed_last.get(keycode, False)


# Mouse
__mouse_buttons_last = (False, False, False, False, False)
__scroll_delta = 0


def get_scroll_delta() -> int:
    return __scroll_delta

def get_mouse_buttons() -> tuple[bool, bool, bool, bool, bool]:
    return pygame.mouse.get_pressed(5)

def get_mouse_buttons_down() -> tuple[bool, bool, bool, bool, bool]:
    return (not __mouse_buttons_last[0] and get_mouse_buttons()[0],
            not __mouse_buttons_last[1] and get_mouse_buttons()[1],
            not __mouse_buttons_last[2] and get_mouse_buttons()[2],
            not __mouse_buttons_last[3] and get_mouse_buttons()[3],
            not __mouse_buttons_last[4] and get_mouse_buttons()[4])

def get_mouse_buttons_up() -> tuple[bool, bool, bool, bool, bool]:
    return (__mouse_buttons_last[0] and not get_mouse_buttons()[0],
            __mouse_buttons_last[1] and not get_mouse_buttons()[1],
            __mouse_buttons_last[2] and not get_mouse_buttons()[2],
            __mouse_buttons_last[3] and not get_mouse_buttons()[3],
            __mouse_buttons_last[4] and not get_mouse_buttons()[4])

def get_mouse_pos() -> tuple[int, int]:
    return pygame.mouse.get_pos()

def set_mouse_pos(pos: tuple[int, int]):
    pygame.mouse.set_pos(pos)

def get_mouse_visible() -> bool:
    return pygame.mouse.get_visible()

def set_mouse_visible(value: bool):
    pygame.mouse.set_visible(value)


# ////////////////////////
# ///////// Time /////////
# ////////////////////////
time_scale: float = 1
unscaled_delta_time: float = 0.001
unscaled_fixed_delta_time: float = 1 / 60
total_time: float = 0


def delta_time() -> float:
    return unscaled_delta_time * time_scale

def fixed_delta_time() -> float:
    return unscaled_fixed_delta_time * time_scale

def unscaled_total_time() -> float:
    return pygame.time.get_ticks() / 1000


# ////////////////////////
# /////// Rendering //////
# ////////////////////////
can_render = True
draw_passes = dict[str, DrawPass]()



# ////////////////////////
# //// Initialization ////
# ////////////////////////
running = True
scene_manager = SceneManager.empty()


def run(scene_manager_init: SceneManager | None = None,
        draw_passes_init: dict[str, DrawPass] | None = None,
        fullscreen: bool = False, borderless = False, default_window_size: tuple[int, int] = (0, 0)):
    pygame.init()
    
    # Variable declaration
    global running, total_time, _keys_pressed, \
        __keys_pressed_last, __scroll_delta, unscaled_delta_time, \
        __mouse_buttons_last, can_render, scene_manager, \
        draw_passes
    # Private
    next_fixed_timestep = 0
    clock = pygame.time.Clock()
    
    # Window initialization
    global screen, window
    screen = pygame.display.set_mode(flags=pygame.SRCALPHA)
    window = Window.from_display_module()
    
    if fullscreen:
        window.set_fullscreen(True)
    window.resizable = True
    window.borderless = borderless
    if default_window_size == (0, 0):
        window.maximize()
    else:
        window.size = default_window_size
        window.position = (0, 32) # Make handle visible
    
    # Initialization checking
    if scene_manager_init != None:
        scene_manager = scene_manager_init
    elif scene_manager.current_scene == None:
        raise ValueError("Scene manager was not initialized")
    
    if draw_passes_init != None:
        draw_passes = draw_passes_init
    elif len(draw_passes) == 0:
        raise ValueError("Draw passes dict was not initialized")


    # Game loop
    scene_manager.start()
    while running:
        __keys_pressed_last = _keys_pressed.copy()
        __scroll_delta = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                _keys_pressed[event.dict["key"]] = True
            if event.type == pygame.KEYUP:
                _keys_pressed[event.dict["key"]] = False
            if event.type == pygame.MOUSEWHEEL:
                __scroll_delta = event.dict["y"]

        unscaled_delta_time = max(clock.get_time() / 1000, 0.001)
        total_time += delta_time()

        # Updating scenes
        next_fixed_timestep += unscaled_delta_time
        while next_fixed_timestep > 0:
            next_fixed_timestep -= unscaled_fixed_delta_time
            scene_manager.fixed_update()
        scene_manager.update()

        __mouse_buttons_last = pygame.mouse.get_pressed(num_buttons=5)
        
        # Drawing to screen
        if can_render:
            scene_manager.draw() # Call draw on all  actors
            
            screen_aspect_ratio = screen.get_width() / screen.get_height()
            
            sorted_draw_passes = sorted(draw_passes.values(), key=lambda dp : dp.order)
            for draw_pass in sorted_draw_passes:
                if screen.get_height() < screen.get_width():
                    desired_scale = (screen.get_width() / screen_aspect_ratio, screen.get_height())
                else: # H > W
                    desired_scale = (screen.get_height() * screen_aspect_ratio, screen.get_width())
                scaled = pygame.transform.scale(draw_pass.draw(), desired_scale)
                pos = ((screen.get_width() - desired_scale[0]) / 2, (screen.get_height() - desired_scale[1]) / 2)
                screen.blit(scaled, pos) # Actually draw on screen
            pygame.display.flip()

        clock.tick(1000)

    pygame.quit()

from typing import Any, Callable
import pygame, engine
from pygame.font import Font


UNIVERSAL_UI_DRAW_PASS: str = "UI"


class UiElement(engine.Actor):
    def __init__(self, rect: pygame.Rect, draw_pass: str = UNIVERSAL_UI_DRAW_PASS, order: int = 0):
        self.rect = rect
        self.draw_pass = draw_pass
        self.order = order
        super().__init__()
    
    def point_in_rect(self, point: tuple[float, float] | pygame.Vector2):
        return self.rect.collidepoint(point)
    
    def mouse_in_rect(self):
        sz = engine.draw_passes[self.draw_pass].surface.get_size()
        return self.point_in_rect((sz[0] * engine.get_mouse_pos(self.draw_pass)[0], sz[1] * engine.get_mouse_pos(self.draw_pass)[1]))
    
    @staticmethod
    def get_position(draw_pass: str, percentage: tuple[float, float]) -> tuple[float, float]:
        sz = engine.draw_passes[draw_pass].surface.get_size()
        return (sz[0] * percentage[0], sz[1] * percentage[1])


class Text(UiElement):
    def __init__(self,
                position: tuple[float, float] | pygame.Vector2,
                font: Font,
                text: str,
                color: pygame.Color,
                background: pygame.Color | None = None,
                antialias: bool = False,
                draw_pass: str = UNIVERSAL_UI_DRAW_PASS,
                order: int = 0,
                rotation: float = 0):
        self.position = position
        self.font = font
        self.text = text
        self.antialias = antialias
        self.color = color
        self.background = background
        self.rotation = rotation
        # Setting the rect
        sz = Text.render_surface(self).get_size()
        super().__init__(
            pygame.Rect(
                position[0] - sz[0] * 0.5, 
                position[1] - sz[1] * 0.5,
                sz[0],
                sz[1]), 
            draw_pass, order)
    
    def render_surface(self) -> pygame.Surface:
        return self.font.render(self.text, self.antialias, self.color, self.background)
    
    def draw(self):
        engine.draw_passes[self.draw_pass].blit(
            self.order,
            self.render_surface(),
            self.position,
            (1, 1),
            self.rotation,
            (0.5, 0.5))
        # Debug draw rect
        # engine.draw_passes[self.draw_pass].blit(
        #     self.order + 1,
        #     engine.DrawPass.get_pixel(pygame.Color(255, 0, 255, 64), self.rect.size),
        #     self.rect.center,
        #     (1, 1),
        #     self.rotation,
        #     (0.5, 0.5))


class Button(Text):
    def __init__(self,
                position: tuple[float, float] | pygame.Vector2,
                font: Font, text: str,
                color: pygame.Color,
                background: pygame.Color | None,
                selected_color: pygame.Color,
                selected_background: pygame.Color | None,
                on_click: Callable[[], None] = lambda : None,
                on_selected: Callable[[], None] = lambda : None,
                on_deselected: Callable[[], None] = lambda : None,
                padding: tuple[float, float] = (0, 0),
                antialias: bool = False,
                draw_pass: str = UNIVERSAL_UI_DRAW_PASS,
                order: int = 0,
                rotation: float = 0):
        super().__init__(position, font, text, color, background, antialias, draw_pass, order, rotation)
        self.selected_color = selected_color
        self.selected_background = selected_background
        self._was_selected = False
        self.on_clicked = on_click
        self.on_selected = on_selected
        self.on_deselected = on_deselected
        
        # Add padding to rect
        self.rect.inflate_ip(padding)
    
    def render_surface(self) -> pygame.Surface:
        if self.mouse_in_rect():
            return self.font.render(self.text, self.antialias, self.selected_color)
        else:
            return super().render_surface()
    
    def update(self):
        selected = self.mouse_in_rect()
        if selected and engine.get_mouse_buttons_down()[0]:
            self.on_clicked()
        if selected != self._was_selected:
            self.on_selected() if selected else self.on_deselected
        self._was_selected = selected
    
    def draw(self):
        # Drawing extended background
        bg = self.selected_background if self.mouse_in_rect() else self.background
        if bg != None:
            engine.draw_passes[self.draw_pass].blit(
                self.order,
                engine.DrawPass.get_pixel(bg, self.rect.size),
                self.position,
                (1, 1),
                self.rotation,
                (0.5, 0.5))
        super().draw()


class SelectableButton(Button):
    def __init__(self,
                position: tuple[float, float] | pygame.Vector2,
                font: Font, text: str,
                color: pygame.Color,
                background: pygame.Color | None,
                selected_color: pygame.Color,
                selected_background: pygame.Color | None,
                on_click: Callable[[], None] = lambda : None,
                on_selected: Callable[[], None] = lambda : None,
                on_deselected: Callable[[], None] = lambda : None,
                padding: tuple[float, float] = (0, 0),
                antialias: bool = False,
                draw_pass: str = UNIVERSAL_UI_DRAW_PASS,
                order: int = 0,
                rotation: float = 0):
        super().__init__(position, font, text, color, background, selected_color, selected_background,
                        on_click, on_selected, on_deselected, padding, antialias, draw_pass, order, rotation)
        self.selected = False
    
    def mouse_in_rect(self):
        return self.selected or super().mouse_in_rect()
    
    def update(self):
        if self.selected and (engine.get_key_down(pygame.K_SPACE) or engine.get_key_down(pygame.K_RETURN)):
            self.on_clicked()
        super().update()
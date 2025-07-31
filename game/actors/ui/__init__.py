from typing import Any, Callable
import pygame, engine, engine.collider
from pygame.font import Font


UNIVERSAL_UI_DRAW_PASS: str = "UI"


class UiElement(engine.Actor):
    def __init__(self, rect: pygame.Rect, draw_pass: str = UNIVERSAL_UI_DRAW_PASS, order: int = 0):
        super().__init__()
        self.rect = rect
        self.draw_pass = draw_pass
        self.order = order
    
    def point_in_rect(self, point: tuple[float, float] | pygame.Vector2):
        return self.rect.collidepoint(point)
    
    def mouse_in_rect(self):
        return self.point_in_rect(engine.get_mouse_pos())


class Text(UiElement):
    def __init__(self,
                position: tuple[float, float] | pygame.Vector2,
                font: Font,
                text: str,
                color: tuple[int, int, int, int],
                background: tuple[int, int, int, int] = (0, 0, 0, 0),
                antialias: bool = True,
                draw_pass: str = UNIVERSAL_UI_DRAW_PASS,
                order: int = 0,
                rotation: float = 0,
                pivot: tuple[float, float] = (0.5, 0.5)):
        self.font = font
        self.text = text
        self.antialias = antialias
        self.color = color
        self.background = background
        self.rerender_surface()
        self.position = position
        self.rotation = rotation
        self.pivot = pivot
        super().__init__(pygame.Rect(position, self.surface.get_size()), draw_pass, order)
    
    def _render_surface(self) -> pygame.Surface:
        return self.font.render(self.text, self.antialias, self.color, self.background)
    
    def rerender_surface(self) -> None:
        self.surface = self._render_surface()
    
    def __setattr__(self, name: str, value: Any):
        """Any time an attribute is changed other than position, rotation, or pivot, re-render the text surface."""
        super().__setattr__(name, value)
        if name != "position" or name != "rotation" or name != "pivot":
            self.rerender_surface()
    
    def draw(self):
        engine.draw_passes[self.draw_pass].blit(
            self.order,
            self.surface,
            self.position,
            (1, 1),
            self.rotation,
            self.pivot)


class Button(Text):
    def __init__(self,
                position: tuple[float, float] | pygame.Vector2,
                font: Font, text: str,
                color: tuple[int, int, int, int],
                background: tuple[int, int, int, int],
                selected_color: tuple[int, int, int, int],
                selected_background: tuple[int, int, int, int],
                on_click: Callable[[], None] = lambda : None,
                on_selected: Callable[[], None] = lambda : None,
                on_deselected: Callable[[], None] = lambda : None,
                antialias: bool = True,
                draw_pass: str = UNIVERSAL_UI_DRAW_PASS,
                order: int = 0,
                rotation: float = 0,
                pivot: tuple[float, float] = (0.5, 0.5)):
        super().__init__(position, font, text, color, background, antialias, draw_pass, order, rotation, pivot)
        self.selected_color = selected_color
        self.selected_background = selected_background
        self._was_selected = False
        self.on_clicked = on_click
        self.on_selected = on_selected
        self.on_deselected = on_deselected
    
    def _render_surface(self) -> pygame.Surface:
        if self.mouse_in_rect():
            return self.font.render(self.text, self.antialias, self.selected_color, self.selected_background)
        else:
            return super()._render_surface()
    
    def update(self):
        selected = self.mouse_in_rect()
        if selected and engine.get_mouse_buttons_down()[0]:
            self.on_clicked()
        if selected != self._was_selected:
            self.on_selected() if selected else self.on_deselected
            self.rerender_surface()
        self._was_selected = selected
        
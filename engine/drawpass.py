from pygame import Surface, Rect, Vector2, transform
import engine, pygame
from typing import Any


class DrawPass:
    def __init__(self, resolution: tuple[int, int], 
                order: int = 0, 
                camera: engine.Camera | None = None, 
                clear_color: tuple[int, int, int, int] = (0, 0, 0, 255)):
        self.surface = Surface(resolution, pygame.SRCALPHA)
        self.order = order
        self.clear_color = clear_color
        if camera is None:
            self.camera = engine.Camera((0, 0), resolution)
        else:
            self.camera = camera
        self._operations = dict[float, list[tuple[Any, ...]]]()
    
    @classmethod
    def create_ui(cls,
                resolution: tuple[int, int],
                order: int = 99,
                clear_color: tuple[int, int, int, int] = (0, 0, 0, 0)):
        """Create a DrawPass with coordinate (0, 0) in the top left corner"""
        return cls(resolution, order, engine.Camera((resolution[0] / 2, resolution[1] / 2), resolution), clear_color)

    def blit(self, 
            order: float,
            source: Surface,
            position: tuple[float, float] | Vector2,
            scale: tuple[float, float] | Vector2 = (1, 1),
            rotation: float = 0,
            pivot: tuple[float, float] | Vector2 = (0.5, 0.5),
            source_rect: Rect | None = None,
            special_flags = 0):
        """
        Draw a surface to this draw pass.\n
        :param order: Order of drawing this operation, lower is drawn first\n
        :param source: The source Surface\nposition - the world space position\n
        :param scale: Multiplier to the scale of the source surface\n
        :param rotation: Degrees to rotate counterclockwise\n
        :param pivot: Position between 0 and 1 of the origin of the surface 
        (where it will be scaled and rotated from)\n
        :param source_rect: Use a smaller rect of this surface
        :param special_flags: Pygame special flags"""
        
        campos = self.camera.position
        # Half of the draw pass surface size
        halfsurfsz = (self.surface.get_width() / 2, self.surface.get_height() / 2)
        # How much bigger is the draw pass compared to the camera
        worldtocamsz = (self.surface.get_width() / self.camera.width, self.surface.get_height() / self.camera.height)
        # Scale multiplier applied to the source
        if source_rect == None:
            actualscale = (scale[0] * source.get_width(), scale[1] * source.get_height())
        else:
            actualscale = (scale[0] * source_rect.width, scale[1] * source_rect.height)
        
        
        # Size object relative to cam size
        scale = (actualscale[0] * worldtocamsz[0], actualscale[1] * worldtocamsz[1])
        
        # Also handle the source_rect
        if source_rect != None and rotation == 0:
            # Offset pivot relative to the source_rect
            pivot = (source_rect.width / source.get_width() * pivot[0],
                    source_rect.height /source.get_height() * pivot[1])
            # Account for texture resizing
            source_rect.size = (int(source_rect.width * scale[0] / source.get_width()), 
                                int(source_rect.height * scale[1] / source.get_height()))
            source_rect.topleft = (int(source_rect.left * scale[0] / source.get_width()), 
                                int(source_rect.top * scale[1] / source.get_height()))
        
        # Offset the pivot of the object relative to the camera and center the camera on (0, 0)
        position = ((position[0] - campos.x - actualscale[0] * pivot[0]) * worldtocamsz[0] + halfsurfsz[0],
                    (position[1] - campos.y - actualscale[1] * pivot[1]) * worldtocamsz[1] + halfsurfsz[1])
        
        # Rotation operations
        if rotation != 0:
            from math import sin, cos, radians
            rotrad = radians(rotation)
            
            # Rotation does not work with source_rect, copy it to another surface
            if source_rect != None:
                newTex = Surface(source_rect.size, pygame.SRCALPHA)
                newTex.blit(source, (0, 0), source_rect, special_flags)
                source = newTex
                source_rect = None
            
            # Correct for pygame.transform.rotate function which automatically adds padding
            w = abs(sin(rotrad)) * scale[1] + abs(cos(rotrad)) * scale[0]
            h = abs(sin(rotrad)) * scale[0] + abs(cos(rotrad)) * scale[1]
            position = ((position[0] - (w - scale[0]) / 2),
                        (position[1] - (h - scale[1]) / 2))
            
            # Pivot rotation
            if pivot != (0.5, 0.5):
                pivotcenter = ((0.5 - pivot[0]) * scale[0], (0.5 - pivot[1]) * scale[0])
                rotated = (pivotcenter[0] * cos(-rotrad) - pivotcenter[1] * sin(-rotrad),
                              pivotcenter[0] * sin(-rotrad) + pivotcenter[1] * cos(-rotrad))
                move = (rotated[0] - pivotcenter[0], rotated[1] - pivotcenter[1])
                position = (position[0] + move[0], position[1] + move[1])
        
        # Blit
        self._blit(order, transform.rotate(transform.scale(source, scale), rotation), position, source_rect, special_flags)
    
    def _blit(self, order: float, source: Surface, dest_pos: tuple[float, float], source_rect: Rect | None = None, special_flags=0):
        """Internal wrapper for `self.surface.blit(source, dest_rect, source_rect, special_flags)`"""
        if order not in self._operations.keys():
            self._operations[order] = list[tuple[Any, ...]]()
        self._operations[order].append((source, dest_pos, source_rect, special_flags))

    def draw(self) -> Surface:
        """Draw all operations to self.surface and then return it"""
        sorted_order = sorted(self._operations.keys())
        self.surface.fill(self.clear_color)
        for order in sorted_order:
            operations = self._operations[order]
            for oper in operations:
                self.surface.blit(*oper)
        self._operations.clear()
        return self.surface
    
    
    @staticmethod
    def get_pixel(color: pygame.Color, size: tuple[int, int] = (1, 1)) -> Surface:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(color)
        return surf
    
    @staticmethod
    def get_circle(color: pygame.Color, radius: float, width: int = 0) -> Surface:
        surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (radius, radius), radius, width)
        return surf
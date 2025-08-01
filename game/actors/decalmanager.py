import engine, pygame, engine.spritesheet


class DecalManager(engine.Actor):
    def __init__(self):
        super().__init__()
        self.__decals = []
    
    def update(self):
        for d in self.__decals:
            d[0] -= engine.delta_time()
            if d[0] <= 0:
                self.__decals.remove(d)
    
    def draw(self):
        for d in self.__decals:
            if engine.draw_passes["Main"].camera.rect.collidepoint(d[2]):
                engine.draw_passes["Main"].blit(
                    -9990,
                    d[1],
                    d[2],
                    d[3],
                    d[4],
                    d[5],
                    d[6],
                    d[7]
                )
    
    
    def add_decal(self,
                lifetime: float,
                source: pygame.Surface,
                position: tuple[float, float] | pygame.Vector2,
                scale: tuple[float, float] | pygame.Vector2 = (1, 1),
                rotation: float = 0,
                pivot: tuple[float, float] | pygame.Vector2 = (0.5, 0.5),
                source_rect: pygame.Rect | None = None,
                special_flags = 0):
        self.__decals.append([lifetime, source, position, scale, rotation, pivot, source_rect, special_flags])
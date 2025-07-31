import engine, pygame, engine.collider


class Obstacle(engine.Actor):
    def __init__(self,
                position: tuple[float, float] | pygame.Vector2,
                collider_radius: float,
                texture: pygame.Surface,
                pivot: tuple[float, float] = (0.5, 0.5)):
        self.position = position
        self.collider_radius = collider_radius
        self.texture = texture
        self.pivot = pivot
    
    def start(self):
        self.collider = engine.collider.CircleCollider(pygame.Vector2(self.position), self.collider_radius, "Obstacle")
    
    def draw(self):
        engine.draw_passes["Main"].blit(
            self.collider.position.y,
            self.texture,
            self.collider.position,
            pivot=self.pivot)
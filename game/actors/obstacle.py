import engine, pygame, engine.collider
import game.actors.car as car

class Obstacle(engine.Actor):
    def __init__(self,
                position: tuple[float, float] | pygame.Vector2,
                collider_radius: float,
                texture: pygame.Surface,
                pivot: tuple[float, float] = (0.5, 0.5)):
        super().__init__()
        self.position = position
        self.collider_radius = collider_radius
        self.texture = texture
        # self.shadow = Obstacle.create_shadow((collider_radius * 3.5, collider_radius * 2.5))
        self.shadow = car.Car.create_shadow(self.texture, 32)
        self.pivot = pivot
    
    def start(self):
        self.collider = engine.collider.CircleCollider(pygame.Vector2(self.position), self.collider_radius, "Obstacle")
    
    def draw(self):
        # Draw circle shadow
        # engine.draw_passes["Main"].blit(
        #     self.collider.position.y,
        #     self.shadow,
        #     self.collider.position + pygame.Vector2(0, 1))
        # Draw realistic shadow
        engine.draw_passes["Main"].blit(
            self.collider.position.y,
            self.shadow,
            self.collider.position,
            (1, 1),
            180,
            (0.5, 0))
        # Draw self
        engine.draw_passes["Main"].blit(
            self.collider.position.y,
            self.texture,
            self.collider.position,
            pivot=self.pivot)
    
    @staticmethod
    def create_shadow(ellipse_size: tuple[float, float], alpha: int = 64) -> pygame.Surface:
        surf = pygame.Surface(ellipse_size, pygame.SRCALPHA)
        pygame.draw.ellipse(surf, pygame.Color(0, 0, 0, alpha), pygame.Rect((0, 0), ellipse_size))
        return surf
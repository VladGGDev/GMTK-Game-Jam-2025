import engine, pygame, engine.collider
import game.actors.car as car

class Obstacle(engine.Actor):
    def __init__(self,
                position: tuple[float, float] | pygame.Vector2,
                collider_radius: float,
                texture: pygame.Surface,
                pivot: tuple[float, float] = (0.5, 0.5),
                source_rect: pygame.Rect | None = None):
        super().__init__()
        self.position = position
        self.collider_radius = collider_radius
        self.texture = texture
        self.shadow = Obstacle.create_circle_shadow((collider_radius * 4, collider_radius * 2))
        # self.shadow = pygame.transform.flip(car.Car.create_shadow(self.texture, 32), False, True)
        self.pivot = pivot
        self.source_rect = source_rect
    
    def start(self):
        self.collider = engine.collider.CircleCollider(pygame.Vector2(self.position), self.collider_radius, "Obstacle")
    
    def draw(self):
        # Draw circle shadow
        engine.draw_passes["Main"].blit(
            self.collider.position.y,
            self.shadow,
            self.collider.position + pygame.Vector2(0, 3))
        # Draw realistic shadow
        # engine.draw_passes["Main"].blit(
        #     self.collider.position.y - 9999,
        #     self.shadow,
        #     self.collider.position,
        #     (1, 0.5),
        #     180,
        #     (0.5, 0),
        #     self.source_rect)
        # Draw self
        engine.draw_passes["Main"].blit(
            self.collider.position.y,
            self.texture,
            self.collider.position,
            pivot=self.pivot,
            source_rect=self.source_rect)
        
        # Debug draw collider
        # engine.draw_passes["Main"].blit(
        #     self.collider.position.y,
        #     engine.DrawPass.get_circle(pygame.Color("red"), self.collider.radius, 1),
        #     self.collider.position)
    
    @staticmethod
    def create_circle_shadow(ellipse_size: tuple[float, float], alpha: int = 64) -> pygame.Surface:
        surf = pygame.Surface(ellipse_size, pygame.SRCALPHA)
        pygame.draw.ellipse(surf, pygame.Color(0, 0, 0, alpha), pygame.Rect((0, 0), ellipse_size))
        return surf        
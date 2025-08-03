import engine, pygame, random
from engine.spritesheet import SpriteSheet
import engine.collider as collider

import game.actors.car as car
from game.actors.decalmanager import DecalManager


class Enemy(engine.Actor):
    graphic = SpriteSheet("game/sprites/Zombie.png", (8, 8))
    big_blood_tex = SpriteSheet("game/sprites/Blood Big.png", (16, 16))
    MAX_SPEED = 40
    MIN_SPEED = 30
    
    def __init__(self, position: pygame.Vector2 | tuple[float, float], speed: float):
        self.speed = speed
        self.start_position = position
        self.source = random.randint(0,1)
        self.shadow = car.Car.create_shadow(Enemy.graphic.texture)
        self.direction = pygame.Vector2()

    def start(self):
        self.collider = collider.CircleCollider(pygame.Vector2(self.start_position), 4, "Enemy")
        self.car_ref = engine.scene_manager.current_scene.get_actor(car.Car)

    def fixed_update(self):
        self.direction  = self.car_ref.collider.position - self.collider.position
        self.collider.position += self.direction.normalize() * self.speed * engine.fixed_delta_time()
        
    def draw(self):
        # Draw shadow
        engine.draw_passes["Main"].blit(
            self.collider.position.y,
            self.shadow,
            self.collider.position + pygame.Vector2(1, 1),
            source_rect=self.graphic[self.source]
        )
        # Draw self
        engine.draw_passes["Main"].blit(
            self.collider.position.y,
            Enemy.graphic.texture if self.direction.x > 0 else pygame.transform.flip(Enemy.graphic.texture, True, False),
            self.collider.position,
            source_rect=self.graphic[self.source] if self.direction.x > 0 else self.graphic[1 - self.source]
        )

    def end(self):
        engine.scene_manager.current_scene.get_actor(DecalManager).add_decal(
            20,
            Enemy.big_blood_tex.texture,
            self.collider.position,
            source_rect=Enemy.big_blood_tex[random.randrange(0, Enemy.big_blood_tex.get_num_cells())]
        )
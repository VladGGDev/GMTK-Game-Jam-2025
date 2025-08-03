import engine, pygame, random, math
from engine.lerputil import remap
from engine.spritesheet import SpriteSheet
import engine.collider as collider

import game.actors.car as car
from game.actors.decalmanager import DecalManager
from game.actors.cameramanager import CameraManager
from engine.shake import RandomShake, SineShake
import pygame.mixer

class Enemy(engine.Actor):
    graphic = pygame.image.load("game/sprites/Zombie.png")
    big_blood_tex = SpriteSheet("game/sprites/Blood Big.png", (16, 16))
    MAX_SPEED = 36
    MIN_SPEED = 20
   
    def __init__(self, position: pygame.Vector2 | tuple[float, float], speed: float):
        self.speed = speed
        self.start_position = position
        self.shadow = car.Car.create_shadow(Enemy.graphic)
        self.direction = pygame.Vector2()
        self.rotation_offset = random.uniform(0, 180)

    def start(self):
        self.collider = collider.CircleCollider(pygame.Vector2(self.start_position), 4, "Enemy")
        self.car_ref = engine.scene_manager.current_scene.get_actor(car.Car)
        self.camera_manager_ref = engine.scene_manager.current_scene.get_actor(CameraManager)

    def fixed_update(self):
        self.direction  = self.car_ref.collider.position - self.collider.position
        self.collider.position += self.direction.normalize() * self.speed * engine.fixed_delta_time()
        
    def draw(self):
        rotation = math.sin((engine.total_time + self.rotation_offset) * \
                            remap(self.speed, Enemy.MIN_SPEED, Enemy.MAX_SPEED, 0.75, 7.5)) * 15
        # Draw shadow
        engine.draw_passes["Main"].blit(
            self.collider.position.y,
            self.shadow,
            self.collider.position + pygame.Vector2(1, 1),
            rotation=rotation
        )
        # Draw self
        engine.draw_passes["Main"].blit(
            self.collider.position.y,
            Enemy.graphic if self.direction.x > 0 else pygame.transform.flip(Enemy.graphic, True, False),
            self.collider.position,
            rotation=rotation
        )

    def end(self):
        self.camera_manager_ref.add_shake(SineShake(0.3, 1.5, 60))
        engine.scene_manager.current_scene.get_actor(DecalManager).add_decal(
            20,
            Enemy.big_blood_tex.texture,
            self.collider.position,
            (1.25, 1.25),
            random.uniform(25, 65),
            (0.5, 0.5),
            Enemy.big_blood_tex[random.randrange(0, Enemy.big_blood_tex.get_num_cells())]
        )
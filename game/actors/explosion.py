import engine, pygame, engine.collider
from engine.tweening import Tween, easingfuncs, lerpfuncs

from game.actors.gameendmenu import GameEndMenu
from game.actors.pausemenu import PauseMenu
from game.actors.scoremanager import ScoreManager

from game.actors.enemy import Enemy
from engine.tweening import Tween, easingfuncs, lerpfuncs
import pygame.mixer
import random
from engine.lerputil import lerp
from game.actors.cameramanager import CameraManager
from engine.shake import SineShake


class Explosion(engine.Actor):
    decal_tex = pygame.image.load("game/sprites/Explosion Decal.png")

    def __init__(self, position: pygame.Vector2):
        super().__init__()
        self.collider.position = position
        self.radius_tween = Tween(0, 40, 1.25, easingfuncs.ease_out_expo, lerpfuncs.lerp)
        self.alpha_tween = Tween(255, 0, 1.25, easingfuncs.ease_in_sine, lerpfuncs.lerp)
        self.list_freq = [44100,22050,11025]
    
    def start(self):
        base_sound = pygame.mixer.Sound("game/sounds/Car Explosion.wav")
        base_sound.set_volume(0.25)
        base_sound.play()
        self.collider = engine.collider.CircleCollider(self.collider.position, 50, "Explosion")

        engine.scene_manager.current_scene.create_actor(GameEndMenu())
        engine.scene_manager.current_scene.get_actor(PauseMenu).can_open = False
        engine.scene_manager.current_scene.get_actor(CameraManager).add_shake(SineShake(0.3, 3.5, 70))
        
        # Destroy more enemies
        hits = 0
        for enemy in engine.scene_manager.current_scene.get_actors(Enemy):
            if self.collider.check(enemy.collider):
                engine.scene_manager.current_scene.destroy_actor(enemy)
                hits += 1
        engine.scene_manager.current_scene.get_actor(ScoreManager).score += hits
    
    def draw(self):
        engine.draw_passes["Main"].blit(-9990, Explosion.decal_tex, self.collider.position, (1.25, 1.25))
        engine.draw_passes["Main"].blit(
            -9989,
            engine.DrawPass.get_circle(pygame.Color(255, 255, 255, int(self.alpha_tween.result())), self.radius_tween.result()), 
            self.collider.position)
import engine, pygame, engine.collider
from engine.tweening import Tween, easingfuncs, lerpfuncs

from game.actors.gameendmenu import GameEndMenu
from game.actors.pausemenu import PauseMenu
from game.actors.scoremanager import ScoreManager
from game.actors.enemy import Enemy


class Explosion(engine.Actor):
    decal_tex = pygame.image.load("game/sprites/Explosion Decal.png")
    
    def __init__(self, position: pygame.Vector2):
        super().__init__()
        self.collider.position = position
        self.radius_tween = Tween(0, 32, 1.25, easingfuncs.ease_out_expo, lerpfuncs.lerp)
        self.alpha_tween = Tween(255, 0, 1.25, easingfuncs.ease_in_sine, lerpfuncs.lerp)
    
    def start(self):
        self.collider = engine.collider.CircleCollider(self.collider.position, 16, "Explosion")
        engine.scene_manager.current_scene.create_actor(GameEndMenu())
        engine.scene_manager.current_scene.get_actor(PauseMenu).can_open = False
        
        # Destroy more enemies
        hits = 0
        for enemy in engine.scene_manager.current_scene.get_actors(Enemy):
            if self.collider.check(enemy.collider):
                engine.scene_manager.current_scene.destroy_actor(enemy)
                hits += 1
        engine.scene_manager.current_scene.get_actor(ScoreManager).score += hits
    
    def draw(self):
        engine.draw_passes["Main"].blit(-9990, Explosion.decal_tex, self.collider.position)
        engine.draw_passes["Main"].blit(
            -9989,
            engine.DrawPass.get_circle(pygame.Color(255, 255, 255, int(self.alpha_tween.result())), self.radius_tween.result()), 
            self.collider.position)
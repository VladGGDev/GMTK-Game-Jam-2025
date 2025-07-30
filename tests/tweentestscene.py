from engine.actor import Actor
from engine.camera import Camera
from engine.scene import Scene
from engine.tweening import Tween, TweenSequence, easingfuncs, lerpfuncs
import engine.tweening.easingfuncs.custom as easingfuncs_custom
from engine import get_key_down
import engine
import pygame

class TweenTestScene(Scene):
    def __init__(self):
        super().__init__([])
        self.tween0 = Tween((100, 100), (900, 100), 1, easingfuncs.linear)
        self.tween1 = Tween((100, 200), (900, 200), 1, easingfuncs.ease_out_expo)
        self.tween2 = Tween((100, 300), (900, 300), 1, easingfuncs.ease_in_out_quart)
        self.tween3 = Tween((100, 400), (900, 400), 1, easingfuncs.ease_out_circ)
        self.tween4 = Tween((100, 500), (900, 500), 1, easingfuncs.ease_in_out_back)
        self.tween5 = Tween((100, 600), (900, 600), 1, easingfuncs.ease_out_bounce)
        
        self.tween_fluent1 = \
            Tween.new()\
            .with_start((100, 800))\
            .with_target((900, 800))\
            .with_duration(3)\
            .with_easingfunc(easingfuncs_custom.ease_out_elastic_custom(5))
        
        self.tween_col1 = Tween((0, 0, 0, 0), (255, 255, 255, 255), 1, easingfuncs_custom.linear_yo_yo(), lerpfuncs.color_lerp)
        
        self.tween_seq = TweenSequence[tuple[float, float]](easingfunc=easingfuncs.ease_out_expo)\
            .start_delay(1.5, (100, 700))\
            .add(Tween((100, 700), (300, 800), 3, easingfuncs.ease_in_out_quart))\
            .add(Tween((300, 800), (100, 800), 1))\
            .delay(0.5)\
            .add(Tween((100, 800), (100, 700), 0.5))
        
        
    def start(self):
        print("Press SPACE to reset the tweens.\nPress R to reverse the tweens.")
        
    def update(self):
        if get_key_down(pygame.K_SPACE):
            self.tween0.restart()
            self.tween1.restart()
            self.tween2.restart()
            self.tween3.restart()
            self.tween4.restart()
            self.tween5.restart()
            self.tween_fluent1.restart()
            self.tween_col1.restart()
            self.tween_seq.restart()
        if get_key_down(pygame.K_r):
            self.tween0.reverse()
            # self.tween1.reverse()
            self.tween2.reverse()
            # self.tween3.reverse()
            self.tween4.reverse()
            # self.tween5.reverse()
        if get_key_down(pygame.K_ESCAPE):
            engine.running = False
        return super().update()
    
    def draw(self):
        RADIUS = 10
        circle = pygame.Surface((RADIUS * 2, RADIUS * 2))
        pygame.draw.circle(circle, pygame.Color("white"), (RADIUS, RADIUS), RADIUS)
        engine.draw_passes["Main"].blit(0, circle, self.tween0.result())
        engine.draw_passes["Main"].blit(0, circle, self.tween1.result())
        engine.draw_passes["Main"].blit(0, circle, self.tween2.result())
        engine.draw_passes["Main"].blit(0, circle, self.tween3.result())
        engine.draw_passes["Main"].blit(0, circle, self.tween4.result())
        engine.draw_passes["Main"].blit(0, circle, self.tween5.result())
        
        engine.draw_passes["Main"].blit(0, circle, self.tween_fluent1.result())
        
        engine.draw_passes["Main"].blit(0, circle, (1200, 500))
        
        engine.draw_passes["Main"].blit(0, circle, self.tween_seq.result())
        return super().draw()
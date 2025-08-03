import pygame, engine
import random
from math import sin,pi,cos
from abc import ABC, abstractmethod


class BaseShake(ABC):
    @abstractmethod
    def update(self) -> pygame.Vector2:
        pass

    @abstractmethod
    def is_done(self) -> bool:
        pass

class RandomShake(BaseShake):
    def __init__(self,duration : float,intensity : float) -> None:
        self.offset = pygame.Vector2(0, 0)
        self.duration = duration
        self.remaining = duration
        self.intensity = intensity
    
    def update(self) -> pygame.Vector2:
        if self.remaining <= 0:
            return pygame.Vector2(0,0)
        self.remaining -= engine.delta_time()
        return pygame.Vector2(random.uniform(-self.intensity,self.intensity),
                              random.uniform(-self.intensity,self.intensity)
                              )
    
    def is_done(self) -> bool:
        return self.remaining <= 0

class SineShake(BaseShake):
    def __init__(self, duration:float, intensity:float, freq:float) -> None:
        self.offset = pygame.Vector2(0,0)
        self.duration = duration
        self.remaining = duration
        self.intensity = intensity
        self.freq = freq
        self.time = 0
        self.phase_offset = random.uniform(0, pi * 2)

    def update(self) -> pygame.Vector2:
        if self.remaining <= 0:
            return pygame.Vector2(0,0)
        
        self.time += engine.delta_time()

        offset_x = sin(self.freq * self.time + self.phase_offset) * self.intensity
        offset_y = cos(self.freq * self.time + self.phase_offset) * self.intensity * 0.5
                       

        self.remaining -= engine.delta_time()

        return pygame.Vector2(offset_x,offset_y)
    
    def is_done(self) -> bool:
        return self.remaining <=0
        
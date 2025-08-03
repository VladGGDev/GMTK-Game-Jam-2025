import engine, pygame, random
from math import sqrt, sin, cos, pi
from game.actors.enemy import Enemy
from game.actors.car import Car
import game.scenes.carscene as carscene


class EnemySpawner(engine.Actor):

    # enemy_sound = pygame.mixer.Sound()
    enemy_channel = pygame.mixer.Channel(6)

    def __init__(self,
                base_delay=3.0, 
                base_cap=2, 
                max_cap=50):
        self.base_delay = base_delay
        self.base_cap = base_cap
        self.max_cap = max_cap
        self.enemies_spawned_total = 0   
        self.timer = 0.0
    
    def start(self):
        self.car_ref = engine.scene_manager.current_scene.get_actor(Car)

    def get_current_cap(self) -> int:
        return min(self.max_cap, int(sqrt(self.enemies_spawned_total + 1) * self.base_cap))
    
    def get_spawn_delay(self) -> float:
        return max(0.1, self.base_delay) 

    def get_spawn_position(self):
        dist = engine.draw_passes["Main"].camera.width
        dir = random.uniform(0, pi * 2)
        return(dist * -sin(dir), dist * -cos(dir))
    
    def get_num_zombies(self) -> int:
        return len(engine.scene_manager.current_scene.get_actors(Enemy))
    
    def update(self):
        self.timer -= engine.delta_time()
        current_cap = self.get_current_cap()
        if self.timer <= 0 and self.get_num_zombies() < current_cap:
            spawn_pos = self.get_spawn_position()
            engine.scene_manager.current_scene.create_actor(Enemy(spawn_pos, random.uniform(Enemy.MIN_SPEED, Enemy.MAX_SPEED)))

            self.enemies_spawned_total += 1
            self.base_delay -= 0.025
            self.timer = self.get_spawn_delay()


    

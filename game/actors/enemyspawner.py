import engine, pygame
from game.actors.enemy import Enemy
import random
import math 

class EnemySpawner(engine.Actor):

    def __init__(self, map_size : tuple[float,float] | pygame.Vector2, 
                 base_delay=2.0, 
                 base_cap=4, 
                 max_cap=500):
        self.map_size = map_size
        self.base_delay = base_delay     
        self.base_cap = base_cap         
        self.max_cap = max_cap           
        self.enemies : list[Enemy] = []
        self.enemies_spawned_total = 0   
        self.timer = 0.0

    def get_current_cap(self) -> int:
        return min(self.max_cap, int(math.sqrt(self.enemies_spawned_total + 1) * self.base_cap))
    
    def get_spawn_delay(self) -> float:
        cap = self.get_current_cap()
        return max(0.1, self.base_delay / cap) 

    def get_spawn_position_outside_camera(self) :
        while True:
            x = random.randint(0, self.map_size.x)
            y = random.randint(0, self.map_size.y)
            point = pygame.Vector2(x, y)
            if not engine.draw_passes["Main"].camera.rect.collidepoint(point):
                return point
    
    def spawn_enemy(self):
        spawn_point = self.get_spawn_position_outside_camera()
        new_enemy = Enemy(spawn_point)
        self.enemies.append(new_enemy)
    
    def update(self):
        self.timer -= engine.delta_time()
        current_cap = self.get_current_cap()
        if self.timer <= 0 and len(self.enemies) < current_cap:
            spawn_pos = self.get_random_spawn_pos()
            engine.scene_manager.current_scene.create_actor(Enemy(spawn_pos,speed=random.randint(Enemy.MIN_SPEED,Enemy.MAX_SPEED)))
            self.enemies_spawned_total += 1
            self.timer = self.get_spawn_delay()


    

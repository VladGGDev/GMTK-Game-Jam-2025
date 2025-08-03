import engine, pygame, engine.collider as colliders, engine.tweening.lerpfuncs as lerputil, engine.tweening.easingfuncs as easings
from math import pi, sin, cos, degrees
from engine.tweening import Tween

from game.actors.decalmanager import DecalManager
from game.actors.scoremanager import ScoreManager
from game.actors.explosion import Explosion
import game.scenes.carscene as carscene
<<<<<<< Updated upstream
<<<<<<< Updated upstream
from game.actors.enemy import Enemy

=======
from engine.sound import pitch_shift
# from engine.lerputil import lerp
>>>>>>> Stashed changes
=======
from engine.sound import pitch_shift
# from engine.lerputil import lerp
>>>>>>> Stashed changes

class Car(engine.Actor):

    pygame.mixer.init(frequency=44100, size=-16, channels=1)  
    base_sound = pygame.mixer.Sound("game/sounds/Engine.wav")
    base_array = pygame.sndarray.array(base_sound) 
    MIN_PITCH = 0.7 
    MAX_PITCH = 1.3  
    engine_chan = pygame.mixer.Channel(3)

    def __init__(self):
        super().__init__()
        # Constants
        self.MAX_SPEED = 175
        self.MAX_DRIFT_SPEED = 200
        self.MIN_SPEED = 0
        self.ACCELERATION = self.MAX_SPEED / 0.25
        self.DECELERATION = self.MAX_SPEED / 1
        self.FRICTION_DECELERATION = self.MAX_SPEED / 5
        self.TURN_SPEED = 120 * pi / 180 # radians per second
        self.DRIFT_TURN_SPEED = 270 * pi / 180 # radians per second
        self.MAX_DRIFT_ENERGY = 1 # Seconds of drift
        self.DRIFT_GFX_MIN_PERCENTAGE = 0.5
        self.DRIFT_GFX_DIRECTION = pi / 3
        
        # Other initialization
        self.texture = pygame.image.load("game/sprites/Masina.png")
        self.shadow = Car.create_shadow(self.texture)
        
        # Dynamic values
        self.direction = 0
        self.speed = self.MIN_SPEED
        self.drift_energy = 0
        self.last_dir = 0
        self.gfx_direction = self.direction
        self.lost = False
        
        # Loop data
        self.drift_points = list[pygame.Vector2]()
        
        # Last loop data
        self.debug_last_drift_points = list[pygame.Vector2]()
        self.last_loop_alpha_tween = Tween(255, 0, 1, lerpfunc=lerputil.lerp)
        self.last_loop_alpha_tween.restart_at(1)
    
    def start(self):
        # Other initializations
        self.collider = colliders.CircleCollider(pygame.Vector2(0, 0), 4, "Car")
        self.decal_manager_ref = engine.scene_manager.current_scene.get_actor(DecalManager)
        self.skid_mark_sprite = pygame.image.load("game/sprites/Skid Marks.png")
        self.score_manager_ref = engine.scene_manager.current_scene.get_actor(ScoreManager)
        engine.draw_passes["Main"].camera.position = (0, 0)

    def play_engine(self, speed, max_speed):
        t = max(0.0, min(1.0, speed / max_speed))
        pitch = self.MIN_PITCH + (self.MAX_PITCH- self.MIN_PITCH) * t
        new_array = pitch_shift(self.base_array, pitch)
        new_sound = pygame.sndarray.make_sound(new_array.copy())
        new_sound.set_volume(0.8)
        self.engine_chan.play(new_sound, loops=-1)    
    
    def update(self):
        if self.lost:
            return
        pressed = engine.get_key
        
        dir = int(pressed(pygame.K_a) or pressed(pygame.K_LEFT)) - int(pressed(pygame.K_d) or pressed(pygame.K_RIGHT))
        if dir != 0: self.last_dir = dir
        max_sp = lerputil.lerp(self.MAX_SPEED, self.MAX_DRIFT_SPEED, easings.ease_out_cubic(self.drift_energy / self.MAX_DRIFT_ENERGY))
        turn_sp = self.TURN_SPEED if not pressed(pygame.K_SPACE) else self.DRIFT_TURN_SPEED
        
        # Drift energy
        self.drift_energy = max(self.drift_energy - engine.delta_time(), 0)
        if pressed(pygame.K_SPACE) and dir != 0:
            self.drift_energy = self.MAX_DRIFT_ENERGY
        
        # Acceleration controls
        if pressed(pygame.K_w) or pressed(pygame.K_UP) or self.drift_energy > 0:
            self.speed += self.ACCELERATION * engine.delta_time()
            self.play_engine(self.speed,self.MAX_DRIFT_SPEED)
        elif pressed(pygame.K_s) or pressed(pygame.K_DOWN):
            self.speed -= self.DECELERATION * engine.delta_time()
        else:
            self.speed -= self.FRICTION_DECELERATION * engine.delta_time()
        self.speed = pygame.math.clamp(self.speed, self.MIN_SPEED, max_sp)            
        
        # Steering controls
        self.direction += dir * turn_sp * engine.delta_time() * (self.speed / max_sp)
        
        # Clamp camera position to scene bounds
        cam_max = pygame.Vector2(carscene.CarScene.HALF_MAP_SIZE) - pygame.Vector2(engine.draw_passes["Main"].camera.half_resolution)
        clamped_position = self.v2_clamp(self.collider.position, cam_max)
        # Framerate-independent damping
        engine.draw_passes["Main"].camera.position = lerputil.vector2_lerp(
            pygame.Vector2(engine.draw_passes["Main"].camera.position),
            clamped_position,
            1 - 0.005**engine.delta_time())
        
        # Smooth direction
        self.gfx_direction = lerputil.lerp(
            self.gfx_direction,
            self.get_drift_additional_rotation(),
            1 - 0.0005**engine.delta_time())
    
    def fixed_update(self):
        if self.lost:
            return
        # Loop logic
        if self.drift_energy > 0:
            self.drift_points.append(pygame.Vector2(self.collider.position))
            self.decal_manager_ref.add_decal(
                15,
                self.skid_mark_sprite,
                pygame.Vector2(self.collider.position),
                rotation=degrees(self.direction + self.get_drift_additional_rotation())
            )
            if len(self.drift_points) > 1:
                # Check for completed loop
                intersects = Car.segment_intersects_polygon(self.drift_points[-2], self.drift_points[-1], self.drift_points[:-50])
                if intersects != None:
                    # Remove the trailing segments which are not part of the polygon
                    self.drift_points = self.drift_points[intersects[0]:]
                    self.last_loop_alpha_tween.restart()
                    self.debug_last_drift_points = self.drift_points[:]
                    
                    self.score_manager_ref.total_loops += 1
                    # Kill enemies inside the loop
                    hits = 0
                    enemies = engine.scene_manager.current_scene.get_actors(Enemy)
                    for enemy in enemies:
                        if Car.point_inside_polygon(enemy.collider.position, self.drift_points):
                            engine.scene_manager.current_scene.destroy_actor(enemy)
                            hits += 1
                    self.score_manager_ref.score += hits
                    # Clear the polygon
                    self.drift_points.clear()
        else:
            self.drift_points.clear()
        
        # Moving the collider
        move = self.speed * engine.fixed_delta_time()
        self.collider.position += pygame.Vector2(
            move * -sin(self.direction),
            move * -cos(self.direction)
        )
        
        # Changing values in score manager
        if self.drift_energy > 0:
            self.score_manager_ref.drift_distance += move / 8
        self.score_manager_ref.total_distance += move / 8
        
        # Check for collision with anything
        for coll in colliders.all_colliders:
            if coll.tag != "Car" and self.collider.check(coll):
                self.lost = True
                engine.scene_manager.current_scene.create_actor(Explosion(self.collider.position))
                break
        
        # Clamp position to scene bounds
        self.collider.position = self.v2_clamp(self.collider.position, pygame.Vector2(carscene.CarScene.HALF_MAP_SIZE))
        
    
    def draw(self):
        if self.lost:
            return
        direction = degrees(self.direction + self.gfx_direction)
        # Draw shadow
        engine.draw_passes["Main"].blit(
            self.collider.position.y,
            self.shadow,
            self.collider.position + pygame.Vector2(1, 1),
            (1, 1),
            direction
        )
        # Draw car
        engine.draw_passes["Main"].blit(
            self.collider.position.y,
            self.texture,
            self.collider.position,
            (1, 1),
            direction
        )
        # Debug draw drift points
        for point in self.debug_last_drift_points:
            engine.draw_passes["Main"].blit(
                99,
                engine.DrawPass.get_pixel(pygame.Color(255, 0, 0, int(self.last_loop_alpha_tween.result())), (2, 2)),
                point
            )
    
    
    def get_drift_additional_rotation(self) -> float:
        return self.DRIFT_GFX_DIRECTION * self.last_dir if self.drift_energy / self.MAX_DRIFT_ENERGY > self.DRIFT_GFX_MIN_PERCENTAGE else 0
    
    def v2_clamp(self, val: pygame.Vector2, max: pygame.Vector2):
            clamp = pygame.math.clamp
            return pygame.Vector2(clamp(val.x, -max.x, max.x), clamp(val.y, -max.y, max.y))
    
    
    
    # Point-polygon intersections
    @staticmethod
    def point_inside_polygon(point: pygame.Vector2, polygon: list[pygame.Vector2]) -> bool:
        point2 = point + pygame.Vector2(500, 0)
        point3 = point + pygame.Vector2(-500, 0)
        ctr_intersections = 0
        num_vertices = len(polygon)
        i = 0
        while i < num_vertices - 1:
            a, b = polygon[i], polygon[i + 1]
            if Car.segments_intersect(point, point2, a, b):
                ctr_intersections += 1
            i += 1
        return ctr_intersections % 2 == 1
    
    @staticmethod
    def segment_intersects_polygon(a1: pygame.Vector2, a2: pygame.Vector2, polygon: list[pygame.Vector2]) -> tuple[int, int] | None:
        num_vertices = len(polygon)
        i = 0
        while i < num_vertices - 1:
            a, b = polygon[i], polygon[i + 1]
            if Car.segments_intersect(a1, a2, a, b):
                return (i, i + 1)
            i += 1
        return None
    
    @staticmethod
    def segments_intersect(a1: pygame.Vector2, a2: pygame.Vector2, b1: pygame.Vector2, b2: pygame.Vector2) -> bool:
        # Thanks @Grumdrig and @i_4_got on stack overflow
        def ccw(A,B,C):
            return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
        return ccw(a1,b1,b2) != ccw(a2,b1,b2) and ccw(a1,a2,b1) != ccw(a1,a2,b2)
    
    
    
    @staticmethod
    def create_shadow(source: pygame.Surface, alpha: int = 64) -> pygame.Surface:
        surf = pygame.Surface(source.get_size(), source.get_flags())
        surf.blit(source, (0, 0))
        surf.fill(pygame.Color(0, 0, 0), special_flags=pygame.BLEND_MULT)
        surf.set_alpha(alpha)
        return surf
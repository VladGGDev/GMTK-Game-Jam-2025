import engine, pygame, random
from engine.spritesheet import SpriteSheet

from game.actors.car import Car
from game.actors.scoremanager import ScoreManager
from game.actors.obstacle import Obstacle
from game.actors.decalmanager import DecalManager
from game.actors.pausemenu import PauseMenu
from game.actors.enemyspawner import EnemySpawner

from game.utility.circlecollidersolver import solve_all_circle_collisions


class CarScene(engine.Scene):
    MAP_SIZE = (1024, 1024)
    HALF_MAP_SIZE = (MAP_SIZE[0] // 2, MAP_SIZE[1] // 2)
    
    def __init__(self):
        self.ROAD_WIDTH = 72
        def random_position() -> tuple[int, int]:
            return (random.randrange(-CarScene.HALF_MAP_SIZE[0], CarScene.HALF_MAP_SIZE[0]),
                random.randrange(-CarScene.HALF_MAP_SIZE[1], CarScene.HALF_MAP_SIZE[1]))
        
        # Generating decoration
        self.deco_tiles = SpriteSheet("game/sprites/Decorations.png", (8, 8))
        self.background = pygame.image.load("game/sprites/Sand Background.png")
        DECORATION_COUNT = 2000
        self.decorations = list[tuple[float, float, int]]()
        for _ in range(DECORATION_COUNT):
            rand_pos = random_position()
            if abs(rand_pos[0]) <= self.ROAD_WIDTH / 2 + 8:
                continue
            self.decorations.append((rand_pos[0], rand_pos[1], random.randrange(0, self.deco_tiles.get_num_cells())))
        
        # Initialize obstacle actors
        OBSTACLE_COUNT = 50
        obstacle_sheet = SpriteSheet("game/sprites/Obstacles.png", (32, 32))
        obstacle_settings = [
            (2.5, (0.5, 0.9), 0),
            (2.5, (0.5, 0.9), 1),
            (7, (0.5, 0.8), 2),
            (6, (0.48, 0.8), 3),
        ]
        obstacles = list[engine.Actor]()
        for _ in range(OBSTACLE_COUNT):
            rand_pos = random_position()
            if abs(rand_pos[0]) <= self.ROAD_WIDTH / 2 + 8:
                continue
            settings = random.choice(obstacle_settings)
            obstacles.append(Obstacle(rand_pos, settings[0], obstacle_sheet.texture, settings[1], obstacle_sheet[settings[2]]))
        
        # Adding actors
        super().__init__([ScoreManager(), DecalManager(), Car(), PauseMenu(), EnemySpawner()] + obstacles)
    
    def fixed_update(self):
        super().fixed_update()
        solve_all_circle_collisions({"Obstacle", "Explosion"})
    
    def draw(self):
        # Draw background
        engine.draw_passes["Main"].blit(-9999999, self.background, (-256, -256))
        engine.draw_passes["Main"].blit(-9999999, self.background, (-256, 256))
        engine.draw_passes["Main"].blit(-9999999, self.background, (256, -256))
        engine.draw_passes["Main"].blit(-9999999, self.background, (256, 256))
        # Draw decorations
        for deco in self.decorations:
            pos = (deco[0], deco[1])
            if engine.draw_passes["Main"].camera.rect.collidepoint(pos):
                engine.draw_passes["Main"].blit(pos[1], self.deco_tiles.texture, pos, source_rect=self.deco_tiles[deco[2]])
        
        # Draw road
        ROAD_LINE_DISTANCE = 16
        ROAD_LINE_LENGTH = 16
        ROAD_LINE_WIDTH = 2
        ROAD_MARGIN_LINE_PADDING = 4
        ROAD_MARGIN_LINE_WIDTH = 2
        ROAD_BLACK_COLOR = pygame.Color(79, 82, 117)
        ROAD_WHITE_COLOR = pygame.Color(230, 232, 250)
        ROAD_YELLOW_COLOR = pygame.Color(255, 218, 36)
        engine.draw_passes["Main"].blit(-9999, engine.DrawPass.get_pixel(ROAD_BLACK_COLOR, (self.ROAD_WIDTH, CarScene.MAP_SIZE[1])), (0, 0))
        engine.draw_passes["Main"].blit(-9999, engine.DrawPass.get_pixel(ROAD_YELLOW_COLOR, (ROAD_MARGIN_LINE_WIDTH, CarScene.MAP_SIZE[1])), (-self.ROAD_WIDTH / 2 + ROAD_MARGIN_LINE_PADDING, 0))
        engine.draw_passes["Main"].blit(-9999, engine.DrawPass.get_pixel(ROAD_YELLOW_COLOR, (ROAD_MARGIN_LINE_WIDTH, CarScene.MAP_SIZE[1])), (self.ROAD_WIDTH / 2 - ROAD_MARGIN_LINE_PADDING, 0))
        # Draw road lines
        for y in range(-int(CarScene.HALF_MAP_SIZE[1] - ROAD_LINE_LENGTH / 2), int(CarScene.HALF_MAP_SIZE[1] + ROAD_LINE_LENGTH / 2), ROAD_LINE_DISTANCE + ROAD_LINE_LENGTH):
            engine.draw_passes["Main"].blit(-9999, engine.DrawPass.get_pixel(ROAD_WHITE_COLOR, (ROAD_LINE_WIDTH, ROAD_LINE_LENGTH)), (0, y))
        
        super().draw()
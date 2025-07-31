import engine, pygame, random
from engine.spritesheet import SpriteSheet
from game.actors.car import Car
from game.actors.obstacle import Obstacle
from game.utility.circlecollidersolver import solve_all_circle_collisions


class CarScene(engine.Scene):
    def __init__(self):
        self.MAP_SIZE = (1536, 1536) # Halfway between 1024 and 2048
        self.HALF_MAP_SIZE = (self.MAP_SIZE[0] / 2, self.MAP_SIZE[1] / 2)
        self.ROAD_WIDTH = 72
        def random_position() -> tuple[float, float]:
            return (random.uniform(-self.HALF_MAP_SIZE[0], self.HALF_MAP_SIZE[0]),
                random.uniform(-self.HALF_MAP_SIZE[1], self.HALF_MAP_SIZE[1]))
        
        # Generating decoration
        DECORATION_COUNT = 2000
        self.decorations = list[tuple[float, float]]()
        for _ in range(DECORATION_COUNT):
            self.decorations.append(random_position())
        
        # Initialize actors
        OBSTACLE_COUNT = 100
        obstacles = list[engine.Actor]()
        for _ in range(OBSTACLE_COUNT):
            rand_pos = random_position()
            if abs(rand_pos[0]) <= self.ROAD_WIDTH / 2 + 8:
                continue
            obstacles.append(Obstacle(rand_pos, 2, engine.DrawPass.get_pixel(pygame.Color("green"), (4, 64)), (0.5, 1)))
        super().__init__([Car()] + obstacles)
    
    def update(self):
        if engine.get_key_down(pygame.K_ESCAPE):
            engine.running = False
        super().update()
    
    def fixed_update(self):
        super().fixed_update()
        solve_all_circle_collisions({"Obstacle"})
    
    def draw(self):
        # Draw decorations
        for deco in self.decorations:
            engine.draw_passes["Main"].blit(-9999999, engine.DrawPass.get_pixel(pygame.Color(255, 255, 255, 128), (8, 8)), deco)
        
        # Draw road
        ROAD_LINE_DISTANCE = 16
        ROAD_LINE_LENGTH = 16
        ROAD_LINE_WIDTH = 2
        ROAD_MARGIN_LINE_PADDING = 4
        ROAD_MARGIN_LINE_WIDTH = 2
        ROAD_BLACK_COLOR = pygame.Color(79, 82, 117)
        ROAD_WHITE_COLOR = pygame.Color(230, 232, 250)
        ROAD_YELLOW_COLOR = pygame.Color(255, 218, 36)
        engine.draw_passes["Main"].blit(-9999999, engine.DrawPass.get_pixel(ROAD_BLACK_COLOR, (self.ROAD_WIDTH, self.MAP_SIZE[1])), (0, 0))
        engine.draw_passes["Main"].blit(-9999999, engine.DrawPass.get_pixel(ROAD_YELLOW_COLOR, (ROAD_MARGIN_LINE_WIDTH, self.MAP_SIZE[1])), (-self.ROAD_WIDTH / 2 + ROAD_MARGIN_LINE_PADDING, 0))
        engine.draw_passes["Main"].blit(-9999999, engine.DrawPass.get_pixel(ROAD_YELLOW_COLOR, (ROAD_MARGIN_LINE_WIDTH, self.MAP_SIZE[1])), (self.ROAD_WIDTH / 2 - ROAD_MARGIN_LINE_PADDING, 0))
        # Draw road lines
        for y in range(-int(self.HALF_MAP_SIZE[1] - ROAD_LINE_LENGTH / 2), int(self.HALF_MAP_SIZE[1] + ROAD_LINE_LENGTH / 2), ROAD_LINE_DISTANCE + ROAD_LINE_LENGTH):
            engine.draw_passes["Main"].blit(-9999999, engine.DrawPass.get_pixel(ROAD_WHITE_COLOR, (ROAD_LINE_WIDTH, ROAD_LINE_LENGTH)), (0, y))
        
        super().draw()
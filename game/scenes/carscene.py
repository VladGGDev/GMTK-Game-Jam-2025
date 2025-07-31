import engine, pygame, random
from engine.spritesheet import SpriteSheet
from game.actors.car import Car


class CarScene(engine.Scene):
    def __init__(self):
        self.MAP_SIZE = (1536, 1536) # Halfway between 1024 and 2048
        self.HALF_MAP_SIZE = (self.MAP_SIZE[0] / 2, self.MAP_SIZE[1] / 2)
        
        # Generating decoration
        DECORATION_COUNT = 2000
        self.decorations = list[tuple[float, float]]()
        for _ in range(DECORATION_COUNT):
            self.decorations.append((
                random.uniform(-self.HALF_MAP_SIZE[0], self.HALF_MAP_SIZE[0]),
                random.uniform(-self.HALF_MAP_SIZE[1], self.HALF_MAP_SIZE[1])))
        
        # Initialize actors
        # OBSTACLE_COUNT = 250
        # obstacles = list[engine.Actor]()
        # for _ in range(OBSTACLE_COUNT):
        #     obstacles.append((
        #         random.uniform(-self.HALF_MAP_SIZE[0], self.HALF_MAP_SIZE[0]),
        #         random.uniform(-self.HALF_MAP_SIZE[1], self.HALF_MAP_SIZE[1])))
        # super().__init__([Car()] + obstacles)
        super().__init__([Car()])
    
    def update(self):
        if engine.get_key_down(pygame.K_ESCAPE):
            engine.running = False
        super().update()
    
    def draw(self):
        # Draw road
        ROAD_WIDTH = 72
        ROAD_LINE_DISTANCE = 16
        ROAD_LINE_LENGTH = 16
        ROAD_LINE_WIDTH = 2
        ROAD_MARGIN_LINE_PADDING = 4
        ROAD_MARGIN_LINE_WIDTH = 2
        ROAD_BLACK_COLOR = pygame.Color(79, 82, 117)
        ROAD_WHITE_COLOR = pygame.Color(230, 232, 250)
        ROAD_YELLOW_COLOR = pygame.Color(255, 218, 36)
        engine.draw_passes["Main"].blit(-5, engine.DrawPass.get_pixel(ROAD_BLACK_COLOR, (ROAD_WIDTH, self.MAP_SIZE[1])), (0, 0))
        engine.draw_passes["Main"].blit(-5, engine.DrawPass.get_pixel(ROAD_YELLOW_COLOR, (ROAD_MARGIN_LINE_WIDTH, self.MAP_SIZE[1])), (-ROAD_WIDTH / 2 + ROAD_MARGIN_LINE_PADDING, 0))
        engine.draw_passes["Main"].blit(-5, engine.DrawPass.get_pixel(ROAD_YELLOW_COLOR, (ROAD_MARGIN_LINE_WIDTH, self.MAP_SIZE[1])), (ROAD_WIDTH / 2 - ROAD_MARGIN_LINE_PADDING, 0))
        # Draw road lines
        for y in range(-int(self.HALF_MAP_SIZE[1] - ROAD_LINE_LENGTH / 2), int(self.HALF_MAP_SIZE[1] + ROAD_LINE_LENGTH / 2), ROAD_LINE_DISTANCE + ROAD_LINE_LENGTH):
            engine.draw_passes["Main"].blit(-5, engine.DrawPass.get_pixel(ROAD_WHITE_COLOR, (ROAD_LINE_WIDTH, ROAD_LINE_LENGTH)), (0, y))
        
        # Draw decorations
        for deco in self.decorations:
            engine.draw_passes["Main"].blit(-99, engine.DrawPass.get_pixel(pygame.Color(255, 255, 255, 128), (8, 8)), deco)
        
        super().draw()
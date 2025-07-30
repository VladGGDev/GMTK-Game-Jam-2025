import engine, pygame
import game
import random


class TurnTestScene(engine.Scene):
    def __init__(self):
        super().__init__([
            TurnTestGameGrid((8, 8), "Main"),
            Player((0, 0)),
            # Enemy((10, 10))
        ])


class TurnTestGameGrid(game.GameGrid):
    def generate(self):
        MAP_SIZE = 30
        OBSTACLE_CHANCE = 0.15
        ENEMY_CHANCE = 0.01
        for y in range(int(-MAP_SIZE / 2), MAP_SIZE // 2 + 1):
            for x in range(int(-MAP_SIZE / 2), MAP_SIZE // 2 + 1):
                # Generate tiles
                if x == 0 and y == 0:
                    color = pygame.Color("cornflowerblue")
                    walkable = True
                elif random.random() < OBSTACLE_CHANCE:
                    color = pygame.Color("Black")
                    walkable = False
                else:
                    color = pygame.Color("white") if (x + y) % 2 == 0 else pygame.Color("Gray80")
                    walkable = True
                    
                    # Spawn enemy
                    if self.manhattan_distance((0, 0), (x, y)) >= 5 and random.random() < ENEMY_CHANCE:
                        engine.scene_manager.current_scene.create_actor(Enemy((x, y)))
                self.tiles[(x, y)] = game.Tile(engine.DrawPass.get_pixel(color, (8, 8)), walkable)


class Player(game.MovingGameActor):
    """The player-controlled actor.\n
    **No other** GameActors must exist before this in the scene.actors list in order for it to have the most priority in turns."""
    def __init__(self, start_gridpos: tuple[int, int]):
        super().__init__(start_gridpos)
        self.pathfind_data = dict[tuple[int, int], int]()
        
    def update(self):
        if engine.get_key_down(pygame.K_ESCAPE):
            engine.running = False
        
        
        # WASD controls
        if engine.get_key_down(pygame.K_d):
            input = (1, 0)
        elif engine.get_key_down(pygame.K_a):
            input = (-1, 0)
        elif engine.get_key_down(pygame.K_w):
            input = (0, -1)
        elif engine.get_key_down(pygame.K_s):
            input = (0, 1)
        else:
            input = (0, 0)
        
        if input != (0, 0) or engine.get_key_down(pygame.K_SPACE):
            # Reserve own movements
            prev_pos = self.grid.get_gridpos_by_actor(self)
            new_pos = (prev_pos[0] + input[0], prev_pos[1] + input[1])
            if self.grid.walkable_tile(new_pos) and new_pos not in self.grid.actors:
                self.move(new_pos)
            
            # Manage the turn manager
            self.pathfind_data = self.grid.pathfind(self.grid.get_gridpos_by_actor(self), 3)
            self.grid.do_turn()
    
    def turn(self, curr_pos: tuple[int, int]):
        # return super().turn(curr_gridpos)
        pass
    
    def draw(self):
        engine.draw_passes["Main"].blit(
            5,
            engine.DrawPass.get_pixel(pygame.Color("gray30")),
            self.postween.result(),
            (6, 6)
        )
        for p in self.pathfind_data:
            if self.pathfind_data[p] == game.PATHFIND_UP:
                col = pygame.Color("red")
            elif self.pathfind_data[p] == game.PATHFIND_RIGHT:
                col = pygame.Color("green")
            elif self.pathfind_data[p] == game.PATHFIND_DOWN:
                col = pygame.Color("blue")
            elif self.pathfind_data[p] == game.PATHFIND_LEFT:
                col = pygame.Color("yellow")
            else: # PATHFIND_TARGET
                col = pygame.Color("magenta")
            col.a = 96
            engine.draw_passes["Main"].blit(
                1,
                engine.DrawPass.get_pixel(col),
                self.grid.get_worldpos_from_grid(p),
                (8, 8)
            )


class Enemy(game.MovingGameActor):
    def start(self):
        super().start()
        self.player = engine.scene_manager.current_scene.get_actor(Player)
    
    def turn(self, curr_pos: tuple[int, int]):
        # curr_pos = self.grid.get_gridpos_by_actor(self)
        if curr_pos not in self.player.pathfind_data:
            return
        dir = self.player.pathfind_data[curr_pos]
        new_pos = self.pathfind_new_pos(dir, curr_pos)
        
        if self.player.pathfind_data[new_pos] == game.PATHFIND_TARGET:
            # Hit the player
            engine.scene_manager.current_scene.destroy_actor(self.player) # This is temporary to simulate damage
            self.grid.remove_from_grid(self.player)
        else:
            # Move towards player if possible
            if new_pos not in self.grid.actors:
                self.move(new_pos)
            else:
                # If can't move there, try moving along the direction if it's safe
                dir = self.player.pathfind_data[new_pos]
                new_pos = self.pathfind_new_pos(dir, curr_pos)
                if self.grid.walkable_tile(new_pos) and new_pos not in self.grid.actors:
                    self.move(new_pos)
    
    def draw(self):
        engine.draw_passes["Main"].blit(
            5,
            engine.DrawPass.get_pixel(pygame.Color("red")),
            self.postween.result(),
            (6, 6)
        )
    
    # ===== Utility =====
    def pathfind_new_pos(self, pathfind_dir: int, gridpos: tuple[int, int]) -> tuple[int, int]:
        """Adds the pathfind direction to the gridpos passed"""
        if pathfind_dir == game.PATHFIND_UP:
            return (gridpos[0], gridpos[1] - 1)
        elif pathfind_dir == game.PATHFIND_RIGHT:
            return (gridpos[0] + 1, gridpos[1])
        elif pathfind_dir == game.PATHFIND_DOWN:
            return (gridpos[0], gridpos[1] + 1)
        elif pathfind_dir == game.PATHFIND_LEFT:
            return (gridpos[0] - 1, gridpos[1])
        else: # pathfind_dir == game.PATHFIND_TARGET:
            return (gridpos[0], gridpos[0])
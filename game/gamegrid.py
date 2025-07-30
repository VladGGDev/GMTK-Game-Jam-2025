import engine
import game
from abc import ABC, abstractmethod


# Constants for pathfinding
PATHFIND_UP = 1
PATHFIND_RIGHT = 2
PATHFIND_DOWN = 3
PATHFIND_LEFT = 4
PATHFIND_TARGET = 0

class GameGrid(engine.Actor, ABC):
    def __init__(self, cell_size: tuple[int, int], draw_pass):
        self.cell_size = cell_size
        self.tiles = dict[tuple[int, int], game.Tile]()
        self.actors = dict[tuple[int, int], game.GameActor]()
        self.pos_actors = dict[game.GameActor, tuple[int, int]]()
        self.remove_queue = list[game.GameActor]()
        self.draw_pass = draw_pass
    
    def start(self):
        super().start()
        self.generate()
    
    # ===== Utility =====
    def get_worldpos_from_grid(self, gridpos: tuple[int, int]) -> tuple[float, float]:
        """Gets the world position of a grid position based on the grid cell size."""
        return (self.cell_size[0] * gridpos[0], self.cell_size[1] * gridpos[1])
    
    def get_worldpos_from_actor(self, actor: game.GameActor) -> tuple[float, float]:
        """Gets the world position of an actor based on the grid cell size."""
        if actor not in self.pos_actors:
            raise ValueError("Actor is not on the grid")
        return self.get_worldpos_from_grid(self.pos_actors[actor])
    
    def move_actor(self, actor: game.GameActor, new_pos: tuple[int, int]):
        """Moves the actor to a new position and deletes the previous or creates a new grid position"""
        if actor in self.pos_actors:
            # Remove from the previous position if it exists
            self.actors.pop(self.pos_actors[actor], None)
        self.actors[new_pos] = actor
        self.pos_actors[actor] = new_pos
    
    def remove_from_grid(self, actor: game.GameActor):
        self.remove_queue.append(actor)
    
    def get_actor_by_gridpos(self, position: tuple[int, int]) -> game.GameActor:
        return self.actors[position]
    
    def get_gridpos_by_actor(self, actor: game.GameActor) -> tuple[int, int]:
        return self.pos_actors[actor]
    
    def walkable_tile(self, gridpos: tuple[int, int], ignore_unwalkable: bool = False):
        if gridpos not in self.tiles: return False
        elif ignore_unwalkable: return True
        else: return self.tiles[gridpos].walkable
    
    @staticmethod
    def manhattan_distance(gridpos_a: tuple[int, int], gridpos_b: tuple[int, int]) -> int:
        """Computes the Manhattan distance or chessboard distance between 2 grid points"""
        return abs(gridpos_b[0] - gridpos_a[0]) + abs(gridpos_b[1] - gridpos_a[1])
    
    
    # ===== Engine logic =====
    def do_turn(self):
        for actor in self.pos_actors:
            actor.turn(self.pos_actors[actor])
        
        # Remove all actors from the remove queue
        for actor in self.remove_queue:
            self.actors.pop(self.pos_actors[actor])
            self.pos_actors.pop(actor)
        self.remove_queue.clear()
    
    @abstractmethod
    def generate(self):
        pass
    
    
    # ===== Pathfinding =====
    def pathfind(self, gridpos: tuple[int, int], min_distance: int, *, ignore_walkable: bool = False):
        """Computes a Lee algorithm flood fill and returns a dict with grid positions with the values of PATHFIND_X constants\n
        :param gridpos: Position on the grid to pathfind to\n
        :param min_distance: The minimum distance the pathfind will stretch to\n
        :param ignore_walkable: Should walk over unwalkable tiles?"""
        # Utility function
        def pos_around(point: tuple[int, int]):
            yield (PATHFIND_RIGHT, (point[0] - 1, point[1]))
            yield (PATHFIND_UP, (point[0], point[1] + 1))
            yield (PATHFIND_LEFT, (point[0] + 1, point[1]))
            yield (PATHFIND_DOWN, (point[0], point[1] - 1))
        
        max_steps = 1 + 2 * (min_distance - 1) * min_distance
        
        from queue import SimpleQueue
        q = SimpleQueue()
        curr_pos = gridpos
        q.put(curr_pos)
        m: dict[tuple[int, int], int] = {curr_pos: PATHFIND_TARGET}
        
        while not q.empty() and max_steps > 0:
            max_steps -= 1
            curr_pos = q.get(False)
            for path in pos_around(curr_pos):
                if self.walkable_tile(path[1], ignore_walkable) and path[1] not in m:
                    m[path[1]] = path[0]
                    q.put(path[1])
                    # max_steps -= 1
        return m
    
    
    # ===== Actor logic =====
    def draw(self):
        """Draw all tiles"""
        for pos in self.tiles:
            engine.draw_passes[self.draw_pass].blit(
                0,
                self.tiles[pos].sprite,
                self.get_worldpos_from_grid(pos)
            )
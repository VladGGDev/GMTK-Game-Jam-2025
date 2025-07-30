import engine, engine.collider, engine.tweening
import game
from abc import ABC, abstractmethod


class GameActor(engine.Actor, ABC):
    """The base grid-and-turn-based actor for this game"""
    def __init__(self, start_gridpos: tuple[int, int]):
        super().__init__(engine.collider.NoCollider)
        self._start_gridpos = start_gridpos
        # self.stats = ???
    
    def start(self):
        self.grid = engine.scene_manager.current_scene.get_actor(game.GameGrid)
        self.grid.move_actor(self, self._start_gridpos) # Initialize position on grid
    
    @abstractmethod
    def turn(self, curr_pos: tuple[int, int]):
        """The actor must move, give and take damage here.\n
        :param curr_pos: The current grid position of the game actor"""
        pass


class MovingGameActor(GameActor):
    """A GameActor which implements 'move' method which tweens between the previous grid position to a new one using 'postween'"""
    def start(self):
        """Initialize the postween"""
        super().start()
        worldpos = self.grid.get_worldpos_from_grid(self._start_gridpos)
        self.postween = engine.tweening.Tween(worldpos, worldpos, 0.2, engine.tweening.easingfuncs.ease_out_cubic)
    
    def move(self, new_gridpos: tuple[int, int]):
        """Moves the actor to new_gridpos and tweens between positions"""
        prev_worldpos = self.grid.get_worldpos_from_actor(self)
        new_worldpos = self.grid.get_worldpos_from_grid(new_gridpos)
        self.postween = self.postween.with_start(prev_worldpos).with_target(new_worldpos)
        self.postween.restart()
        self.grid.move_actor(self, new_gridpos)
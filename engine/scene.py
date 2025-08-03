from engine.actor import Actor
from engine.camera import Camera
import engine.collider
from typing import Any


class Scene(Actor):
    def __init__(self, actors: list[Actor] = []):
        self.actors = actors
    

    def start(self):
        for actor in self.actors:
            actor.start()

    def update(self):
        for actor in self.actors:
            actor.update()

    def fixed_update(self):
        for actor in self.actors:
            actor.fixed_update()

    def end(self):
        engine.collider.all_colliders.clear()
        for actor in self.actors:
            actor.end()

    def draw(self):
        for actor in self.actors:
            actor.draw()
    
    
    def get_actor[TActor](self, actor_type: type[TActor]) -> TActor:
        for actor in self.actors:
            if isinstance(actor, actor_type):
                return actor
        raise ValueError(f"Scene has no actor of type {type(actor_type)}")
    
    def try_get_actor[TActor](self, actor_type: type[TActor]) -> TActor | None:
        for actor in self.actors:
            if isinstance(actor, actor_type):
                return actor
        return None
    
    def get_actors[TActor](self, actor_type: type[TActor]) -> list[TActor]:
        res = []
        for actor in self.actors:
            if isinstance(actor, actor_type):
                res.append(actor)
        return res
    
    
    def create_actor(self, actor: Actor):
        self.actors.append(actor)
        actor.start()
    
    def destroy_actor(self, actor: Actor):
        engine.collider.all_colliders.remove(actor.collider)
        self.actors.remove(actor)
        actor.end()
        


class SceneManager(Actor):
    def __init__(self, scenes: dict[Any, tuple[type[Scene], tuple[Any, ...]]], start_scene: Any):
        self.scenes = scenes
        self.skip_next_draw = False
        if start_scene not in scenes:
            raise ValueError("start_scene is not a key in the scenes dict")
        self.current_scene = self._create_scene(start_scene)
        engine.collider.all_colliders.clear()

    # Current scene manipulation
    def change_scene(self, new_scene_key: Any):
        if new_scene_key not in self.scenes:
            raise ValueError("new_scene_key is not a key in the scenes dict")
        self.end()
        self.current_scene = self._create_scene(new_scene_key)
        engine.collider.all_colliders.clear()
        self.skip_next_draw = True
        self.start()

    # Engine related functions
    def start(self):
        self.current_scene.start()

    def update(self):
        self.current_scene.update()

    def fixed_update(self):
        self.current_scene.fixed_update()

    def end(self):
        self.current_scene.end()

    def draw(self):
        if self.skip_next_draw:
            self.skip_next_draw = False
            return
        self.current_scene.draw()
    
    # Scene dict functions
    def _create_scene(self, key: Any) -> Scene:
        if key not in self.scenes:
            raise ValueError("new_scene_key is not a key in the scenes dict")
        scene_t = self.scenes[key][0]
        return scene_t(*self.scenes[key][1])
    
    def add_scene(self, key: Any, scene_type: type[Scene], *params: Any):
        self.scenes[key] = (scene_type, *params)
    
    def delete_scene(self, key: Any):
        if key not in self.scenes:
            raise ValueError("new_scene_key is not a key in the scenes dict")
        self.scenes.pop(key)

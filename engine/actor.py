from abc import ABC, abstractmethod
import engine.collider


class Actor(ABC):
    @abstractmethod
    def __init__(self, collider: engine.collider.Collider):
        self.collider = collider

    def start(self):
        pass

    def update(self):
        pass

    def fixed_update(self):
        pass

    def end(self):
        pass

    def draw(self):
        pass

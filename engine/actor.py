from abc import ABC, abstractmethod
import engine.collider


class Actor(ABC):
    @abstractmethod
    def __init__(self):
        self.collider = engine.collider.NoCollider()

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

from abc import ABC, abstractmethod


class Actor(ABC):
    @abstractmethod
    def __init__(self, collider):
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

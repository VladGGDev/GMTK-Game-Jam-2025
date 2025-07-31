from abc import ABC, abstractmethod
from pygame import Vector2, Rect


class Collider(ABC):
    @abstractmethod
    def __init__(self, position: Vector2, tag: str = ""):
        self.position = position
        self.tag = tag
        all_colliders.append(self)

    @abstractmethod
    def check(self, other: "Collider") -> bool:
        pass

    def relative_position_to(self, other: "Collider") -> Vector2:
        return other.position - self.position


class NoCollider(Collider):
    def __init__(self, position: Vector2 = Vector2(0, 0)):
        super().__init__(position)
    
    def check(self, other: Collider) -> bool:
        return False


class BoxCollider(Collider):
    def __init__(self, center: Vector2, size: tuple[float, float], tag: str = ""):
        super().__init__(center, tag)
        self.size = size

    @property
    def half_size(self) -> tuple[float, float]:
        return (self.size[0] / 2, self.size[1] / 2)

    @property
    def rect(self) -> Rect:
        return Rect(
            self.position[0] - self.half_size[0],
            self.position[1] - self.half_size[1],
            self.size[0],
            self.size[1])

    def check(self, other: Collider) -> bool:
        if isinstance(other, BoxCollider):
            return self.rect.colliderect(other.rect)
        elif isinstance(other, CircleCollider):
            rel_pos = self.relative_position_to(other)
            rel_pos = Vector2(abs(rel_pos.x), abs(rel_pos.y))

            # Check if too far
            if rel_pos.x > other.radius + self.half_size[0] or rel_pos.y > other.radius + self.half_size[1]:
                return False

            # Check if too close
            if rel_pos.x <= self.half_size[0] or rel_pos.x <= self.half_size[1]:
                return True

            # Check corners
            corner_dist_sq = rel_pos.distance_squared_to(
                Vector2(self.half_size))
            return corner_dist_sq <= other.radius * other.radius
        return False


class CircleCollider(Collider):
    def __init__(self, position: Vector2, radius: float, tag: str = ""):
        super().__init__(position, tag)
        self.radius = radius

    @property
    def diameter(self) -> float:
        return self.radius * 2

    def check(self, other: Collider) -> bool:
        if isinstance(other, CircleCollider):
            return self.position.distance_squared_to(other.position) < \
                (self.radius + other.radius) * (self.radius + other.radius)
        elif isinstance(other, BoxCollider):
            return other.check(self)
        return False


all_colliders = list[Collider]()

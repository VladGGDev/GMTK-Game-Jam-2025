"""Common linear interpolation functions"""
from engine.lerputil import lerp
from pygame import Vector2, Vector3

def vector2_lerp(a: Vector2, b: Vector2, t: float) -> Vector2:
    return Vector2(lerp(a.x, b.x, t), lerp(a.y, b.y, t))

def vector3_lerp(a: Vector3, b: Vector3, t: float) -> Vector3:
    return Vector3(lerp(a.x, b.x, t), lerp(a.y, b.y, t), lerp(a.z, b.z, t))

def tuple_lerp(a: tuple, b: tuple, t: float) -> tuple:
    return tuple((lerp(ai, bi, t) for ai, bi in zip(a, b)))

def color_lerp(a: tuple[float, float, float, float], b: tuple[float, float, float, float], t: float) -> tuple[float, float, float, float]:
    return (lerp(a[0], b[0], t),
            lerp(a[1], b[1], t),
            lerp(a[2], b[2], t),
            lerp(a[3], b[3], t))

def no_lerp[T](a: T, b: T, t: float) -> T:
    return a
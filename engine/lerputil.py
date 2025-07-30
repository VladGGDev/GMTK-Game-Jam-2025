from pygame.math import clamp


def lerp(a: float, b: float, t: float) -> float:
    """Returns a value at t ratio between a and b. Parameter 't' expects a value between 0 and 1"""
    return a * (1 - t) + b * t


def lerp_clamped(a: float, b: float, t: float) -> float:
    """Same as lerp, but t is clamped between 0 and 1"""
    t = clamp(t, 0, 1)
    return a * (1 - t) + b * t


def inverse_lerp(a: float, b: float, val: float) -> float:
    """Returns the ratio between a and b of val. Parameter 'val' expects a value between a and b"""
    return val / (b - a)


def remap(val: float, a1: float, b1: float, a2: float, b2: float) -> float:
    """Remaps parameter 'val' from range [a1, b1] to [a2, b2]"""
    return lerp(a2, b2, inverse_lerp(a1, b1, val))

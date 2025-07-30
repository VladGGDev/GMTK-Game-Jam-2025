"""Contains functions which return easing functions based on parameters"""
from math import pi, sin
from typing import Callable

# Constants
__C4 = 2 * pi / 3

def ease_in_back_custom(amount: float) -> Callable[[float], float]:
    return lambda x : (amount + 1) * x * x * x - amount * x * x

def ease_out_back_custom(amount: float) -> Callable[[float], float]:
    return lambda x : 1 + (amount + 1) * (x - 1)**3 + amount * (x - 1)**2

def ease_in_out_back_custom(amount_in: float, amount_out: float) -> Callable[[float], float]:
    return lambda x : 2*x*2*x * ((amount_in + 1) * 2 * x - amount_in) / 2 if x < 0.5 else\
        ((2 * x - 2)**2 * ((amount_out + 1) * (x * 2 - 2) + amount_out) + 2) / 2

def ease_in_elastic_custom(revolutions: int) -> Callable[[float], float]:
    return lambda x : 0 if x == 0 else\
        1 if x == 1 else\
        -(2*(10 * x - 10)) * sin((x * (revolutions * 3 + 1) - 10.75) * __C4)

def ease_out_elastic_custom(revolutions: int) -> Callable[[float], float]:
    return lambda x : 0 if x == 0 else\
        1 if x == 1 else\
        2**(-10 * x) * sin((x * (revolutions * 3 + 1) - 0.75) * __C4) + 1

def yo_yo(exponent: float) -> Callable[[float], float]:
    return lambda x : 1 - abs(((x - 0.5) * 2)**exponent)

def quad_yo_yo(x: float) -> float:
    return 1 - ((x - 0.5) * 2)**2

def cubic_yo_yo(x: float) -> float:
    return 1 - abs(((x - 0.5) * 2)**3)

def linear_yo_yo(fadein: float = 0.5, fadeout: float = 0.5) -> Callable[[float], float]:
    stay = 1 - fadein - fadeout
    return lambda x : x / fadein if x <= fadein else\
        1 - (x - fadein - stay) / fadeout if x >= fadein + stay else\
        1
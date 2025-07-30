# Thanks https://easings.net/ for all easing functions in this file!

from math import pi, sin, cos, sqrt

# Constants
__C1 = 1.70158
__C2 = __C1 * 1.525
__C3 = __C1 + 1
__C4 = 2 * pi / 3
__C5 = 2 * pi / 4.5
__N1 = 7.5625
__D1 = 2.75


def linear(x: float) -> float:
    return x

def ease_in_sine(x: float) -> float:
    return 1 - cos(x * pi / 2)

def ease_out_sine(x: float) -> float:
    return sin(x * pi / 2)

def ease_in_out_sine(x: float) -> float:
    return -(cos(pi * x) - 1) / 2

def ease_in_quad(x: float) -> float:
    return x * x

def ease_out_quad(x: float) -> float:
    return 1 - (1 - x) * (1 - x)

def ease_in_out_quad(x: float) -> float:
    return 2 * x * x if x < 0.5 else 1 - (-2 * x + 2)**2 / 2

def ease_in_cubic(x: float) -> float:
    return x * x * x

def ease_out_cubic(x: float) -> float:
    return 1 - (1 - x)**3

def ease_in_out_cubic(x: float) -> float:
    return 4 * x * x * x if x < 0.5 else 1 - (-2 * x + 2)**3 / 2

def ease_in_quart(x: float) -> float:
    return x * x * x * x

def ease_out_quart(x: float) -> float:
    return 1 - (1 - x)**4

def ease_in_out_quart(x: float) -> float:
    return 8 * x * x * x * x if x < 0.5 else 1 - (-2 * x + 2)**4 / 2

def ease_in_quint(x: float) -> float:
    return x * x * x * x * x

def ease_out_quint(x: float) -> float:
    return 1 - (1 - x)**5

def ease_in_out_quint(x: float) -> float:
    return 16 * x * x * x * x * x if x < 0.5 else 1 - (-2 * x + 2)**5 / 2

def ease_in_expo(x: float) -> float:
    return 0 if x == 0 else 2**(10 * x - 10)

def ease_out_expo(x: float) -> float:
    return 1 if x == 1 else 1 - 2**(-10 * x)

def ease_in_out_expo(x: float) -> float:
    return 0 if x == 0 else\
        1 if x == 1 else\
        2**(20 * x - 10) / 2 if x < .5 else\
        (2 - 2**(-20 * x + 10)) / 2

def ease_in_circ(x: float) -> float:
    return 1 - sqrt(1 - x*x)

def ease_out_circ(x: float) -> float:
    return sqrt(1 - (x - 1)*(x - 1))

def ease_in_out_circ(x: float) -> float:
    return (1 - sqrt(1 - 2 * x * 2 * x)) / 2 if x < 0.5 else (sqrt(1 - (-2 * x + 2)**2) + 1) / 2

def ease_in_back(x: float) -> float:
    return __C3 * x * x * x - __C1 * x * x

def ease_out_back(x: float) -> float:
    return 1 + __C3 * (x - 1)**3 + __C1 * (x - 1)**2

def ease_in_out_back(x: float) -> float:
    return (2*x*2*x) * ((__C2 + 1) * 2 * x - __C2) / 2 if x < 0.5 else ((2 * x - 2)**2 * ((__C2 + 1) * (x * 2 - 2) + __C2) + 2) / 2

def ease_in_elastic(x: float) -> float:
    return 0 if x == 0 else\
        1 if x == 1 else\
        -(2**(10 * x - 10)) * sin((x * 10 - 10.75) * __C4)

def ease_out_elastic(x: float) -> float:
    return 0 if x == 0 else\
        1 if x == 1 else\
        2**(-10 * x) * sin((x * 10 - 0.75) * __C4) + 1

def ease_in_out_elastic(x: float) -> float:
    return 0 if x == 0 else\
        1 if x == 1 else\
        -(2**(20 * x - 10)) * sin((20 * x - 11.125) * __C5) / 2 if x < 0.5 else\
        2**(-20 * x + 10) * sin((20 * x - 11.125) * __C5) / 2 + 1

def ease_out_bounce(x: float) -> float:
    if x < 1 / __D1:
        return __N1 * x * x
    elif x < 2 / __D1:
        x -= 1.5 / __D1
        return __N1 * x * x + 0.75
    elif x < 2.5 / __D1:
        x -= 2.25 / __D1
        return __N1 * x * x + 0.9375
    else:
        x -= 2.625 / __D1
        return __N1 * x * x + 0.984375

def ease_in_bounce(x: float) -> float:
    return 1 - ease_out_bounce(1 - x)

def easeInOutBounce(x: float) -> float:
    return (1 - ease_in_bounce(1 - 2 * x)) / 2 if x < 0.5 else (1 + ease_out_bounce(2 * x - 1)) / 2

from typing import Callable
import engine, pygame
from . import easingfuncs
from . import lerpfuncs


class Tween[T]:
    def __init__(self, start: T, target: T, duration: float, 
                easingfunc: Callable[[float], float] = easingfuncs.linear,
                lerpfunc: Callable[[T, T, float], T] = lerpfuncs.tuple_lerp,
                use_unscaled_time = False) -> None:
        self.start = start
        self.target = target
        self.duration = duration
        self.easingfunc = easingfunc
        self.lerpfunc = lerpfunc
        self.use_unscaled_time = use_unscaled_time
        self.start_time = self._get_time()
    
    
    # Runtime-related methods
    def _get_time(self) -> float:
        return engine.unscaled_total_time() if self.use_unscaled_time else engine.total_time
    
    def elapsed_time(self) -> float:
        return self._get_time() - self.start_time

    def elapsed_percentage(self) -> float:
        """Return the elapsed time in percentages of total duration."""
        return pygame.math.clamp(self.elapsed_time() / max(self.duration, 0.0000001), 0, 1)    
    
    def eased_elapsed_percentage(self) -> float:
        self.elapsed_percentage
        return self.easingfunc(self.elapsed_percentage())
    
    def running(self) -> bool:
        """Return whether the running time of the tween exceeded the total duration"""
        return self.elapsed_time() <= self.duration
    
    def restart(self):
        self.start_time = self._get_time()
    
    def restart_at(self, t_percent: float):
        self.start_time = self._get_time() - self.duration * t_percent
    
    def reverse(self):
        """Reverse the start and target of this tween in place."""
        self.start, self.target = self.target, self.start
        self.restart_at(1 - self.elapsed_percentage())
    
    def set_duration(self, duration, offset = True):
        """Set the duration of this tween in place.\n
        If offset is True, the elapsed percentage will be offset to account for a change in duration."""
        if offset: 
            prev_elapsed = self.elapsed_percentage()
            self.duration = duration
            self.restart_at(prev_elapsed)
        else:
            self.duration = duration
    
    
    # Result-related methods
    def result(self) -> T:
        return self.result_at(self.elapsed_percentage())
    
    def result_at(self, t_percent: float) -> T:
        return self.lerpfunc(self.start, self.target, self.easingfunc(t_percent))
    
    
    # Dunders
    def __call__(self) -> T:
        return self.result()
    
    def __str__(self) -> str:
        return f"Tween({self.start} -> {self.target})={self.result()}"
    
    
    # Fluent interface implementation with functional programming
    @classmethod
    def new(cls, lerpfunc: Callable[[T, T, float], T] = lerpfuncs.tuple_lerp, use_unscaled_time = False) -> "Tween":
        """Return an zeroed tween to be used with functional programming methods"""
        return Tween(T.__default__, T.__default__, 0, easingfuncs.linear, lerpfunc, use_unscaled_time)
    
    def copy(self) -> "Tween":
        return Tween(self.start, self.target, self.duration, self.easingfunc, self.lerpfunc, self.use_unscaled_time)
        
    def with_start(self, start: T) -> "Tween":
        """Return a copy of this tween with start set to another value"""
        new = self.copy()
        new.start = start
        return new
    
    def with_target(self, target: T) -> "Tween":
        """Return a copy of this tween with target set to another value"""
        new = self.copy()
        new.target = target
        return new
    
    def with_duration(self, duration, offset = True) -> "Tween":
        """Return a copy of this tween with duration set to another value.\n
        If offset is True, the elapsed percentage will be offset to account for a change in duration."""
        new = self.copy()
        new.duration = duration
        if offset:
            new.restart_at(self.elapsed_percentage())
        return new
    
    def with_easingfunc(self, easingfunc: Callable[[float], float]) -> "Tween":
        """Return a copy of this tween with easingfunc set to another value"""
        new = self.copy()
        new.easingfunc = easingfunc
        return new
    
    def with_lerpfunc(self, lerpfunc: Callable[[T, T, float], T]) -> "Tween":
        """Return a copy of this tween with lerpfunc set to another value"""
        new = self.copy()
        new.lerpfunc = lerpfunc
        return new
    
    def as_reversed(self) -> "Tween":
        """Return a copy of this tween with start and target reversed."""
        new = self.copy()
        new.reverse()
        return new



class TweenSequence[T]:
    def __init__(self, *tweens: Tween[T], easingfunc: Callable[[float], float] = easingfuncs.linear, use_unscaled_time = False) -> None:
        self.easingfunc = easingfunc
        self.use_unscaled_time = use_unscaled_time
        self.start_time = self._get_time()
        self._total_duration = 0
        self._tweens = list[Tween[T]]()
        for t in tweens:
            self.add(t)
    
    
    # Adding to sequence
    def add(self, tween: Tween[T]) -> "TweenSequence":
        self._tweens.append(tween)
        self._total_duration += tween.duration
        return self
    
    def delay(self, seconds: float) -> "TweenSequence":
        """Extends the internal tween list with a an unmovable copy of the last tween.
        If this is the first operation on the tween sequence, use start_delay instead."""
        if len(self._tweens) == 0:
            raise IndexError("Cannot add a delay to an empty tween sequence. Use start_delay instead.")
        prev = self._tweens[-1]
        self._tweens.append(prev.with_start(prev.target).with_duration(seconds))
        self._total_duration += seconds
        return self
    
    def start_delay(self, seconds: float, start, use_unscaled_time=False) -> "TweenSequence":
        self._tweens.append(Tween(start, start, seconds, easingfuncs.linear, lerpfuncs.no_lerp, use_unscaled_time))
        self._total_duration += seconds
        return self
    
    
    # Runtime-related methods
    def _get_time(self) -> float:
        return engine.unscaled_total_time() if self.use_unscaled_time else engine.total_time
    
    def elapsed_time(self) -> float:
        return self._get_time() - self.start_time

    def elapsed_percentage(self) -> float:
        """Return the elapsed time in percentages of total duration."""
        return pygame.math.clamp(self.elapsed_time() / max(self._total_duration, 0.0000001), 0, 1)    
    
    def eased_elapsed_percentage(self) -> float:
        self.elapsed_percentage
        return self.easingfunc(self.elapsed_percentage())
    
    def running(self) -> bool:
        """Return whether the running time of the tween sequence exceeded the total duration"""
        return self.elapsed_time() <= self._total_duration
    
    def restart(self):
        self.start_time = self._get_time()
    
    def restart_at(self, t_percent: float):
        self.start_time = self._get_time() - self._total_duration * t_percent    
    
    
    # Result-related methods
    def result(self) -> T:
        return self.result_at(self.eased_elapsed_percentage())
    
    def result_at(self, t_percent: float) -> T:
        curr_duration = t_percent * self._total_duration
        for t in self._tweens:
            if curr_duration <= t.duration:
                return t.result_at(0 if t.duration == 0 else curr_duration / t.duration)
            else:
                curr_duration -= t.duration
        raise RuntimeError("TweenSequence did not return a result. Possibly because it has duration 0.")
    
    
    # Dunders
    def __call__(self) -> T:
        return self.result()
    
    def __str__(self) -> str:
        return f"Tween sequence({len(self._tweens)} tweens)={self.result()}"

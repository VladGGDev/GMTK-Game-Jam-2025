import pygame
import numpy as np
def pitch_shift(sound_array, pitch_factor):
    
    indices = (np.arange(0, len(sound_array), pitch_factor)).astype(int)
    indices = indices[indices < len(sound_array)]
    return sound_array[indices]



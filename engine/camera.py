from pygame import Vector2


class Camera:
    # def __init__(self, position: tuple[float, float] | Vector2 = (0, 0), height: float = 1080, aspect_ratio: float = 16/9):
    def __init__(self, position: tuple[float, float] | Vector2 = (0, 0), resolution: tuple[float, float] = (1920, 1080)):
        self.position = Vector2(position)
        self.resolution = resolution
    
    
    @property
    def height(self) -> float:
        """Modify relolution height without changing aspect ratio."""
        return self.__height
    
    @height.setter
    def height(self, value: float):
        self.__height = value
    
    
    @property
    def width(self) -> float:
        """Modify relolution width without changing aspect ratio."""
        return self.__height * self.__aspect_ratio
    
    @width.setter
    def width(self, value: float):
        self.__height = value / self.__aspect_ratio
    
    
    @property
    def aspect_ratio(self) -> float:
        return self.__aspect_ratio
    
    @aspect_ratio.setter
    def aspect_ratio(self, value: float):
        self.__aspect_ratio = value
    
    
    @property
    def resolution(self) -> tuple[float, float]:
        return (self.width, self.height)
    
    @property
    def half_resolution(self) -> tuple[float, float]:
        return (self.width / 2, self.height / 2)
    
    @resolution.setter
    def resolution(self, value: tuple[float, float]):
        self.__height = value[1]
        self.__aspect_ratio = value[0] / value[1]

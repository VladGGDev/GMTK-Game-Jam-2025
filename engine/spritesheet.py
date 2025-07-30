import engine, pygame
from pygame import Rect


class SpriteSheet:
    def __init__(self,
                file_path: str,
                cell_size: tuple[int, int],
                padding: tuple[int, int] = (0, 0),
                margin_padding: tuple[int, int] = (0, 0)):
        self.texture = pygame.image.load(file_path)
        self.cell_size = cell_size
        self.padding = padding
        self.margin_padding = margin_padding
    
    def __getitem__(self, cell_pos: tuple[int, int] | int) -> Rect:
        return self.get_rect(cell_pos)
    
    def get_grid_width(self) -> int:
        """Returns the amount of cells in one row"""
        return (self.texture.get_width() - self.margin_padding[0] * 2 + self.padding[0]) // (self.cell_size[0] + self.padding[0])
    
    def get_grid_height(self) -> int:
        """Returns the amount of cells in one column"""
        return (self.texture.get_height() - self.margin_padding[1] * 2 + self.padding[0]) // (self.cell_size[1] + self.padding[1])
    
    def get_grid_size(self) -> tuple[int, int]:
        return (self.get_grid_width(), self.get_grid_height())
    
    def get_num_cells(self) -> int:
        """Returns the maximum number of cells"""
        return self.get_grid_width() * self.get_grid_height()
    
    def get_rect(self, cell_pos: tuple[int, int] | int) -> Rect:
        if isinstance(cell_pos, int):
            if cell_pos >= self.get_num_cells():
                raise ValueError("Cell index outside of bounds")
            return Rect(
                self.margin_padding[0] + (self.cell_size[0] + self.padding[0]) * (cell_pos % self.get_grid_width()),
                self.margin_padding[1] + (self.cell_size[1] + self.padding[1]) * (cell_pos // self.get_grid_width()),
                self.cell_size[0],
                self.cell_size[1]
            )
        else:
            if cell_pos[0] >= self.get_grid_width() or cell_pos[1] >= self.get_grid_height():
                raise ValueError("Cell index outside of bounds")
            return Rect(
                self.margin_padding[0] + (self.cell_size[0] + self.padding[0]) * cell_pos[0],
                self.margin_padding[1] + (self.cell_size[1] + self.padding[1]) * cell_pos[1],
                self.cell_size[0],
                self.cell_size[1]
            )


class TileSheet(SpriteSheet):
    """A SpriteSheet with optional str named rect values"""
    def __init__(self,
                file_path: str,
                cell_size: tuple[int, int],
                padding: tuple[int, int] = (0, 0),
                margin_padding: tuple[int, int] = (0, 0),
                tile_names: list[str] = []):
        super().__init__(file_path, cell_size, padding, margin_padding)
        
        self.tile_LUT = dict[str, tuple[int, int] | int]((
            (tile_names[pos], pos) 
            for pos in range(min(self.get_num_cells(), len(tile_names)))
            ))
    
    def __getitem__(self, cell_pos: tuple[int, int] | int | str) -> Rect:
        return self.get_rect(cell_pos)
    
    def get_rect(self, cell_pos: tuple[int, int] | int | str) -> Rect:
        if isinstance(cell_pos, str):
            return self.get_rect_by_name(cell_pos)
        else:
            return super().get_rect(cell_pos)
    
    def register_tile(self, name: str, position: tuple[int, int] | int):
        self.tile_LUT[name] = position
    
    def register_tiles(self, *name_position_pairs: tuple[str, tuple[int, int] | int]):
        for pair in name_position_pairs:
            self.register_tile(pair[0], pair[1])
    
    def get_rect_by_name(self, name) -> Rect:
        if name not in self.tile_LUT:
            raise KeyError(f"No tile was with name '{name}'")
        return super().get_rect(self.tile_LUT[name])
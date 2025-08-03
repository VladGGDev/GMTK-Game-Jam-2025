import engine, engine.collider

class ScoreManager(engine.Actor):
    def __init__(self) -> None :
        super().__init__()
        self.score: int = 0
        self.total_distance: float = 0
        self.drift_distance: float = 0
        self.total_loops: int = 0
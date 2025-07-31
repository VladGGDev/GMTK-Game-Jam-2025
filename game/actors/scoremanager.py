import engine, engine.collider

class ScoreManager(engine.Actor):
    def __init__(self) -> None :
        self.score : int = 0

    def add_points(self, points : int) -> None :
        self.score += points

    def reset_score(self ) -> None:
        self.score = 0

    def get_score(self) -> int:
        return self.score
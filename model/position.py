from typing import Dict, Tuple

class Position:
    def from_dict(self, pos_dict: Dict):
        self.x = pos_dict['x']
        self.y = pos_dict['y']
        return self

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def getpos(self, x, y) -> Tuple[int, int]:
        return x, y

    def __eq__(self, o: object) -> bool:
        if object is None:
            return False
        if type(object) != type(self):
            return False
        return (self.x, self.y) == object.getpos()

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __repr__(self) -> str:
        return self.__str__()

    def __sub__(self, o: object) -> 'Position':
        if not isinstance(o, Position):
            raise TypeError('Can\'t subtract these types')
        return Position(self.x - o.x, self.y - o.y)

    def __add__(self, o: object) -> 'Position':
        if not isinstance(o, Position):
            raise TypeError('Can\'t add these types')
        return Position(self.x + o.x, self.y + o.y)

    def engine_str(self) -> str:
        return f"{self.x} {self.y}"

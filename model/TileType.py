from enum import Enum

class TileType:
    GREEN_GROCER = 1
    GRASS = 2
    ARID = 3
    SOIL = 4
    F_BAND_OUTER = 5
    F_BAND_MID = 6
    F_BAND_INNER = 7

    def __str__(self) -> str:
        return f"{self.name}"

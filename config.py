from model.position import Position
from model.item_type import ItemType
from model.upgrade_type import UpgradeType

class Config:
    START_ITEM = ItemType.COFFEE_THERMOS
    START_UPGRADE = UpgradeType.BACKPACK
    MOVES_TO_GREEN_GROCER = 1 if START_UPGRADE == UpgradeType.LONGER_LEGS else 2
    INITIAL_POTATO_COUNT = 20
    GROCER_POSITION = Position(15, 0)

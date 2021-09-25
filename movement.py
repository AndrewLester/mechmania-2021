
from model.tile_type import TileType
from model.game_state import GameState
from api.game_util import distance
from model.position import Position
from api.constants import Constants
from model.decisions.move_decision import MoveDecision
from model.player import Player
from random import randint
import math

constants = Constants()


def move_randomly(player: Player, y: bool = True) -> MoveDecision:
    return move_relative(player, randint(-10, 10), randint(-10, 10) if y else 0)


def move_to_grocer(player: Player) -> MoveDecision:
    green_grocer_x = constants.BOARD_WIDTH // 2
    green_grocer_y = 0

    return move_relative(player, green_grocer_x - player.position.x, green_grocer_y - player.position.y)


def move_relative(player: Player, x_diff: int, y_diff: int) -> MoveDecision:
    if x_diff > constants.MAX_MOVEMENT:
        x_diff = constants.MAX_MOVEMENT
    elif x_diff < -constants.MAX_MOVEMENT:
        x_diff = -constants.MAX_MOVEMENT

    if y_diff > constants.MAX_MOVEMENT:
        y_diff = constants.MAX_MOVEMENT
    elif y_diff < -constants.MAX_MOVEMENT:
        y_diff = -constants.MAX_MOVEMENT

    distance = abs(x_diff) + abs(y_diff)
    if distance > 10:
        if abs(x_diff) > abs(y_diff):
            x_diff = int(math.copysign(10 - abs(y_diff), x_diff))
        else:
            y_diff = int(math.copysign(10 - abs(x_diff), y_diff))

    new_x = player.position.x + x_diff
    new_y = player.position.y + y_diff

    new_x = min(constants.BOARD_WIDTH - 1, max(0, new_x))
    new_y = min(constants.BOARD_HEIGHT - 1, max(0, new_y))

    return MoveDecision(Position(new_x, new_y))


def get_turns_to_position(origin: Position, destination: Position) -> int:
    return distance(origin, destination) // constants.MAX_MOVEMENT


def at_green_grocer(game_state: GameState, position: Position) -> bool:
    return game_state.tile_map.get_tile(position.x, position.y).type == TileType.GREEN_GROCER

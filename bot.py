from model.crop_type import CropType
from model.crop import Crop
from model.decisions.harvest_decision import HarvestDecision
from api import game_util
from functools import reduce
from math import ceil
from model.decisions.move_decision import MoveDecision
from typing import Callable, List, Optional

from api.constants import Constants
from config import Config
from game import Game
from model.decisions.turn_decision import TurnDecision, TurnDecisionGenerator, TurnDecisionOverride
from model.game_state import GameState
from model.position import Position
from model.tile_type import TileType
from movement import move_randomly
from networking.io import Logger
from turns import turn_decisions

logger = Logger()
constants = Constants()


class Bot:
    decision_index: float = 0

    def __init__(self, turn_decisions: List[TurnDecisionGenerator], decision_overrides: List[TurnDecisionOverride]) -> None:
        self.turn_decisions = turn_decisions
        self.decisions_length = reduce(
            lambda d1, d2: d1 + d2.times, turn_decisions, 0)
        self.decision_overrides = decision_overrides

    def make_decision(self, state: GameState, increment_decision: bool=False) -> TurnDecision:
        if state.feedback:
            logger.debug(f'Received feedback: {state.feedback}')
        for override in self.decision_overrides:
            turn_decision = override(state)
            if turn_decision is not None:
                return turn_decision.get_turn_decision(state)

        if self.decision_index < len(self.turn_decisions):
            logger.debug(f'Making decision with index: {self.decision_index}')
            turn_decision_generator = self.turn_decisions[int(
                self.decision_index)]

            if increment_decision:
                turn_decision_generator.update_status(state)
                if hasattr(turn_decision_generator, 'is_finished') and turn_decision_generator.is_finished is not None:
                    logger.debug(f'Turn decision times: {turn_decision_generator.times}, is finished: {turn_decision_generator.is_finished(state)}')
                turn_decision = turn_decision_generator.get_turn_decision(state)
                times = turn_decision.times
                if times > 0:
                    logger.debug(f'Incrementing decision by {1 / times}')
                    self.decision_index += 1 / times
                    if abs(ceil(self.decision_index) - self.decision_index) < 0.001:
                        self.decision_index = round(self.decision_index)
            else:
                turn_decision = turn_decision_generator.get_turn_decision(state)
        else:
            player = state.get_my_player()
            turn_decision = TurnDecision(
                move_decision=move_randomly(player),
            )

        return turn_decision

def harvest_grown_crops(state: GameState) -> Optional[TurnDecision]:
    if state.turn < 50:
        return None

    player = state.get_my_player()
    positions = game_util.within_move_range(state, player.name)
    for position in positions:
        if state.tile_map.get_tile(position.x, position.y).crop != CropType.NONE and \
            state.tile_map.get_tile(position.x, position.y).turns_left_to_grow == 0:
            harvest_positions = game_util.within_harvest_range(state, position)
            return TurnDecision(
                move_decision=MoveDecision(position),
                action_decision=HarvestDecision(harvest_positions)
            )

def main():
    """
    Competitor TODO: choose an item and upgrade for your bot
    """
    game = Game(Config.START_ITEM, Config.START_UPGRADE)
    bot = Bot(turn_decisions, [harvest_grown_crops])

    while (True):
        try:
            game.update_game()
        except IOError:
            exit(-1)
        move_decision = bot.make_decision(game.game_state).move_decision
        logger.debug(f'Sending move decision: {move_decision}')
        game.send_move_decision(move_decision)

        try:
            game.update_game()
        except IOError:
            exit(-1)
        action_decision = bot.make_decision(
            game.game_state, increment_decision=True).action_decision
        logger.debug(f'Sending action decision: {action_decision}')
        game.send_action_decision(action_decision)


if __name__ == "__main__":
    main()

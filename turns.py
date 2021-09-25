from purchase import buy_up_to
from model.decisions.do_nothing_decision import DoNothingDecision
from model.decisions.buy_decision import BuyDecision
from config import Config
from model.crop_type import CropType
from planting import harvest_nearby, plant_cross, plant_row
from model.position import Position
from typing import List
from model.decisions.turn_decision import TurnDecision, TurnDecisionGenerator
from movement import at_green_grocer, get_turns_to_position, move_randomly, move_relative, move_to_grocer
from model.decisions.move_decision import MoveDecision
from random import randint


turn_decisions: List[TurnDecisionGenerator] = [
    TurnDecisionGenerator(
        get_move_decision=lambda state: move_to_grocer(state.get_my_player()),
        get_action_decision=lambda _: BuyDecision(
            [CropType.POTATO, CropType.QUADROTRITICALE], [20, 3]),
        times=Config.MOVES_TO_GREEN_GROCER
    ),
    TurnDecision(
        move_decision=MoveDecision(Position(15, 7)),
    ),
    TurnDecisionGenerator(
        get_move_decision=lambda state: move_randomly(
            state.get_my_player(), y=False),
        get_action_decision=lambda state: plant_cross(state, CropType.POTATO)
    ),
    TurnDecisionGenerator(
        get_move_decision=lambda state: move_relative(
            state.get_my_player(), 3, 0),
        get_action_decision=lambda state: plant_cross(state, CropType.POTATO),
        times=3
    ),
    TurnDecisionGenerator(
        get_move_decision=lambda state: move_relative(
            state.get_my_player(), -9, 0),
        get_action_decision=lambda state: harvest_nearby(state)
    ),
    TurnDecisionGenerator(
        get_move_decision=lambda state: move_relative(
            state.get_my_player(), 3, 0),
        get_action_decision=lambda state: harvest_nearby(state),
        times=3
    ),
    TurnDecisionGenerator(
        get_move_decision=lambda state: move_relative(
            state.get_my_player(), 15 - state.get_my_player().position.x, 3 - state.get_my_player().position.y),
        get_action_decision=lambda state: plant_row(
            state, CropType.QUADROTRITICALE)
    ),
    TurnDecisionGenerator(
        get_move_decision=lambda state: move_to_grocer(state.get_my_player()),
        get_action_decision=lambda state: buy_up_to(state, CropType.JOGAN_FRUIT, 10),
        is_finished=lambda state: at_green_grocer(
            state, state.get_my_player().position)
    ),
    TurnDecisionGenerator(
        get_move_decision=lambda state: move_relative(
            state.get_my_player(), randint(-3, 3), 4),
        get_action_decision=lambda state: plant_cross(
            state, CropType.JOGAN_FRUIT),
        is_finished=lambda state: state.get_my_player().seed_inventory.get(CropType.JOGAN_FRUIT, 0) == 0
    ),
]

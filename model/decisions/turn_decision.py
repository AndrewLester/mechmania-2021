from model.decisions.do_nothing_decision import DoNothingDecision
from dataclasses import dataclass
from game import Game
from model.game_state import GameState
from model.decisions.plant_decision import PlantDecision
from model.position import Position
from typing import Callable, Optional, cast
from .move_decision import MoveDecision
from .action_decision import ActionDecision

TurnDecisionOverride = Callable[[GameState], Optional['TurnDecisionGenerator']]
MoveDecisionGenerator = Callable[[GameState], MoveDecision]
ActionDecisionGenerator = Callable[[GameState], ActionDecision]

class TurnDecisionGenerator:
    get_move_decision: MoveDecisionGenerator
    get_action_decision: ActionDecisionGenerator
    _times: int
    is_finished: Optional[Callable[[GameState], bool]] = None
    _finished: bool = False

    def __init__(self, get_move_decision: Optional[MoveDecisionGenerator] = None, get_action_decision: Optional[ActionDecisionGenerator] = None, times: int = 1, is_finished: Optional[Callable[[GameState], bool]] = None) -> None:
        if get_move_decision is None:
                get_move_decision = lambda state: MoveDecision(Position(state.get_my_player().position.x, state.get_my_player().position.y))

        if get_action_decision is None:
            get_action_decision = lambda _: DoNothingDecision()

        self.get_move_decision = get_move_decision
        self.get_action_decision = get_action_decision
        self._times = times
        self.is_finished = is_finished

    def update_status(self, state: GameState) -> None:
        if self.is_finished is not None:
            self._finished = self.is_finished(state)

    @property
    def times(self) -> float:
        if self.is_finished is not None:
            return 1 if self._finished else 0
        return self._times

    def get_turn_decision(self, state: GameState) -> 'TurnDecision':
        player = state.get_my_player()
        return TurnDecision(
            move_decision=self.get_move_decision(state) if self.get_move_decision is not None else MoveDecision(player.position),
            action_decision=self.get_action_decision(state) if self.get_action_decision else DoNothingDecision(),
            times=int(self.times)
        )

@dataclass(init=False)
class TurnDecision(TurnDecisionGenerator):
    move_decision: MoveDecision
    action_decision: ActionDecision

    def __init__(self, move_decision: MoveDecision, action_decision: Optional[ActionDecision] = None, times: int = 1) -> None:
        self.move_decision = move_decision
        self.action_decision = action_decision or DoNothingDecision()

        self.get_move_decision = lambda _: self.move_decision
        self.get_action_decision = lambda _: self.action_decision
        self._times = times

    @property
    def times(self) -> float:
        return self._times

from model.decisions.action_decision import ActionDecision
from model.decisions.do_nothing_decision import DoNothingDecision
from model.position import Position
from random import seed
from networking.io import Logger
from model.game_state import GameState
from model.crop_type import CropType
from model.player import Player
from model.decisions.plant_decision import PlantDecision
from model.decisions.harvest_decision import HarvestDecision
from api import game_util

logger = Logger()


def plant_cross(state: GameState, crop: CropType) -> ActionDecision:
    player = state.get_my_player()
    seed_inventory = player.seed_inventory
    seed_count = seed_inventory.get(crop, 0)
    positions = game_util.within_harvest_range(state, player.name)
    if seed_count < len(positions):
        logger.warn('not enough seeds for positions')
    logger.debug(f'PLANTING POSITIONS: {positions}, SEED COUNT: {seed_count}')
    positions = positions[:min(seed_count, len(positions))]
    logger.debug(f'Plant decision: {[crop] * len(positions)}, {positions}')
    if len(positions) < 1:
        return DoNothingDecision()
    return PlantDecision([crop] * len(positions), positions)


def plant_row(state: GameState, crop: CropType) -> ActionDecision:
    player = state.get_my_player()
    seed_inventory = player.seed_inventory
    seed_count = seed_inventory.get(crop, 0)
    positions = [
        Position(0, 0),
        Position(-1, 0),
        Position(1, 0),
    ]
    positions = [player.position + position for position in positions]
    logger.debug(f'Pos: {positions}')
    if seed_count < len(positions):
        logger.warn('not enough seeds for positions')
    logger.debug(f'PLANTING POSITIONS: {positions}, SEED COUNT: {seed_count}')
    positions = positions[:min(seed_count, len(positions))]
    logger.debug(f'Plant decision: {[crop] * len(positions)}, {positions}')
    if len(positions) < 1:
        return DoNothingDecision()
    return PlantDecision([crop] * len(positions), positions)


def harvest_nearby(state: GameState) -> HarvestDecision:
    player = state.get_my_player()
    positions = game_util.within_harvest_range(state, player.name)
    logger.debug(f'HARVESTING POSITIONS: {positions}')
    return HarvestDecision(positions)

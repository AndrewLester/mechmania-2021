from model.decisions.buy_decision import BuyDecision
from model.crop_type import CropType
from model.game_state import GameState

def buy_up_to(state: GameState, crop: CropType, max_quantity: int) -> BuyDecision:
    player = state.get_my_player()
    quantity = min(player.money / crop.get_seed_price(), max_quantity)
    return BuyDecision([crop], [quantity])

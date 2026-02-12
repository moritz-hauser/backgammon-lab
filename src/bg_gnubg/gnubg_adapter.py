import base64
import logging
from typing import TypeAlias
from bg_game.game_types import (
    AgentPerspectiveState,
    Action,
    Dice,
    BAR, OFF,
)

log = logging.getLogger(__name__) 

BoardPosition: TypeAlias = tuple[int, ...]  # 25 ints for each player
GnubgBoard: TypeAlias = tuple[BoardPosition, BoardPosition]
GnubgMove: TypeAlias = tuple[tuple[int,int], ...]

POS_KEY_LEN = 80    # Position Key is expected to be 80bits
POS_ID_LEN = 14     # Position ID is expected to be 14chars

GNUBG_BAR = 25  # Encodings of bar and off on the board
GNUBG_OFF = 0

_gnubg = None

def _require_gnubg():
    global _gnubg
    if _gnubg is None:
        try:
            import gnubg
            _gnubg = gnubg
        except ImportError as e:
            raise ImportError(
                "gnubg not installed. Install with: pip install -e '.[gnubg]'"
            ) from e
    return _gnubg

class GnuBgAdapter():

    @classmethod
    def _aps_to_position_key(cls, aps: AgentPerspectiveState) -> str:
        """
        Builds the 10 byte binary used by GNUBG to
        describe the state of the board from 
        an APS.
        https://www.gnu.org/software/gnubg/manual/html_node/A-technical-description-of-the-Position-ID.html
        """

        # For some reason GNUBG keeps playing as the enemy, 
        # so we must first flip the APS for it to work
        # (Probably error in my adapter here)
        aps_flip = AgentPerspectiveState.get_enemy_perspective(aps)
        
        pos_key = ''   

        # First, encode own points starting at ace point (=23):
        for amount_checkers in aps_flip.points[::-1]:
            if amount_checkers > 0:
                pos_key += '1' * amount_checkers
            pos_key += '0'
        # Then encode own bar
        pos_key += '1' * aps_flip.bar_me
        pos_key += '0'
        
        # Secondly, encode enemy points starting at his ace point (=0):
        for amount_checkers in aps_flip.points:
            if amount_checkers < 0:
                pos_key += '1' * abs(amount_checkers)
            pos_key += '0'
        # Then encode enemy bar
        pos_key += '1' * aps_flip.bar_enemy
        pos_key += '0'

        # Pad out to 80 bits with 0s
        amount_zeros = POS_KEY_LEN - len(pos_key)
        zeros = '0' * amount_zeros
        pos_key += zeros
        
        return pos_key

    @classmethod
    def _position_key_to_id(cls, pos_key: str) -> str:
        """
        Convert binary string to bytes (reading bits left-to-right, bytes in little-endian)
        GNUBG encodes bits LSB-first within each byte, and bytes in little-endian order.
        Base64 encode to ASCII.
        """
        key_bytes = bytearray()
        for i in range(0, 80, 8):
            byte_bits = pos_key[i:i+8]
            # Reverse bits within byte (LSB first)
            byte_bits_reversed = byte_bits[::-1]
            byte_value = int(byte_bits_reversed, 2)
            key_bytes.append(byte_value)
        
        # Base64 encode
        position_id = base64.b64encode(bytes(key_bytes)).decode('ascii').rstrip('=')
        return position_id

    @classmethod
    def _board_from_position_id(cls, pos_id: str) -> GnubgBoard:
        gnubg = _require_gnubg()
        # Method name is wrong, actually takes id!
        # = ASCII string insted of bytes
        return gnubg.board_from_position_key(pos_id)


    @classmethod
    def _gnubg_mv_to_action(cls, move: GnubgMove) -> Action:
        return tuple(
            (BAR if frm == GNUBG_BAR else 24 - frm, OFF if to == GNUBG_OFF else 24 - to)
            for frm, to in move
        )

    @classmethod
    def _gnubg_board_from_aps(cls, aps: AgentPerspectiveState) -> GnubgBoard:
        """
        Experimental:
        Builds GnubgBoard directly from aps without
        generating id or key in between.
        """
        # Replace signed entries with 0; reverse: go from 23->0
        my_pos: list[int] = [0 if p < 0 else p for p in aps.points][::-1] + [aps.bar_me]
        
        # Replace unsigned entries with 0
        enem_pos: list[int] = [0 if p > 0 else abs(p) for p in aps.points] + [aps.bar_enemy]

        #return (tuple(my_pos), tuple(enem_pos))

        # enem first, mine second
        return (tuple(enem_pos), tuple(my_pos))
    
    @DeprecationWarning
    def best_action_from_aps_old(self, aps: AgentPerspectiveState, dice: Dice, ply: int = 1) -> Action:
        """
        Uses the GNUBG-NN to calculate to optimal action in 
        a certain state.
        """
        gnubg = _require_gnubg()

        pos_key: str = GnuBgAdapter._aps_to_position_key(aps)
        log.info(f"Position Key calculated: {pos_key}")
        assert len(pos_key) == POS_KEY_LEN

        pos_id: str = GnuBgAdapter._position_key_to_id(pos_key) 
        log.info(f"Position Id calculated: {pos_id}")
        assert len(pos_id) == POS_ID_LEN
        
        board: GnubgBoard = GnuBgAdapter._board_from_position_id(pos_id)
        log.info(f"Build GnubgBoard: {board}")

        # Experimental
        board2: GnubgBoard = GnuBgAdapter._gnubg_board_from_aps(aps)
        log.info(f"(Directly from aps: {board})")

        move: GnubgMove = gnubg.best_move(board, dice[0], dice[1], ply)
        log.info(f"Determined best GnubgMove: {move}")

        action: Action = GnuBgAdapter._gnubg_mv_to_action(move)
        log.info(f"Converted to action: {action}")
        return action
    
    @classmethod
    def best_action_from_aps(cls, aps: AgentPerspectiveState, dice: Dice, ply: int = 1) -> Action:
        """
        Uses the GNUBG-NN to calculate to optimal action in 
        a certain state.
        """
        gnubg = _require_gnubg()
        
        log.info(f"Received aps: {aps}")

        board: GnubgBoard = GnuBgAdapter._gnubg_board_from_aps(aps)
        log.info(f"Built from aps: {board}")

        move: GnubgMove = gnubg.best_move(board, dice[0], dice[1], ply)
        log.info(f"Determined best GnubgMove: {move}")

        action: Action = GnuBgAdapter._gnubg_mv_to_action(move)
        log.info(f"Converted to aps-action: {action}")
        return action

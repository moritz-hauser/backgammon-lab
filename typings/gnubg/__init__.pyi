# Type stubs for gnubg module

from typing import Tuple

BoardPosition = Tuple[int, ...]  # 25 ints for each player
GnubgBoard = Tuple[BoardPosition, BoardPosition]
GnubgMove = Tuple[Tuple[int, int], ...]

def board_from_position_key(pos_id: str) -> GnubgBoard:
    """
    Convert position ID to board representation.
    
    Args:
        pos_id: Base64-encoded position identifier (14 chars)
    
    Returns:
        Tuple of (enemy_position, my_position) where each position 
        is a tuple of 25 integers representing checker counts
    """
    ...

def best_move(
    board: GnubgBoard,
    die1: int,
    die2: int,
    ply: int = 1
) -> GnubgMove:
    """
    Calculate best move using GNUBG neural network.
    
    Args:
        board: Board state as (enemy_pos, my_pos)
        die1: First die value (1-6)
        die2: Second die value (1-6)
        ply: Search depth/ply level (default: 1)
    
    Returns:
        Tuple of (from, to) moves representing the best action
    """
    ...
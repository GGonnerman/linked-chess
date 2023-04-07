from model.pieces.chess_piece import ChessPiece
from color import Color
from model.pieces.movement import add_selected


class Knight(ChessPiece):
    def __init__(self, color, row, column):
        super().__init__("Knight", color, row, column)

    def get_potential_moves(self, gameboard):
        return add_selected(self, gameboard,
            [2, 1],
            [1, 2],
            [-1, 2],
            [-2, 1],
            [-2, -1],
            [-1, -2],
            [1, -2],
            [2, -1],
        )

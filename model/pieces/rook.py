from model.pieces.movement import add_until_end
from model.pieces.chess_piece import ChessPiece

class Rook(ChessPiece):
	def __init__(self, color, row, column):
		super().__init__("Rook", color, row, column)

	def get_potential_moves(self, gameboard):
		return add_until_end(self, gameboard, [0, 1], [0, -1], [1, 0], [-1, 0])


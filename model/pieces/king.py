from model.pieces.movement import add_selected
from model.pieces.chess_piece import ChessPiece

class King(ChessPiece):
	def __init__(self, color, row, column):
		super().__init__("King", color, row, column)


	def get_potential_moves(self, gameboard):
		return add_selected(self, gameboard, [1, 1], [-1, -1], [1, -1], [-1, 1], [0, 1], [0, -1], [1, 0], [-1, 0])
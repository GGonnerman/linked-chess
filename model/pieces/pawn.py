from model.pieces.chess_piece import ChessPiece
from model.pieces.movement import add_selected
from color import Color

class Pawn(ChessPiece):
	def __init__(self, color, row, column):
		super().__init__("Pawn", color, row, column)
	
	def get_potential_moves(self, gameboard):
		potential_moves = []

		direction = 1 if self.color == Color.BLACK else -1
		potential_moves += add_selected(self, gameboard, [direction, 0])

		if(self.row == 1 and self.color == Color.BLACK) or (self.row == 6 and self.color == Color.WHITE):
			potential_moves += add_selected(self, gameboard, [direction*2, 0])
		
		# TODO: En-passant
		# TODO: Capturing on diagonals

		return potential_moves


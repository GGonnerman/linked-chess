from model.pieces.chess_piece import ChessPiece
from model.pieces.movement import add_selected
from color import Color

class Pawn(ChessPiece):
	def __init__(self, color, row, column):
		super().__init__("Pawn", color, row, column)
	
	def get_potential_moves(self, gameboard):
		potential_moves = []

		direction = 1 if self.color == Color.BLACK else -1
		if gameboard.get_piece(direction + self.row, self.column) == None:
			potential_moves += add_selected(self, gameboard, [direction, 0])

		if(self.row == 1 and self.color == Color.BLACK) or (self.row == 6 and self.color == Color.WHITE):
			if gameboard.get_piece(direction*2 + self.row, self.column) == None:
				potential_moves += add_selected(self, gameboard, [direction*2, 0])

		potential_moves += self.check_attacking_position(gameboard, [direction, -1], [direction, 1])

		# TODO: En-passant

		return potential_moves

	def check_attacking_position(self, gameboard, *changes):
		potential_moves = []
		for change in changes:
			row = self.row
			column = self.column
			row += change[0]
			column += change[1]
			selected_piece = gameboard.get_piece(row, column)
			if selected_piece != None and selected_piece.color != self.color:
				potential_moves.append([row, column])

		return potential_moves

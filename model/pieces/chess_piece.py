from abc import ABC, abstractmethod
from model.util import coordinate_to_algebraic
from color import Color

class ChessPiece(ABC):
    def __init__(self, name, color, row, column):
        self.name = name
        self.color = color
        self.row = row
        self.column = column

        # Setup the code for the FEN
        self.code = name[0]
        if name == "Knight": self.code = "N"

        if self.color == Color.WHITE:
            self.code = self.code.upper()
        else:
            self.code = self.code.lower()
    
    def get_location(self):
        return [self.row, self.column]

    def __str__(self):
        return f"{self.color} {self.name}: {coordinate_to_algebraic([self.row, self.column])}"

    def get_legal_moves(self, gameboard):
        legal_moves = []
        potential_moves = self.get_potential_moves(gameboard)

        for ending_location in potential_moves:
            new_gameboard = gameboard.copy()
            new_gameboard.attempt_move([self.row, self.column], ending_location)
            active_king_location = None
            for row in new_gameboard.piece_list:
                for piece in row:
                    if piece == None or piece.color != self.color: continue
                    if piece.code.lower() == "k":
                        active_king_location = [piece.row, piece.column]

            # If I dont have a king, I cant move anywhere 
            if active_king_location == None: return []
                
            is_legal_move = True
            for row in new_gameboard.piece_list:
                for piece in row:
                    print(piece)
                    if piece == None or piece.color == self.color: continue
                    their_potential_moves = piece.get_potential_moves(new_gameboard)
                    if active_king_location in their_potential_moves:
                        is_legal_move = False
                        break
            if is_legal_move: legal_moves.append(ending_location)

        return legal_moves


    #@abstractmethod
    #def get_potential_moves(self):
    #    pass

    #@abstractmethod
    #def get_legal_moves(self):
    #    pass
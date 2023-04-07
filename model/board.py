from model.pieces.chess_piece import ChessPiece
from model.util import coordinate_to_algebraic, algebraic_to_coordinate
from color import Color
from model.pieces.pawn import Pawn
from model.pieces.bishop import Bishop
from model.pieces.knight import Knight
from model.pieces.rook import Rook
from model.pieces.queen import Queen
from model.pieces.king import King

class Board():
    def __init__(self):
        self.piece_list = [[None for column in range(8)] for row in range(8)]

        self.active_color = Color.WHITE
        self.castling_availability = ["KQ", "kq"]
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
    
    def copy(self):
        new_board = Board()
        current_FEN = self.generate_FEN()
        new_board.setup(current_FEN)
        return new_board
    
    def is_valid_location(self, row, column):
        if row < 0 or row >= 8 or column < 0 or column >= 8:
            return False
        return True
    
    def get_pieces(self, color=None):
        pieces = []
        for row in self.piece_list:
            for piece in row:
                if piece == None: continue
                if color == Color.WHITE:
                    if piece.color == Color.WHITE: pieces.append(piece)
                elif color == Color.BLACK:
                    if piece.color == Color.BLACK: pieces.append(piece)
                else:
                    pieces.append(piece)
        return pieces

    def get_piece(self, row, column):
        if not self.is_valid_location(row, column): return None
        return self.piece_list[row][column]

    def set_piece(self, new_piece, row, column):
        if not self.is_valid_location(row, column):
            raise IndexError(f"[{row}, {column}] is not within the bounds of the board")
        self.piece_list[row][column] = new_piece

    def is_valid_move(self, starting_location, ending_location):
        # Get the specified piece and its potential moves
        piece_to_move = self.get_piece(*starting_location)
        if piece_to_move == None: return False
        possible_moves = piece_to_move.get_potential_moves(self)
        # Check if any of those moves match the ending_location
        for possible_move in possible_moves:
            if possible_move[0] == ending_location[0] and possible_move[1] == ending_location[1]:
                return True

        return False

    def attempt_move(self, starting_location, ending_location):
        # Ensure it is a valid move
        if not self.is_valid_move(starting_location, ending_location):
            raise Exception("Invalid move")

        self.move(starting_location, ending_location)

        return True
    
    def get_king_location(self, color):
        for row in self.piece_list:
            for piece in row:
                if piece == None or piece.color != color: continue
                if piece.code.lower() == "k":
                    return [piece.row, piece.column]
        return None

    def move(self, starting_location, ending_location):
        # Increment the fullmove counter after black's turn
        if self.active_color == Color.BLACK:
            self.fullmove_number += 1

        piece_to_move = self.get_piece(*starting_location)

        # Check for en-passent possibility
        if isinstance(piece_to_move, Pawn) and (abs(starting_location[0] - ending_location[0]) == 2):
            delta = starting_location[0] - ending_location[0]
            # Adding half delta will move it in the correct direction
            self.en_passant_target = [starting_location[0] + 0.5 * delta, starting_location[1]]
        
        # Empty the halfmove clock if either a pawn move or a capturing move
        # Otherwise, add 1 to it
        # Used for the fifty-move rule
        if isinstance(piece_to_move, Pawn):
            self.halfmove_clock = 0
        elif isinstance(self.get_piece(*ending_location), ChessPiece):
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
        
        # Switch the active color
        self.active_color = Color.BLACK if self.active_color == Color.WHITE else Color.WHITE
        
        # Update the piece's internal location
        piece_to_move.row = ending_location[0]
        piece_to_move.column = ending_location[1]

        # Move the piece to the new location and empty the pieces old location 
        self.set_piece(piece_to_move, *ending_location)
        self.set_piece(None, *starting_location)
    
    def generate_FEN(self):
        piece_placement_data = ""
        for row in range(len(self.piece_list)):
            sequential_empty_spaces = 0
            for column in range(len(self.piece_list[row])):
                piece = self.piece_list[row][column]
                if piece == None:
                    sequential_empty_spaces += 1
                else:
                    if sequential_empty_spaces > 0:
                        piece_placement_data += str(sequential_empty_spaces)
                        sequential_empty_spaces = 0
                    piece_placement_data += piece.code
            if sequential_empty_spaces > 0:
                piece_placement_data += str(sequential_empty_spaces)
            if row < len(self.piece_list) - 1: piece_placement_data += "/"
        processed_en_passant_target = "-" if self.en_passant_target == None else coordinate_to_algebraic(self.en_passant_target)
        return f"{piece_placement_data} {'w' if self.active_color == Color.WHITE else 'b'} {''.join(self.castling_availability)} {processed_en_passant_target} {self.halfmove_clock} {self.fullmove_number}"




    def __str__(self):
        output = "  "
        # Add the number above the board for columns
        for i in range(8):
            output += chr(97+i) + " "
        output += "\n"
        for row in range(len(self.piece_list)):
            # Add the number to the left the board for rows
            output += str(8 - row) + " "
            for column in range(len(self.piece_list)):
                if(piece := self.piece_list[row][column]):
                    output += piece.code
                else:
                    output += " "
                if column == len(self.piece_list) - 1: break
                output += " "
            output += "\n" if row < len(self.piece_list) - 1 else ""
        output += "\n  "
        for i in range(8):
            output += chr(97+i) + " "
        return output

    # rnbqkbnr/pppp1ppp/8/4p3/8/3P4/PPP1PPPP/RNBQKBNR w KQkq - 0 2
    def process_FEN(FEN):

        piece_map = {
            "r": Rook,
            "n": Knight,
            "b": Bishop,
            "q": Queen,
            "k": King,
            "p": Pawn,
        }

        raw_pl, raw_ac, raw_ca, raw_ept, raw_hc, raw_fn = FEN.split(" ")

        pl = raw_pl.split("/")

        piece_list = [[None for column in range(8)] for row in range(8)]

        row = 0
        column = 0
        for i in range(len(pl)):
            column = 0
            for j in range(len(pl[i])):
                active_piece = pl[i][j]
                # If it is a number (whitespace), add that many and skip
                if active_piece in "12345678":
                    column += int(active_piece)
                    continue
                # It must be a real piece
                piece_color = Color.WHITE if active_piece.isupper() else Color.BLACK

                piece_list[row][column] = piece_map[active_piece.lower()](piece_color, row, column)
                print(f"Setting up [{row}, {column}] with {piece_list[row][column]}")

                column += 1

            row += 1

        active_color = Color.WHITE if raw_ac.lower() == "w" else Color.BLACK

        ca_white = ''.join([c for c in raw_ca if c.isupper()])
        ca_black = ''.join([c for c in raw_ca if c.islower()])

        castling_availability = [ca_white, ca_black]

        en_passant_target = None if raw_ept == "-" else algebraic_to_coordinate(raw_ept)
        halfmove_clock = int(raw_hc)
        fullmove_number = int(raw_fn)

        return [piece_list, active_color, castling_availability, en_passant_target, halfmove_clock, fullmove_number]

    def setup(self, FEN=None):
        if FEN == None:
            for column in range(8):
                pass
                #self.piece_list[1][column] = Pawn(Color.BLACK, 1, column)
                #self.piece_list[6][column] = Pawn(Color.WHITE, 6, column)

            for column in [0, 7]:
                self.piece_list[0][column] = Rook(Color.BLACK, 0, column)
                self.piece_list[7][column] = Rook(Color.WHITE, 7, column)

            for column in [2, 5]:
                self.piece_list[0][column] = Bishop(Color.BLACK, 0, column)
                self.piece_list[7][column] = Bishop(Color.WHITE, 7, column)

            for column in [1, 6]:
                self.piece_list[0][column] = Knight(Color.BLACK, 0, column)
                self.piece_list[7][column] = Knight(Color.WHITE, 7, column)

            self.piece_list[0][3] = Queen(Color.BLACK, 0, 3)
            self.piece_list[7][3] = Queen(Color.WHITE, 7, 3)

            self.piece_list[0][4] = King(Color.BLACK, 0, 4)
            self.piece_list[7][4] = King(Color.WHITE, 7, 4)
        else:
            pl, ac, ca, ept, hc, fn = Board.process_FEN(FEN)
            self.piece_list = pl
            self.active_color = ac
            self.castling_availability = ca
            self.en_passant_target = ept
            self.halfmove_clock = hc
            self.fullmove_number = fn
            print(self)
from model.board import Board

class Game():
    def __init__(self):
        pass

    def __str__(self):
        return str(self.board)

    def start(self, FEN=None):
        self.board = Board()
        self.board.setup(FEN)

    def get_deletion_options(self, piece_type, color):
        options = []
        for row in self.board.piece_list:
            for item in row:
                if item == None: continue
                if not isinstance(item, piece_type): continue
                if item.color != color: continue
                options.append(item)
        return options
    
    def delete_piece(self, row, column):
        self.board.set_piece(None, row, column)
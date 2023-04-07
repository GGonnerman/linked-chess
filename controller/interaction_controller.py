from view.constants import BOX_LENGTH
from color import Color

class InteractionController():
    def __init__(self, model, view, controller):
        self.model = model
        self.view = view
        self.controller = controller
        self.selected_piece = None
        self.selected_ending_location = None
        self.view.bind_mouse_click(self.click_event)
        self.update()
        self.is_accepting_input = True
    
    def update(self):
        options = [[self.model.game_1.board, self.view.upper_boxes],
                   [self.model.game_2.board, self.view.lower_boxes]]
        for board, boxes in options:
            for row in range(len(board.piece_list)):
                for column in range(len(board.piece_list[row])):
                    current_piece = board.piece_list[row][column]
                    current_box = boxes[row][column]
                    current_box.clear_highlighting()
                    if current_piece == None:
                        # Remove the images for every cell that doesnt have a piece
                        current_box.clear_image()
                    else:
                        file_name = f"{current_piece.color.name.title()}_{current_piece.name}"
                        # If it still has a piece, but it is a new piece, update the image
                        if current_box.photo_image_name != file_name:
                            current_box.clear_image() # Delete the old piece
                            current_box.display_image(file_name) # Display the new one
        self.show_issues()
        self.show_selected()

    def process_click(self, event):
        # If on the lowerboard, offset the y value
        if self.model.active_name == "lower": event.y -= BOX_LENGTH * 9
        row = int(event.y / BOX_LENGTH)
        column = int(event.x / BOX_LENGTH)
        return row, column
    
    def click_event(self, event):
        # Uncomment this line to restrict movement until there
        #if not self.controller.connection.is_connected: return
        if not self.is_accepting_input: return
        row, column = self.process_click(event)
        print("Row: " + str(row) + " Column: " + str(column))
        clicked_piece = self.model.active_game.board.get_piece(row, column)
        print(f"Clicked Piece: {clicked_piece}")
        if clicked_piece != None: print(f"{clicked_piece.color} == {self.model.active_game.board.active_color} ?  {clicked_piece.color == self.model.active_game.board.active_color}")
        # If I click on a new one of my pieces, update the 'selected piece'
        if clicked_piece != None and clicked_piece.color == self.model.active_game.board.active_color:
            print("Updating the selected piece")
            self.selected_piece = clicked_piece
            self.highlight_possible_moves()
            return

        # This is now not one of my pieces that I clicked on

        # Move to the location I clicked on if I can
        if self.selected_piece != None and [row, column] in self.selected_piece.get_potential_moves(self.model.active_game.board):
            self.selected_ending_location = [row, column]
            print(f"You plan to move to [{row}, {column}]")
        
        print(f"Highlighting possible moves")
        # Highlighting possible moves
        self.highlight_possible_moves()

    def show_issues(self):
        active_game = self.model.active_game
        active_color = active_game.board.active_color
        inactive_color = Color.BLACK if active_color == Color.WHITE else Color.WHITE

        active_king_location = active_game.board.get_king_location(active_color)

        should_highlight_king = False

        for piece in active_game.board.get_pieces(inactive_color):
            if active_king_location in piece.get_potential_moves(active_game.board):
                should_highlight_king = True
                break
        
        if should_highlight_king:
            if self.model.active_name == "upper":
                boxes = self.view.upper_boxes
            else:
                boxes = self.view.lower_boxes
            boxes[active_king_location[0]][active_king_location[1]].issue()
    
    def show_selected(self):
        if self.selected_piece == None: return
        if self.model.active_name == "upper":
            boxes = self.view.upper_boxes
        else:
            boxes = self.view.lower_boxes
        boxes[self.selected_piece.row][self.selected_piece.column].select()

    def highlight_possible_moves(self):
        self.update()
        print("Checking if none selected")
        if self.selected_piece == None: return
        print(f"Highlighting possible moves for {self.selected_piece}; code: {self.selected_piece.code.lower()}")
        if self.selected_piece.code.lower() == "k":
            for row, column in self.model.active_game.board.get_piece(self.selected_piece.row, self.selected_piece.column).get_legal_moves(self.model.active_game.board):
                if self.model.active_name == "upper":
                    boxes = self.view.upper_boxes
                else:
                    boxes = self.view.lower_boxes
                boxes[row][column].highlight()
        else:
            for row, column in self.model.active_game.board.get_piece(self.selected_piece.row, self.selected_piece.column).get_legal_moves(self.model.active_game.board):
                if self.model.active_name == "upper":
                    boxes = self.view.upper_boxes
                else:
                    boxes = self.view.lower_boxes
                boxes[row][column].highlight()
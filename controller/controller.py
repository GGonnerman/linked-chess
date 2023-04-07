from model.util import wait_until
from view.constants import BOX_LENGTH
from controller.interaction_controller import InteractionController
from model.connection import Connection

class Controller():
    def __init__(self, model, view):
        self.interaction_controller = InteractionController(model, view, self)
        self.model = model
        self.view = view
        print("Starting controller")
        self.connection = Connection()
        self.connection.connect()
    
    def gameplay_loop(self):
        # TODO: Increase the timeout massively
        set_number = 0
        while(True):
            if set_number % 2 == 0:
                self.model.active_game = self.model.game_1
                self.model.active_name = "upper"
                self.model.inactive_game = self.model.game_2
                self.model.inactive_name = "lower"
            else:
                self.model.active_game = self.model.game_2
                self.model.active_name = "lower"
                self.model.inactive_game = self.model.game_1
                self.model.inactive_name = "upper"

            self.interaction_controller.update()

            self.interaction_controller.is_accepting_input = True

            if self.model.active_name == "upper":
                self.view.canvas.configure(background='white')
            else:
                self.view.canvas.configure(background='black')

            print("Waiting for planned move")

            wait_until(self.has_planned_move, 900)
            piece_to_move_1, selected_ending_location_1 = self.get_planned_move()

            active_color_before_move_1 = self.model.active_game.board.active_color
            active_color_before_move_2 = self.model.inactive_game.board.active_color

            print("Got planned move. About to send socket")

            print(f"Sending: {piece_to_move_1}, {selected_ending_location_1}")

            # Process my move first
            captured_piece_1 = self.model.active_game.board.get_piece(*selected_ending_location_1)
            self.model.active_game.board.attempt_move(piece_to_move_1, selected_ending_location_1)

            self.interaction_controller.is_accepting_input = False

            self.interaction_controller.update()

            # Then send my move over
            self.connection.send_socket({
                "piece_to_move": piece_to_move_1,
                "selected_ending_location": selected_ending_location_1,
            })

            print("Sent socket. About to get socket")

            # Then get their move
            in_data = self.connection.get_socket()
            piece_to_move_2 = in_data["piece_to_move"]
            selected_ending_location_2 = in_data["selected_ending_location"]

            print(f"Received: {piece_to_move_2}, {selected_ending_location_2}")

            print("Got socket. About to send captures")

            # Then process their move
            captured_piece_2 = self.model.inactive_game.board.get_piece(*selected_ending_location_2)
            self.model.inactive_game.board.attempt_move(piece_to_move_2, selected_ending_location_2)

            self.interaction_controller.update()

            if captured_piece_2 != None:
                # Prompt for the piece to delete, and delete it
                print(f"You have to delete a piece in your {self.model.active_name} game, {active_color_before_move_1.name.title()}")
                piece_to_delete_1 = self.get_piece_to_delete(captured_piece_2.__class__, active_color_before_move_1)
                self.model.active_game.delete_piece(piece_to_delete_1.row, piece_to_delete_1.column)
                # Comunicate which piece needs to be deleted
                self.connection.send_socket({ "piece_to_delete": piece_to_delete_1, })
            else:
                # Communicate that no pieces need to be deleted
                self.connection.send_socket({ "piece_to_delete": None, })

            print("Processed my captures. About get captures")
            
            in_data = self.connection.get_socket()
            piece_to_delete_2 = in_data["piece_to_delete"]

            if piece_to_delete_2 != None:
                self.model.inactive_game.delete_piece(piece_to_delete_2.row, piece_to_delete_2.column)

            print("Got captures, about to start second loop")

            set_number += 1
        
    def has_planned_move(self):
        return self.interaction_controller.selected_piece != None and \
                self.interaction_controller.selected_ending_location != None

    def get_planned_move(self):
        res = [[self.interaction_controller.selected_piece.row, self.interaction_controller.selected_piece.column],
                self.interaction_controller.selected_ending_location]
        self.interaction_controller.selected_piece = None
        self.interaction_controller.selected_ending_location = None
        return res


    def get_piece_to_delete(self, piece_type, active_color_before_move):
            while(True):

                options = self.model.active_game.get_deletion_options(piece_type, active_color_before_move)

                for i, option in enumerate(options):
                    print(f"\t{i}: {option}")
                
                inpt = input("Which option would you like? ")
                selection = int(inpt)
                if selection < 0 or selection >= len(options): continue
                selected_option_to_delete = options[selection]
                confirmation = input(f"Would you like to delete {selected_option_to_delete}? ")
                if confirmation.lower() == "y" or confirmation.lower == "yes":
                    return selected_option_to_delete
                else:
                    continue

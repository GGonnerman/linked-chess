import socket
import pickle
import re

from game.util import *
from game.game import Game
from game.pieces.pawn import Pawn
from game.pieces.color import Color

def get_piece_to_move(game):
    while(True):
        print(game.board)
        # Get a piece selection from the user
        inpt = input("Piece to move (e.g., g5): ")
        # Allow them to gracefully quit
        if inpt == "q": exit(0)
        # Ensure its a valid piece to select 
        if is_valid_algebraic(inpt) == False: continue
        row, column = algebraic_to_coordinate(inpt)
        selected_piece = game.board.get_piece(row, column)
        if selected_piece == None: continue
        if selected_piece.color != game.board.active_color: continue
        # Confirm that the user wants to select the selected piece (and preview the potential moves)
        confirmation = input(f"Would you like to select the {selected_piece.name} on {coordinate_to_algebraic([row, column])} who has the potential moves of {' '.join([coordinate_to_algebraic(opt) for opt in selected_piece.get_potential_moves(game.board)])}? ")
        if confirmation.lower() == "y" or confirmation.lower == "yes":
            return selected_piece
        else:
            continue


def get_destination_location(game, selected_piece):
    while(True):
        # Give the user their possible options in a list
        options = selected_piece.get_potential_moves(game.board)
        print("Here are you possible options:")
        for i, option in enumerate(options):
            print(f"\t{i}: {coordinate_to_algebraic(option)}")
        # Get the chosen option from the list
        inpt = input("Which option would you like? ")
        selection = int(inpt)
        if selection < 0 or selection >= len(options): continue
        selected_ending_location = options[selection]
        # Confirm the user agrees with this selection
        confirmation = input(f"Would you like to move the {selected_piece.name} on {coordinate_to_algebraic([selected_piece.row, selected_piece.column])} to {coordinate_to_algebraic(selected_ending_location)}? ")
        if confirmation.lower() == "y" or confirmation.lower == "yes":
            return selected_ending_location
        else:
            continue


def get_piece_to_delete(game, piece_type, active_color_before_move):
        while(True):

            options = game.get_deletion_options(piece_type, active_color_before_move)

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

def print_info(game):
    print(f"It is your turn, {game.board.active_color.name.title()}")

def read_socket(conn_in):
    data = conn_in.recv(1024)
    return data

def get_socket(conn_in):
    return pickle.loads(read_socket(conn_in))

def send_socket(s, data):
    s.sendall(pickle.dumps(data))

def get_partner_address():
    inpt = input("Are you the server or client? ").lower()
    if inpt == "server":
        print("Listening for connections")
        return None
    elif inpt == "client":
        while(True):
            inpt = input("What is your partners IP address? ")
            confirmation = input(f"Would you like to connect to {inpt}? ")
            if confirmation.lower() == "y" or confirmation.lower == "yes":
                return inpt
            else:
                continue
    
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

        
if __name__ == "__main__":

    HOST = get_local_ip()
    PORT = 65432
    s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_in.bind((HOST, PORT))
    s_in.listen(5)

    print(f"Your local ip is {HOST}")

    partner_address = get_partner_address()

    # TODO: This is unnecessarily complex. Just make them both type in the other person's local ip
    # Neither person is really the 'server' or 'client' in a meaningful capacity
    # I am the server, I dont know partners address
    if partner_address == None:
        # Constantly watch for incoming message and then grab its address
        while(True):
            conn_in, addr_in = s_in.accept()
            addr, data = read_socket(conn_in)
            data = data.decode("utf-8")
            # If not the correct code, close the connection and try again
            if data != "1989":
                conn_in.close()
                continue
            # If it is correct, save that address
            partner_address = addr
            break
        # Setup an out socket to that address
        s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_out.connect((partner_address, PORT))
        # Send something to that address so it knows I exist
        send_socket(s_out, "1991".encode("utf-8"))
    else:
        # Setup an out socket to the user-provided address
        s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_out.connect((partner_address, PORT))

        # Send something to that address so it knows I exist
        send_socket(s_out, "1989".encode("utf-8"))

        # Constantly watch for a response to know we're able to communicate
        while(True):
            conn_in, addr_in = s_in.accept()
            addr, data = read_socket(conn_in)
            data = data.decode("utf-8")
            # If not the correct code, close the connection and try again
            if data != "1991":
                conn_in.close()
                continue
            break


    game_1 = Game()
    game_1.start()

    game_2 = Game()
    game_2.start()

    set_count = 0

    while(True):

        if set_count % 2 == 0:
            active_game = game_1
            inactive_game = game_2
        else:
            active_game = game_2
            inactive_game = game_1

        print(f"Start of a new turn. This is game {'1' if set_count % 2 == 0 else '2'}")
        print_info(active_game)
        piece_to_move_1 = get_piece_to_move(active_game)

        selected_ending_location_1 = get_destination_location(active_game, piece_to_move_1)

        active_color_before_move_1 = active_game.board.active_color
        active_color_before_move_2 = inactive_game.board.active_color

        send_socket(s_out, {
            "piece_to_move": piece_to_move_1,
            "selected_ending_location": selected_ending_location_1,
            })
        
        in_data = get_socket(conn_in)
        piece_to_move_2 = in_data["piece_to_move"]
        selected_ending_location_2 = in_data["selected_ending_location"]

        captured_piece_1 = active_game.board.get_piece(*selected_ending_location_1)
        captured_piece_2 = inactive_game.board.get_piece(*selected_ending_location_2)

        active_game.board.attempt_move(piece_to_move_1.get_location(), selected_ending_location_1)
        inactive_game.board.attempt_move(piece_to_move_2.get_location(), selected_ending_location_2)

        if captured_piece_2 != None:
            # Prompt for the piece to delete, and delete it
            print(f"You have to delete a piece in your active game, {active_color_before_move_1.name.title()}")
            piece_to_delete_1 = get_piece_to_delete(active_game, captured_piece_2.__class__, active_color_before_move_1)
            active_game.delete_piece(piece_to_delete_1.row, piece_to_delete_1.column)
            # Comunicate which piece needs to be deleted
            send_socket(s_out, { "piece_to_delete": piece_to_delete_1, })
        else:
            # Communicate that no pieces need to be deleted
            send_socket(s_out, { "piece_to_delete": None, })
        
        in_data = get_socket(conn_in)
        piece_to_delete_2 = in_data["piece_to_delete"]

        if piece_to_delete_2 != None:
            inactive_game.delete_piece(piece_to_delete_2.row, piece_to_delete_2.column)

        set_count += 1
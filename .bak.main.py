import socket
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

def read_socket(s):
    conn, addr = s.accept()
    data = conn.recv(1024).decode("utf-8")
    conn.close()
    return [addr, data]

def get_socket_input(s):
    return read_socket(s)[1]

def send_socket(s, message):
    s.sendall(message.encode("utf-8"))

def get_partner_address():
    inpt = input("Are you the server or client?").lower()
    if inpt == "server":
        print("Listening for connections")
        return None
    elif inpt == "client":
        while(True):
            inpt = input("What is your partners IP address? ")
            confirmation = input(f"Would you like to connect to {inpt}")
            if confirmation.lower() == "y" or confirmation.lower == "yes":
                return inpt
            else:
                continue
        

if __name__ == "__main__":

    HOST = "127.0.0.1"
    PORT = 65432
    s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_in.bind((HOST, PORT))
    s_in.listen(5)

    partner_address = get_partner_address()

    # I am the server, I dont know partners address
    if partner_address == None:
        # Constantly watch for incoming message and then grab its address
        while(True):
            addr, data = read_socket(s_in)
            if data != "1991": continue
            partner_address = addr
            break
        # Setup an out socket to that address
        s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_out.bind((addr, PORT))
        # Send something to that address so it knows I exist
        send_socket(s_out, "1989")
    else:
        # Setup an out socket to the user-provided address
        s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_out.bind((partner_address, PORT))

        # Send something to that address so it knows I exist
        send_socket(s_out, "1991")

        # Constantly watch for a response to know we're able to communicate
        while(True):
            addr, data = read_socket(s_in)
            if data != "1989": continue
            break


    game_1 = Game()
    game_1.start()

    game_2 = Game()
    game_2.start()
    game_2.board.active_color = Color.BLACK

    turn_count = 0

    while(True):

        print("Running for game 1...")
        print_info(game_1)
        piece_to_move_1 = get_piece_to_move(game_1)

        selected_ending_location_1 = get_destination_location(game_1, piece_to_move_1)
        print("Running for game 2...")
        print_info(game_2)
        piece_to_move_2 = get_piece_to_move(game_2)

        selected_ending_location_2 = get_destination_location(game_2, piece_to_move_2)

        active_color_before_move_1 = game_1.board.active_color
        active_color_before_move_2 = game_2.board.active_color

        captured_piece_1 = game_1.board.get_piece(*selected_ending_location_1)
        captured_piece_2 = game_2.board.get_piece(*selected_ending_location_2)

        game_1.board.attempt_move(piece_to_move_1.get_location(), selected_ending_location_1)
        game_2.board.attempt_move(piece_to_move_2.get_location(), selected_ending_location_2)

        if captured_piece_2 != None:
            print(f"You have to delete a piece in game 1, {active_color_before_move_1.name.title()}")
            piece_to_delete_1 = get_piece_to_delete(game_1, captured_piece_2.__class__, active_color_before_move_1)
            game_1.delete_piece(piece_to_delete_1.row, piece_to_delete_1.column)

        if captured_piece_1 != None:
            print(f"You have to delete a piece in game 2, {active_color_before_move_2.name.title()}")
            piece_to_delete_2 = get_piece_to_delete(game_2, captured_piece_1.__class__, active_color_before_move_2)
            game_2.delete_piece(piece_to_delete_2.row, piece_to_delete_2.column)

        turn_count += 1
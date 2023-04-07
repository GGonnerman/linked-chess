from model.util import is_valid_coordinate

def add_until_end(selected_piece, gameboard, *changes):
    potential_moves = []
    for change in changes:
        row = selected_piece.row
        column = selected_piece.column
        while (True):
            row += change[0]
            column += change[1]
            # Check is it is a place in the board
            if not is_valid_coordinate([row, column]):
                break
            # If is ampty, add and keep going
            if gameboard.get_piece(row, column) == None:
                potential_moves.append([row, column])
            # If there is a piece, move to the next direction
            else:
                # If that piece is the opposite color, add it before moving to next direction
                if gameboard.get_piece(row, column).color != selected_piece.color:
                    potential_moves.append([row, column])
                break
    return potential_moves


def add_selected(selected_piece, gameboard, *changes):
    potential_moves = []
    # Loop through every valid square (given by offsets [row, col])
    for change in changes:
        row = selected_piece.row
        column = selected_piece.column
        row += change[0]
        column += change[1]
        # Skip if outside of the board
        if not is_valid_coordinate([row, column]):
            continue
        # Add if it is an empty square
        elif gameboard.get_piece(row, column) == None:
            potential_moves.append([row, column])
        # Add if it is a piece of the opposite color (a capture)
        elif gameboard.get_piece(row, column).color != selected_piece.color:
            potential_moves.append([row, column])
    return potential_moves

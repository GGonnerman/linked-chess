import time

def wait_until(predicte, timeout, period=0.25, *args, **kwargs):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if predicte(*args, **kwargs): return True
        time.sleep(period)
    return False

def coordinate_to_algebraic(coordinate):
    if not is_valid_coordinate(coordinate): return False
    # Ensure row and column are ints
    row, column = [int(x) for x in coordinate]
    r = 8 - row
    f = {
        0: "a",
        1: "b",
        2: "c",
        3: "d",
        4: "e",
        5: "f",
        6: "g",
        7: "h",
    }[column]
    return f"{f}{r}"

def algebraic_to_coordinate(algebraic):
    if not is_valid_algebraic(algebraic): return False
    f, r = algebraic # e.g., g5
    row = 8 - int(r)
    column = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
    }[f]
    return [row, column]

def is_valid_algebraic(algebraic):
    if len(algebraic) != 2: return False
    f, r = algebraic # e.g., g5
    if f not in "abcdefgh": return False
    if r not in "12345678": return False
    return True

def is_valid_coordinate(coordinate):
    if len(coordinate) != 2: return False
    row, column = [int(x) for x in coordinate]
    if row < 0 or row >= 8: return False
    if column < 0 or column >= 8: return False
    return True
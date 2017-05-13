assignments = []

# INITIAL CONFIGURATION ##########
rows = 'ABCDEFGHI'
cols = '123456789'


def configure_board_data():
    boxes = cross(rows, cols)
    unit_list = create_units()
    units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

    return boxes, unit_list, units, peers


def create_units():
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
    diagonal_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'], ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
    return row_units + column_units + square_units + diagonal_units


def cross(A, B):
    return [a + b for a in A for b in B]


boxes, unit_list, units, peers = configure_board_data()


# AUXILIARY TOOLS ##########

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def convert_grid_values(grid):
    """
    Converting grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """

    all_digits = '123456789'
    unassigned = '.'
    values = list(grid)

    for value in range(0, len(grid)):
        if values[value] == unassigned:
            values[value] = all_digits

    assert len(values) == 81
    return dict(zip(boxes, values))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[box]) for box in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in rows:
        print(''.join(values[row + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if row in 'CF': print(line)
    return


# STRATEGIES ##########


def naked_twins(values):
    """
    Eliminating values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    for unit in unit_list:
        # Find all instances of naked twins for unit
        unit_values = {box: values[box] for box in unit}
        naked_twins_candidates = [box for box in unit if len(unit_values[box]) == 2]
        naked_twins_valid = {box: unit_values[box] for box in naked_twins_candidates if list(unit_values.values()).count(unit_values[box]) > 1}

        if len(naked_twins_valid) > 0:

            # Eliminate the naked twins as possibilities for their peers
            for twin, twin_value in naked_twins_valid.items():
                for box in unit:
                    if not is_naked_twin_or_resolved(values, twin_value, box):
                        # Replace first digit of naked twin
                        values = assign_value(values, box, values[box].replace(twin_value[0], ""))
                        # Replace second digit of naked twin
                        values = assign_value(values, box, values[box].replace(twin_value[1], ""))
    return values


def is_naked_twin_or_resolved(values, twin_value, box):
    return values[box] == twin_value or len(values[box]) == 1

def eliminate(values):
    """
    Eliminating values from peers of each box with a single value.

    Going through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for box, value in values.items():
        if len(value) == 1:
            for peer in values:
                if peer in peers[box]:
                    values = assign_value(values, peer, values[peer].replace(value, ""))
    return values


def only_choice(values):
    """
    Finalize all values that are the only choice for a unit.

    Going through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    digits = '123456789'
    for unit in unit_list:
        for digit in digits:
            digit_places = [box for box in unit if digit in values[box]]
            if len(digit_places) == 1:
                values = assign_value(values, digit_places[0], digit)
    return values


# MAIN ROUTINES ##########


def reduce_puzzle(values):
    """
    Iterating eliminate() and only_choice().
    1. If at some point, there is a box with no available values, return False.
    2. If the sudoku is solved, return the sudoku.
    3. If after an iteration of both functions, the sudoku remains the same, return the sudoku.

    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        solved_values_before = get_solved_values(values)
        # Eliminate Strategy
        values = eliminate(values)
        # Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = get_solved_values(values)
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if exists_box_with_no_values(values):
            return False
    return values


def exists_box_with_no_values(values):
    return len([box for box in values.keys() if len(values[box]) == 0])


def get_solved_values(values):
    # Check how many boxes have a determined value
    return len([box for box in values.keys() if len(values[box]) == 1])


def search(values):
    """
    Creating a search tree and solving the Sudoku using Depth-First Search and Constraint Propagation
    """
    not_reduceable = False

    # First, reduce the puzzle
    sudoku = reduce_puzzle(values)

    if sudoku is not_reduceable:
        return not_reduceable

    if is_puzzle_solved(sudoku):
        return sudoku

    _, box = choose_unfilled_square(sudoku)

    # Using recursion to solve each one of the resulting Sudokus
    for value in sudoku[box]:
        new_sudoku = sudoku.copy()
        new_sudoku[box] = value
        attempt = search(new_sudoku)
        if attempt:
            # If it returns a value (not False), return that answer!
            return attempt


def choose_unfilled_square(values):
    # Choosing one of the unfilled squares with the fewest possibilities
    return min((len(values[b]), b) for b in boxes if len(values[b]) > 1)


def is_puzzle_solved(values):
    return all(len(values[b]) == 1 for b in boxes)


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(convert_grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

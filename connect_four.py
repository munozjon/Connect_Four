import numpy as np

# main board rows
main_rows_arr = np.zeros((6, 7), int)

# board columns function
def arr_of_columns(row_arr):
    temp_cols_arr = []
    for i in range(len(row_arr) + 1):
        temp_col = []
        for v in row_arr:
            temp_col.append(v[i])
        temp_cols_arr.append(temp_col)
    cols_arr = np.array(temp_cols_arr)
    return cols_arr

# main columns
main_cols_arr = arr_of_columns(main_rows_arr)


# visualizer
def visual_board(rows_arr):
    # Resets the color to default 
    off = '\x1b[0m'
    # Sets the color to red for player 1
    red = '\x1b[31m'
    # Sets the color to yellow for player 2
    yel = '\x1b[33m'
    # the pieces that will visually show a player's token
    piece = '*'
    cells = ['-', red + piece + off, yel + piece +  off]
    visual_rows = np.array([i for i in rows_arr[::-1]])
    for row in visual_rows:
        print(' '.join([cells[u] for u in row]))
    print(*range(1, 7 + 1))


# returns list of consecutives for rows and columns when called
def subsequences(arr, length):
    subsequent_items = []
    for iterable in arr:
        subsequent_items += (iterable[i: i + length] for i in range(len(iterable) - length + 1))
    return subsequent_items

# returns list of all consecutive diagonal sets in "/" orientation
def consecutive_diagonals(iterable, length):
    list_of_all_items = []
    for list in iterable:
        for i in list:
            list_of_all_items.append(i)
    all_diagonals = []
    row_goalpost = 0
    while row_goalpost < 15:
        goalpost = row_goalpost
        set_limiter = 0
        while set_limiter < 4:
            temporary_set = []
            index = goalpost
            while len(temporary_set) < length:
                temporary_set.append(list_of_all_items[index])
                index += 8
            all_diagonals.append(temporary_set)
            goalpost += 1
            set_limiter += 1
        row_goalpost += 7
    return np.array(all_diagonals)

# returns list of all consecutive diagonal sets in "\" orientation
def consecutive_reverse_diagonals(iterable, length):
    reverse_rows = []
    for list in iterable:
        reverse_rows.append(list[::-1])
    all_reverse_diagonals = consecutive_diagonals(reverse_rows, length)
    return all_reverse_diagonals



# method to check if any tokens match four consecutive 1's or 2's
def check_consecutive(l):
    if all(i == 1 for i in l) == True:
        return True
    elif all(i == 2 for i in l) == True:
        return True
    else:
        return False


def after_turn_check(rows_arr, num_in_a_row):
    cols_arr = arr_of_columns(rows_arr)

    # arrays for consecutive diagonals and reverse diagonals
    diagonals_check = consecutive_diagonals(rows_arr, num_in_a_row)
    reverse_diagonals_check = consecutive_reverse_diagonals(rows_arr, num_in_a_row)

    # arrays for consecutive rows and columns
    rows_check = subsequences(rows_arr, num_in_a_row)
    columns_check = subsequences(cols_arr, num_in_a_row)

    # runs "check_consecutives" for all 4 'check' variables, returns False if all fail
    for row in rows_check:
        if check_consecutive(row) == True:
            return True
    for column in columns_check:
        if check_consecutive(column) == True:
            return True
    for diagonal in diagonals_check:
        if check_consecutive(diagonal) == True:
            return True
    for reverse_diagonal in reverse_diagonals_check:
        if check_consecutive(reverse_diagonal) == True:
            return True
    return False

# adds a player's move to the next open space in the column they selected
def add_to_board(move, rows_arr, player):
    move = int(move) - 1
    for row in rows_arr:
        if row[move] == 0:
            row[move] = player
            break
    return rows_arr



print("Welcome to Connect Four!")

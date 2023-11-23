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

# checks for a win after each turn
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


# gameplay
def game(rows_arr):

    # ensures a turn ends when it needs to for each player
    player_one_turn = True
    player_two_turn = False

    # show the board to the players at the start
    print("\nPlayer 1's tokens are red and Player 2's tokens are yellow. Have fun!\n")
    visual_board(rows_arr)
    
    # keeps the game going until players decide to quit or the game ends
    play_again = ""

    while play_again != "q":

        # player one's turn
        while player_one_turn == True:
            # inputs the player's move
            player_move = input("\nMake your move, Player 1!\n")

            # checks that the player gave a number
            if player_move.isdigit():

                # checks that the player gave a valid column number
                if int(player_move) in range(1, len(rows_arr[0]) + 1):

                    # checks that the column chosen is not full
                    if rows_arr[5][int(player_move) - 1] == 0:
                        
                        # player's move is added to the board and the visual is returned after the move
                        add_to_board(player_move, rows_arr, 1)
                        print("\n")
                        visual_board(rows_arr)

                        # checks if the move resulted in a win
                        if after_turn_check(rows_arr, 4) == True:
                            print("Outstanding! Player 1 wins!")
                            play_again = "q"
                            break

                        else:

                            # checks if there is any more spaces available to play after each player's turn
                            full_board_count = 0
                            for row in rows_arr:
                                if 0 not in row:
                                    full_board_count += 1
                            if full_board_count == len(rows_arr):
                                print("Congrats, nobody wins!")
                                play_again = "q"
                                player_one_turn = False
                            
                            # turn ends for the player and starts for the next player. option to quit the game is given
                            else:
                                player_one_turn = False
                                player_two_turn = True
                                play_again = input("\nKeep the game going! Or enter 'q' to quit.\n")
                    else:
                        print("No more spaces available for that column. Try again!")
                else:
                    print("Please enter a valid column number!")
            else:
                print("Please enter a column number.")
        
        # ends game if player decides to quit after their turn
        if play_again == "q":
            break

        # player two's turn (conditions checked are the same as for player one)
        while player_two_turn == True:
            
            player_move = input("\nPlayer 2's turn! Choose a column:\n")
            
            if player_move.isdigit():
                
                if int(player_move) in range(1, len(rows_arr[0]) + 1):
                    
                    if rows_arr[5][int(player_move) - 1] == 0:
                        
                        add_to_board(player_move, rows_arr, 2)
                        print("\n")
                        visual_board(rows_arr)

                        if after_turn_check(rows_arr, 4) == True:

                            print("Amazing! Player 2 wins!")
                            play_again = "q"
                            break

                        else:
                            full_board_count = 0
                            for row in rows_arr:
                                if 0 not in row:
                                    full_board_count += 1
                            if full_board_count == len(rows_arr):
                                print("Congrats, nobody wins!")
                                play_again = "q"
                                player_two_turn = False
                            
                            else:
                                player_one_turn = True
                                player_two_turn = False
                                play_again = input("\nNo winner just yet, keep going! Or enter 'q' to quit.\n")
                    else:
                        print("No more spaces available for that column. Try again!")
                else:
                    print("Please enter a valid column number!")
                
            else:
                print("Please enter a column number.")

        if play_again == "q":
            break

# introduces the game and asks the players to start the game
def start_game():
    print("\nWelcome to Connect Four!\nCreated by: Jonathan Munoz\n\nPlace tokens on a 7x6 board and try to get 4 in a row to win!\nThis is a 2 player game, so grab a friend and play together!\n")
    initializer = input("Are you both ready? Type 'y' to start!\n")
    if initializer == "y":
        game(main_rows_arr)

start_game()

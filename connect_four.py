import numpy as np

# main board rows
# creates an array of the rows for the board, with 6 rows of 7 values (all zeroes initially)
main_rows_arr = np.zeros((6, 7), int)

# board columns function
# creates an array of the columns for the board by iterating through the 'rows' array and appending the [i] index of the [v] list in the array to a 'temp_col'
# then appending that list to 'temp_cols_arr', before finally turning that into an array and returning it
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


print("Welcome to Connect Four!")

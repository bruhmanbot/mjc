import numpy as np


def check_nxn_diags(matrix) -> list:
    # Takes 2D nxn binary matrix and checks to see which diagonals have non zero product
    # Output index for items making up a non-zero diagonal
    # Check for square matrix
    if matrix.shape[0] != matrix.shape[1]:
        print("Check diag function failed: Not a square matrix")
        return ["Error"]
    else:
        non_zero_diags = []
        # Dimension of matrix determines the number of diagonals in 1 way
        # Going bottom right
        iterations = matrix.shape[0]
        for i in range(iterations):
            diagonal_product = 1
            templist = []

            for j in range(iterations):
                diagonal_product = matrix[j][(i + j) % iterations] * diagonal_product
                templist.append(int(j*iterations+ ((i + j) % iterations)))
                # Index of the diagonal items in the full list

            if diagonal_product:
                non_zero_diags.append(templist)


        # Going top right
        for i in range(iterations):
            diagonal_product = 1

            templist = []

            for j in range(iterations):
                diagonal_product = matrix[j][(i - j) % iterations] * diagonal_product
                templist.append(int(j*iterations+ ((i - j) % iterations)))
                # Index of the diagonal items in the full list

            if diagonal_product:
                non_zero_diags.append(templist)

    # Returning result
    return non_zero_diags

if __name__ == '__main__':
    ser = np.array([1, 1, 1, 0, 1, 0, 1, 0, 0])

    ser = ser.reshape((3, 3))

    print(check_nxn_diags(ser))
    print('skipt')

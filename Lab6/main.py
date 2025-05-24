def transpose(matrix):
    transposed_matrix = []

    for i in range(len(matrix[0])):

        transposed_row = []

        for row in matrix:
            transposed_row.append(row[i])

        transposed_matrix.append(transposed_row)

    return transposed_matrix


def wald_criterion(matrix):
    minimal_winning = [min(strategy) for strategy in matrix]

    return minimal_winning.index(max(minimal_winning)) + 1


def savage_criterion(matrix):
    transpose_matrix = transpose(matrix)

    maximum_winning = [max(assumption) for assumption in transpose_matrix]

    risk_matrix = [row[:] for row in matrix]

    for i in range(len(risk_matrix)):

        for j in range(len(risk_matrix)):
            risk_matrix[i][j] = maximum_winning[j] - risk_matrix[i][j]

    maximum_risking = [max(strategy) for strategy in risk_matrix]

    return maximum_risking.index(min(maximum_risking)) + 1


def hurwitz_criterion(matrix, pessimism=0.5):
    minimal_winning = [min(strategy) for strategy in matrix]

    maximum_winning = [max(strategy) for strategy in matrix]

    h = [minimal_winning[i] * pessimism + maximum_winning[i] * (1 - pessimism) for i in range(len(matrix))]

    return h.index(max(h)) + 1


winning_matrix = [
    [22, 7, 44, 97, 64, 80],
    [15, 56, 97, 36, 16, 85],
    [36, 9, 71, 60, 6, 76],
    [94, 55, 76, 89, 90, 46],
    [4, 5, 75, 19, 40, 80],
    [6, 13, 36, 84, 15, 85]
]

print("Wald optimal strategy:", wald_criterion(winning_matrix))

print("Savage optimal strategy:", savage_criterion(winning_matrix))

print("Hurwitz optimal strategy:", hurwitz_criterion(winning_matrix, 0.9))

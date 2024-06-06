def lcs(X, Y):
    m = len(X)
    n = len(Y)
    L = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    common_lines = {}
    i, j = m, n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            if X[i - 1] not in common_lines:
                common_lines[X[i - 1]] = []
            common_lines[X[i - 1]].append((i - 1, j - 1))  # Correcting indexing here
            i -= 1
            j -= 1
        elif L[i - 1][j] > L[i][j - 1]:
            i -= 1
        else:
            j -= 1

    for key in common_lines:
        common_lines[key].reverse()

    return common_lines


def generate_diff(X, Y, common_lines):
    # Sort common lines based on their indices in X and Y
    sorted_common_lines = sorted(common_lines.items(), key=lambda x: x[1][0])

    diff = []
    prev_x = prev_y = 0

    for line, indices in sorted_common_lines:
        for x_idx, y_idx in indices:
            # Lines in X before the common line
            for x_line in X[prev_x:x_idx]:
                diff.append(f"< {x_line}")
            prev_x = x_idx + 1

            # Lines in Y before the common line
            for y_line in Y[prev_y:y_idx]:
                diff.append(f"> {y_line}")
            prev_y = y_idx + 1

            # Common line
            diff.append(f"  {line}")

    # Lines in X after the last common line
    for x_line in X[prev_x:]:
        diff.append(f"< {x_line}")

    # Lines in Y after the last common line
    for y_line in Y[prev_y:]:
        diff.append(f"> {y_line}")

    return "\n".join(diff)


# # Example usage
# X = ["A", "X", "B", "Y", "C", "Z"]
# Y = ["A", "B", "C"]
# # common_lines = {"A": [(0, 0)], "B": [(1, 1)], "C": [(2, 2)]}
# common_lines = lcs(X,Y)

# diff = generate_diff(X, Y, common_lines)
# print(diff)

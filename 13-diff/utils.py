def lcs(X, Y):
    m = len(X)
    n = len(Y)

    # Create a 2D array to store lengths of longest common subsequence
    L = [[0] * (n + 1) for i in range(m + 1)]

    # Build the L[m+1][n+1] in bottom-up fashion
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    # L[m][n] contains the length of LCS for X[0..m-1], Y[0..n-1]
    length_of_lcs = L[m][n]

    # Create a list to store the LCS
    lcs = [""] * (length_of_lcs + 1)
    lcs[length_of_lcs] = "\0"

    # Start from the right-most-bottom-most corner and
    # one by one store characters in lcs[]
    i = m
    j = n
    index = length_of_lcs - 1
    while i > 0 and j > 0:
        # If current character in X and Y are same, then
        # current character is part of LCS
        if X[i - 1] == Y[j - 1]:
            lcs[index] = X[i - 1]
            i -= 1
            j -= 1
            index -= 1

        # If not same, then find the larger of two and
        # go in the direction of larger value
        elif L[i - 1][j] > L[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(lcs[:-1])


# Example usage
X = "AGGTAB"
Y = "GXTXAYB"
print("Longest Common Subsequence is", lcs(X, Y))

a = [[0] * 5 for i in range(5)]
for i in range(5):
    for j in range(5):
        if i == j:
            a[i][j] = 1
        else:
            a[i][j] = i + 1 + j + 1
for i in range(5):
    print(*a[i])
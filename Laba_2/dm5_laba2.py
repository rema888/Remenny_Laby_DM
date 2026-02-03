def count_paths(m, n):

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    dp[0][0] = 1

    # Заполняем первую строку
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0]  # = 1

    # Заполняем первый столбец
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1]  # = 1

    # Заполняем остальную часть таблицы
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Чтобы попасть в (i, j), можно прийти:
            # - слева: из (i-1, j) → шаг вправо
            # - снизу: из (i, j-1) → шаг вверх
            dp[i][j] = dp[i-1][j] + dp[i][j-1]

    return dp[m][n]

print("Число кратчайших путей (без ограничений):", count_paths(22, 18))

def count_paths_no_up_twice(m, n):

    dp_R = [[0] * (n + 1) for _ in range(m + 1)]
    dp_U = [[0] * (n + 1) for _ in range(m + 1)]

    dp_R[0][0] = 1
    dp_U[0][0] = 0

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 and j == 0:
                continue

            # Пришли в (i, j) шагом вправо (R)
            # Можно прийти из (i-1, j) любым способом (R или U)
            if i > 0:
                dp_R[i][j] = dp_R[i-1][j] + dp_U[i-1][j]

            # Пришли в (i, j) шагом вверх (U)
            # Можно прийти из (i, j-1), только если предыдущий шаг был R (иначе будет 2U подряд)
            if j > 0:
                dp_U[i][j] = dp_R[i][j-1]

    return dp_R[m][n] + dp_U[m][n]

print("Число кратчайших путей (без двух вертик.участков подряд):", count_paths_no_up_twice(22, 18))
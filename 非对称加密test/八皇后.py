global Queen
def check(row, column):
    # 检查行列
    for k in range(8):
        if Queen[k][column] == 1:
            return False

    # 检查主对角线

    for i, j in zip(range(row - 1, -1, -1), range(column - 1, -1, -1)):
        if Queen[i][j] == 1:
            return False

            # 检查副对角线
    for i, j in zip(range(row - 1, -1, -1), range(column + 1, 8)):
        if Queen[i][j] == 1:
            return False

    return True


def print_queen():
    print(Queen)
    for i in range(8):
        for j in range(8):
            if Queen[i][j] == 1:
                print('☆ ' * j + '★ ' + '☆ ' * (7 - j))
    print("\n\n")






def find_Queen(row):
    if row > 7:
        global count
        count += 1
        print_queen()
        return

    for column in range(8):
        if check(row, column):
            Queen[row][column] = 1
            find_Queen(row + 1)
            Queen[row][column] = 0
count=0
find_Queen(8)
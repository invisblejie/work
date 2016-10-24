def solve(problem):
    meno = []
    solvel(problem, meno)
    return meno[0]

def solvel(puzzle,meno):
    #get a meno including possible solution for puzzle
    if not puzzle: return
    possible = findpuzzle(puzzle)
    if not possible: return
    aim = smallpossible(possible)
    if aim == 0:
        meno.append(puzzle)
        return
    for i in range(1,len(possible[aim])):
        puzzlecopy = [j[:] for j in puzzle]
        puzzlecopy[aim[0]][aim[1]] = possible[aim][i]
        solvel(puzzlecopy,meno)
    return meno

def findpuzzle(board):
    # get possible number for every position in board,and judge whether board is right
    allnumber = [1,2,3,4,5,6,7,8,9]
    nine = getnine(board)
    position = {}
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                position[(i,j)] = [[0]]  
            else:
                row = [ x for x in board[i]]
                if not testpuzzle(row): return
                line = [ y[j] for y in board]
                if not testpuzzle(line): return
                ninepuzzle = [x for x in nine[(int(i / 3), int(j / 3))]]
                if not testpuzzle(ninepuzzle): return
                a =[x for x in set(allnumber) - (set(row) | set(line) |set(ninepuzzle))]
                if len(a) == 0: return
                position[(i,j)] = [[len(a)]] + a[:] 
    return position

def getnine(puzzle):
    # divide every position in puzzle into 3*3
    nine = {}
    for k in range(9):
        for l in range(9):
            a = int(k /3 )
            b = int(l / 3)
            if (a, b) in nine:
                nine[(a, b)].append(puzzle[k][l])
            else:
                nine[(a, b)] = [puzzle[k][l]]
    return nine
   
def testpuzzle(temple):
    # test whether puzzle is right or not
    for i in range(9):
        if temple[i] != 0:
            if temple.index(temple[i]) != i:
                return None
    return True
        
def smallpossible(possible):
    # get the position which has smallest possibility
    small = 9
    aim = 0
    for i in possible:
        if possible[i][0][0] != 0:
            if possible[i][0][0] <= small:
                small = possible[i][0][0]
                aim = i
    return aim

problem = [[9, 0, 0, 0, 8, 0, 0, 0, 1],
 [0, 0, 0, 0, 0, 6, 0, 0, 0],
 [0, 0, 5, 0, 7, 0, 3, 0, 0],
 [0, 6, 0, 0, 0, 0, 0, 4, 0],
 [4, 0, 1, 0, 6, 0, 5, 0, 8],
 [0, 9, 0, 0, 0, 0, 0, 2, 0],
 [0, 0, 7, 0, 3, 0, 2, 0, 0],
 [0, 0, 0, 7, 0, 5, 0, 0, 0],
 [1, 0, 0, 0, 4, 0, 0, 0, 7]]
puzzle = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]
 
print(solve(puzzle))

class turn:
    def left_to_right(net, start):
        for i in range(start[1],len(net[start[0]]) - 1):
            if net[start[0]][i + 1] == 0: 
                break
            else:
                start = [start[0], i]
                net[start[0]][i] = 0
        return net, start

        
    def up_to_down(net, start):
        for i in range(start[0],len(net) - 1):
            if net[i + 1][start[1]] == 0:
                break
            else:
                start = [i, start[1]]
                net[i][start[1]] = 0
        return net, start

    def right_to_left(net, start):
        for i in range(start[1], 0, -1):
            if net[start[0]][i - 1] == 0:
                break
            else:
                start = [start[0], i]
                net[start[0]][i] = 0
        return net, start

    def down_to_up(net, start):
        for i in range(start[0], 0, -1):
            if net[i - 1][start[1]] == 0:
                break
            else:
                start = [i, start[1]]
                net[i][start[1]] = 0
        return net, start

def spiralize(size):
    net = [[1]*size for i in range(size)]
    if size == 1:
        return [1]
    start = [1,0]
    temple = False
    while start != temple:
        temple = start
        net, start = turn.left_to_right(net, start)
        net, start = turn.up_to_down(net, start)
        net, start = turn.right_to_left(net, start)
        net, start = turn.down_to_up(net, start)
    return net


assert (spiralize(8) == [[1,1,1,1,1,1,1,1],
                                  [0,0,0,0,0,0,0,1],
                                  [1,1,1,1,1,1,0,1],
                                  [1,0,0,0,0,1,0,1],
                                  [1,0,1,0,0,1,0,1],
                                  [1,0,1,1,1,1,0,1],
                                  [1,0,0,0,0,0,0,1],
                                  [1,1,1,1,1,1,1,1]])

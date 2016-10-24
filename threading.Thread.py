import threading
import time


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

##def thread_fun(num):
##    for n in range(int(num)):
##        print (solve(puzzle))
##        print ("\n I come from %s, number: %s" %(threading.currentThread().getName(), n))
##    print("\n hello")
##
##def main(thread_num):
##    thread_list = list()
##
##    for i in range(thread_num):
##        thread_name = "Okthread_%s" %(i)
##        thread_list.append(threading.Thread(target = thread_fun,name = thread_name, args = (1,)))
##
##    for thread in thread_list:
##        thread.start()
##
##    for thread in thread_list:
##        thread.join()
##
##if __name__ == "__main__":
##    main(3)

        
    
                           
##class MyThread(threading.Thread):
##    def __init__(self):
##        threading.Thread.__init__(self)
##        self.setName("new" + self.name)
##
##    def run(self):
####        print(solve(puzzle))
##        print("I am %s\n"%(self.name))
##
##if __name__ == "__main__":
##    for i in range(5):
##        my_thread = MyThread()
##        my_thread.start()


##counter = 0
##class MyThread(threading.Thread):
##    def __init__(self):
##        threading.Thread.__init__(self)
##
##    def run(self):
##        global counter
##        time.sleep(1)
##        counter += 1
##        print("I am %s,counter is %d"%(self.name, counter))
##
##if __name__ == "__main__":
##    for i in range(225):
##        MyThread().start()
##        

##
##counter = 0
##mutex = threading.Lock()
##
##class MyThread(threading.Thread):
##    def __init__(self):
##        threading.Thread.__init__(self)
##
##    def run(self):
##        global counter
##        time.sleep(1)
##        if mutex.acquire():
##            counter += 1
##            print("I am %s,counter is %d"%(self.name, counter))
##            mutex.release()
##
##if __name__ == "__main__":
##    for i in range(225):
##        My_Thread = MyThread()
##        My_Thread.start()




##counterA = 0
##counterB = 0
##
##mutexA = threading.Lock()
##mutexB = threading.Lock()
##
##class MyThread(threading.Thread):
##    def __init__(self):
##        threading.Thread.__init__(self)
##
##    def run(self):
##        self.fun1()
##        self.fun2()
##        
##    def fun1(self):
##        global mutexA, mutexB
##        if mutexA.acquire():
##            print("I am %s , get res: %s"%(self.name, "ResA"))
##            
##            if mutexB.acquire():
##                print("I am %s , get res: %s"%(self.name,"ResB"))
##                mutexB.release()
##        mutexA.release()
##
##    def fun2(self):
##        global mutexA, mutexB
##        if mutexB.acquire():
##            print("I am %s , get res: %s"%(self.name, "ResB"))
##            
##            if mutexA.acquire():
##                print("I am %s , get res: %s"%(self.name,"ResA"))
##                mutexA.release()
##        mutexB.release()
##
##if __name__ == "__main__":
##    for i in range(225):
##        MyThread().start()



##
##counter = 0
##mutex = threading.RLock()
##
##class MyThread(threading.Thread):
##    def __init__(self):
##        threading.Thread.__init__(self)
##
##    def run(self):
##        global counter,mutex
##        time.sleep(11)
##        if mutex.acquire():
##            counter += 1
##            print("I am %s , counter: %s"%(self.name, counter))
##            if mutex.acquire():
##                counter += 1
##                print("I am %s , counter: %s"%(self.name, counter))
##                mutex.release()
##            mutex.release()
##            
##if __name__ == "__main__":
##    for i in range(225):
##        MyThread().start()                




Condition = threading.Condition()
Products = 0

class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global Condition,Products
        while True:
            if Condition.acquire():
                if Products < 10:
                    Products += 1
                    print("Producer (%s) : deliver one, now products: %s"%(self.name, Products))
                    Condition.notifyAll()
                else:
                    print("Producer (%s) : already 10, stop deliver, now products:%s"%(self.name, Products))
                    Condition.wait()
                Condition.release()
                time.sleep(2)

class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global Condition, Products
        while True:
            if Condition.acquire():
                if Products > 1:
                    Products -= 1
                    print("Consumer (%s):consume one, now products: %s"%(self.name, Products))
                    Condition.notifyAll()
                else:
                    print("Consumer (%s):only one, stop consume, products: %s"%(self.name, Products))
                    Condition.wait()
            Condition.release()
            time.sleep(2)

if __name__ == "__main__":
    for p in range(10):
        Producer().start()
    for c in range(10):
        Consumer().start()



##class MyThread(threading.Thread):
##    def __init__(self, singal):
##        threading.Thread.__init__(self)
##        self.singal = singal
##
##    def run(self):
##        print("I am %s, I will sleep ..." %self.name)
##        self.singal.wait()
##        print("I am %s, I awake ..."%self.name)
##
##if __name__ == "__main__":
##    singal = threading.Event()
##    for i in range(5):
##        MyThread(singal).start()
##
##    print("main thread sleep 3 seconds...")
##    time.sleep(3)
##    singal.set()


                

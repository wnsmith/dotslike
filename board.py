from random import choice
from copy import deepcopy
from numpy import array


class Board():
    #static list lines; each line on the board is represented as '1' in a long binary number
    #each element of lines is a decimal representation of a single line on the board
    lines = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648, 4294967296, 8589934592, 17179869184, 34359738368, 68719476736, 137438953472, 274877906944, 549755813888, 1099511627776, 2199023255552, 4398046511104, 8796093022208, 17592186044416, 35184372088832, 70368744177664, 140737488355328, 281474976710656, 562949953421312, 1125899906842624, 2251799813685248, 4503599627370496, 9007199254740992, 18014398509481984, 36028797018963968, 72057594037927936, 144115188075855872, 288230376151711744, 576460752303423488, 1152921504606846976, 2305843009213693952, 4611686018427387904, 9223372036854775808, 18446744073709551616, 36893488147419103232, 73786976294838206464, 147573952589676412928, 295147905179352825856, 590295810358705651712, 1180591620717411303424, 2361183241434822606848, 4722366482869645213696, 9444732965739290427392, 18889465931478580854784, 37778931862957161709568, 75557863725914323419136, 151115727451828646838272, 302231454903657293676544, 604462909807314587353088, 1208925819614629174706176, 2417851639229258349412352, 4835703278458516698824704, 9671406556917033397649408, 19342813113834066795298816, 38685626227668133590597632, 77371252455336267181195264, 154742504910672534362390528, 309485009821345068724781056, 618970019642690137449562112, 1237940039285380274899124224, 2475880078570760549798248448, 4951760157141521099596496896, 9903520314283042199192993792, 19807040628566084398385987584, 39614081257132168796771975168]
    def __init__(self, linije, scr, side):
        self.linije = linije        #binary number holding lines
        self.side = side            #side to move, '1' or '-1'
        self.points = 57            #at the start there are 57 squares to be marked as either 'x' or 'o'
        #squares are for checking points
        #each element of self.squares is a decimal number representing
        #                        all the lines needed to make a square
        self.squares = [5, 11, 18, 544, 1124, 2248, 4496, 8448, 1064960, 2146816, 4293632, 8587264, 17174528, 34349056, 67633152, 34493956096, 69123178496, 138246356992, 276492713984, 552985427968, 1105970855936, 2211941711872, 4423883423744, 8813272891392, 4521226173153280, 9060044532350976, 18120089064701952, 36240178129403904, 72480356258807808, 144960712517615616, 289921425035231232, 579842850070462464, 1155182100513554432, 2310346608841064448, 597222346585601474560, 1194444693171202949120, 2388889386342405898240, 4777778772684811796480, 9555557545369623592960, 19111115090739247185920, 38222230181478494371840, 296300826683959672832, 76148159536273029070848, 5063557461256977080385536, 10127114922513954160771072, 20254229845027908321542144, 40508459690055816643084288, 81016919380111633286168576, 2455630571092215511121920, 159578208189131051061215232, 2949778999859695186283069440, 5899557999719390372566138880, 11799115999438780745132277760, 1315311291740716542080319488, 22282920707136844948184236032, 64372882042839774294754459648, 49517601571415210995964968960]
        self.scr = scr              #difference in points

    def done(self):
        if self.linije == 79228162514264337593543950335: # <---big number is just all lines marked on the board
            return True
        if abs(self.scr) > self.points:  #game if over if difference is greater than remaining points
            return True
        return False

#    def simulate(self):
#        tmp = deepcopy(self)
#        moves = tmp.getMoves()
#        while not tmp.done():
#            move = choice(moves)
#            tmp.playMove(move)
#            moves.remove(move)
#        return 1 - 2*(tmp.score()<0)
#
#    def sim(self, n):                 #simulates gameplay n times and returns average
#        sm = 0
#        for i in range(n):
#            sm += self.simulate()
#        return 1.0*sm/n

    def getMoves(self):                 #returns a list of all non-marked lines --> all possible moves
        moves = []
        for line in self.lines:
            if (line & self.linije) == 0:
                moves.append(line)
        return moves

    def playMove(self, move):
        self.linije |= move             #marks line on the board
        k = 0
        for i in range(len(self.squares)-1, -1, -1): #check if the added line formed a square (or two)
            if k>1:
                break
            if (self.squares[i] & self.linije) == self.squares[i]: #if it did, there is one less point in the game
                self.points -= 1
                k+=1
                if self.side == 1:
                    self.scr += 1
                else:
                    self.scr -= 1
                self.squares.pop(i)          #once the square is makred, it is removed from the list
        if k == 0:
            self.side *= -1                  #if players marked a square he has another turn

    def getNumpyArray(self):                 #creates numpy array which is used as an input to a neural network
        nar = []                             #first 4 elements are side, difference in points, number of lines left
        nar.append(self.side)                                                            #and number of points left
        nar.append(self.scr)                 #other 96 elements represent lines, '1' for marked line and '0' otherwise
        nar.append(96 - bin(self.linije).count('1'))
        nar.append(self.points)
        for line in self.lines:
            if (self.linije & line) > 0:
                nar.append(1)
            else:
                nar.append(0)
        return nar


    def printLines(self): #an attempt of visual representation of the board
        k = 0;
        for i in range(8):
            space = ' ' * (7-i)
            print(space, end='')
            for j in range(i+2):
                if (self.linije & self.lines[k]) > 0:
                    print('1 ', end='')
                else:
                    print('0 ', end='')
                k+=1
            print()
        for i in range(8):
            if (self.linije & self.lines[k]) > 0:
                print(' 1', end='')
            else:
                print(' 0', end='')
            k+=1
        print()
        for i in range(8):
            space = ' ' * i
            print(space, end='')
            for j in range(9-i):
                if (self.linije & self.lines[k]) > 0:
                    print('1 ', end='')
                else:
                    print('0 ', end='')
                k+=1
            print()
        print()










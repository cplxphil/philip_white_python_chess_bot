
# Philip White
# Began coding:  April 26, 2026


import copy

# Remember, we need to keep track of whether or not each King has ever moved, because
# that impacts whether or not castling is legal.



# Main "top parent" class--Piece

# Important fact about list:  Don't just do list1 = list2, that just passes the
#       address of list1 to list2.  To create a new list, write, list1 = list(list2).
# Use .copy()

class Board():
    def __init__(self, allPieces):

# An interesting comment:  We don't really need a board matrix; the allPieces function suffices, and that's cheaper memory-wise.

#        self.allsquares = []            # (file, rank)
#        for i in range(0,9):            # the 0 rank/file squares will be empty, and will stand for a speical move when called upon--they are for promoting to different pieces, in some cases, and 0,0 is for "off the board"
#            self.allsquares.append([])
#            for j in range (0,9):
#                squareTemp = Square(i,j)
#                self.allsquares[i].append(copy.deepcopy(squareTemp))
        self.allPieces = allPieces.copy()      # contains a list of all the piece elements
                                               # remember:  each piece has a square, not
                                               #   the other way around
    def textDisplay(self):
        print ("\n\n")
        for i in range(8,0,-1):
            printline = ""
            for j in range(1,9):
                foundOnePieceFlag = False
                for selectedPiece in self.allPieces:
                    if selectedPiece.square.rank == i and selectedPiece.square.file == j:
                        printline += selectedPiece.pieceId + " "
                        foundOnePieceFlag = True
                if foundOnePieceFlag == False:
                    printline += ". "
            print(printline)
            print ("\n")
        print ("\n\n")
            


class Square():
    def __init__(self, file, rank):
        self.file = file # 1-8, to stand for a-h, or 0 for "off the board"
                                    # and captured
        self.rank = rank # 1-8, or, 0 for "off the board" and captured
    # Note:  The square does not contain a piece, but the piece contains a
    #   square object.  If we want to see what piece a square contains, we can
    #   simply run through all the pieces--there are 32 at maximum--and check
    #   the square to see if any of the pieces are at that square.  It's linear
    #   time and quick to do that check...and it saves memory because we don't
    #   have to store a "double linking" between Square and Piece objects.
    # Because there are only 32 pieces, and there are 64 squares, it's
    #   actually quicker to do this check rather than check the squares for
    #   pieces stored in them.
    def __eq__(self,item):
        if not isinstance(item,Square):
            return NotImplemented
        else:
            return (self.file == item.file and self.rank == item.rank)
        
    def IsEmpty(chessboard):
        for p in chessboard.allPieces:
            if p.square.file == self.file and p.square.rank == self.rank:
                    return false

class Move():
    def __init__(self, move1squareSource, move1squareTarget, move2squareSource, move2squareTarget):
        self.move1squareSource = move1squareSource
        self.move1squareTarget = move1squareTarget
        self.move2squareSource = move2squareSource
        self.move2squareTarget = move2squareTarget
    def __eq__(self,item):                                  # The problem with this function is, I need to define a good == operator for Square too.  It's *not* needing deepcopy, it's needing ==!  I should probably remove all of the deepcopy and copy code!  I'll do it after a git commit command.
        if not isinstance(item, Move):
            return NotImplemented
        else:
            return (self.move1squareSource == item.move1squareSource and self.move1squareTarget == item.move1squareTarget and self.move2squareSource == item.move2squareSource and self.move2squareTarget == item.move2squareTarget)

    def printMove(self):
        print(f"Move:  {self.move1squareSource.file}, {self.move1squareSource.rank}, to {self.move1squareTarget.file}, {self.move1squareTarget.rank} ; {self.move2squareSource.file}, {self.move2squareSource.rank}, to {self.move2squareTarget.file}, {self.move2squareTarget.rank}")
        
    # Note:  If move2squareSource is a square (0,1-4), it's a pawn promotion...
    #   0 means queen, 1 means rook, 2 means bishop, 3 means knight
    # Make sure to keep that in mind when you build a "MakeMove" function.
    # It will need to parse the idea that a pawn is changing to a Queen, and
    #   it will look up the first move TargetSquare for sure.  DON'T use (0,0).


class Piece():
    def __init__(self, color, square):
        self.square = copy.deepcopy(square)
        self.color = color        # 0 is white, 1 is black
        # type is determined by the class that inherits a mover class later on;
        # the mover classes inherit this class
    def GetAllLegalMoves():
        pass
    def setSquare(self,sq):
        self.square = sq


# All inheritable "initial move inclusion" classes--all inherit Piece, and may
#   be inherited by individual chess piece classes, such as Pawn, Rook, etc.

class KingSpecialMover(Piece): # all possible King castling moves, depending
                               # on the King's color
    def IncludeMoves(self):
        SourceSquare = copy.deepcopy(self.square)
        MovesToAddList = []
        if (   (SourceSquare.rank == 8 and SourceSquare.file == 5 and self.color == 1)
            or (SourceSquare.rank == 1 and SourceSquare.file == 5 and self.color == 0)
           ): # castling is possibly legal because the King is at the right square
            if self.color == 0:
                MovesToAddList.append(Move(Square(5,1) , Square(7,1), Square(8,1) , Square(6,1)))  # White castles Kingside
            else:   # self.color == 1
                MovesToAddList.append(Move(Square(5,8) , Square(7,8), Square(8,8) , Square(6,1)))
        return MovesToAddList
        
    

class PawnSpecialMover(Piece):
    def IncludeMoves(self):
        pieceColor = self.color
        SourceSquare = self.square
        MovesToAddList = []
        # en passant
        if SourceSquare.rank == 5 and pieceColor == 1:
            if SourceSquare.file != 8:
                newMove = Move(copy.deepcopy(SourceSquare),Square(SourceSquare.file+1,6),Square(SourceSquare.file+1,5),Square(0,0)) # the last two parameters indicate that the pawn to the side of this pawn is captured...it will only work if the piece at that square is a pawn!
                MovesToAddList.append(copy.deepcopy(newMove))
            if SourceSquare.file != 1:
                newMove = Move(copy.deepcopy(SourceSquare),Square(SourceSquare.file-1,6),Square(SourceSquare.file-1,5),Square(0,0))
                MovesToAddList.append(copy.deepcopy(newMove))
        if SourceSquare.rank == 4 and pieceColor == 0:
            if SourceSquare.file != 8:
                newMove = Move(copy.deepcopy(SourceSquare),Square(SourceSquare.file+1,3),Square(SourceSquare.file+1,4),Square(0,0)) # the last two parameters indicate that the pawn to the side of this pawn is captured...it will only work if the piece at that square is a pawn!
                MovesToAddList.append(copy.deepcopy(newMove))
            if SourceSquare.file != 1:
                newMove = Move(copy.deepcopy(SourceSquare),Square(SourceSquare.file-1,3),Square(SourceSquare.file-1,3),Square(0,0))
                MovesToAddList.append(copy.deepcopy(newMove))
        # move two squares ahead if and only if on the first row...make sure to add in LinearObstruction restriction!
        if SourceSquare.rank == 2 and pieceColor == 0:
            newMove = Move(copy.deepcopy(SourceSquare),Square(SourceSquare.file,4),Square(0,0), Square(0,0))
            MovesToAddList.append(copy.deepcopy(newMove))
        if SourceSquare.rank == 7 and pieceColor == 1:
            newMove = Move(copy.deepcopy(SourceSquare),Square(SourceSquare.file,5),Square(0,0),Square(0,0))
            MovesToAddList.append(copy.deepcopy(newMove))
        # pawn promotions, INCLUDING diagonal pawn captures!
        if (SourceSquare.rank == 7 and pieceColor == 0) or (SourceSquare.rank == 2 and pieceColor == 1): # white pawn or black pawn
            # straight ahead one square, promote to all 4 possibilities
            # 0 2 is a special code for "add a knight out of nowhere", 0 3 is a special code for "bishop", 0 4 is a special code for "rook," 0 5 is a special code for "queen"
            for promotionPieceID in range(2,6):
                newMove = Move(copy.deepcopy(SourceSquare), Square(SourceSquare.file,SourceSquare.rank + (pieceColor == 0)*(1) + (pieceColor == 1)*(-1)), Square(0,promotionPieceID), Square(SourceSquare.file,SourceSquare.rank + (pieceColor == 0)*(1) + (pieceColor == 1)*(-1)))
                MovesToAddList.append(copy.deepcopy(newMove))
            # diagonal capture one square, promote to all 4 possibilities
            for promotionPieceID in range(2,6):
                if SourceSquare.file > 1:
                    newMove = Move(copy.deepcopy(SourceSquare), Square(SourceSquare.file-1,SourceSquare.rank + (pieceColor == 0)*(1) + (pieceColor == 1)*(-1)), Square(0,promotionPieceID), Square(SourceSquare.file-1,SourceSquare.rank + (pieceColor == 0)*(1) + (pieceColor == 1)*(-1)))
                    MovesToAddList.append(copy.deepcopy(newMove))
                if SourceSquare.file < 8:
                    newMove = Move(copy.deepcopy(SourceSquare), Square(SourceSquare.file+1,SourceSquare.rank + (pieceColor == 0)*(1) + (pieceColor == 1)*(-1)), Square(0,promotionPieceID), Square(SourceSquare.file+1,SourceSquare.rank + (pieceColor == 0)*(1) + (pieceColor == 1)*(-1)))
                    MovesToAddList.append(copy.deepcopy(newMove))
        # regular diagonal capture, excluding promotions
        if (SourceSquare.rank != 7 and pieceColor == 0) or (SourceSquare.rank != 2 and pieceColor == 1):
            if SourceSquare.file > 1:
                newMove = Move(copy.deepcopy(SourceSquare), Square(SourceSquare.file-1,SourceSquare.rank + (pieceColor == 0)*(1) + (pieceColor == 1)*(-1)),Square(0,0),Square(0,0))
                MovesToAddList.append(copy.deepcopy(newMove))
            if SourceSquare.file < 8:
                newMove = Move(copy.deepcopy(SourceSquare), Square(SourceSquare.file+1,SourceSquare.rank + (pieceColor == 0)*(1) + (pieceColor == 1)*(-1)),Square(0,0),Square(0,0))
                MovesToAddList.append(copy.deepcopy(newMove))
        # regular one move up move, excluding promotions
        if pieceColor == 0 and SourceSquare.rank != 7:
            newMove = Move(copy.deepcopy(SourceSquare), Square(SourceSquare.file,SourceSquare.rank + 1), Square(0,0), Square(0,0))
            MovesToAddList.append(copy.deepcopy(newMove))                                      
        if pieceColor == 1 and SourceSquare.rank != 2:
            newMove = Move(copy.deepcopy(SourceSquare), Square(SourceSquare.file,SourceSquare.rank - 1), Square(0,0), Square(0,0))
            MovesToAddList.append(copy.deepcopy(newMove))
        # that's everything!

        return MovesToAddList

        # Note, we added in "move one square ahead" directly...we can't use vertical forward mover and limit to one square at a time because some pawn moves are two at a time
    # also, do not add in the one-ahead move, or the diagonal capture move, if the pawn is promoting...that is handled as a special case above



    

class DiagonalMover(Piece):       # whether or not the target square has a piece on it, move the captured piece/non-piece to 0,0
    def IncludeMoves(self):
        SourceSquare = self.square
        MovesToAddList = []

        # Important note:  When we include two moves, watch out, because we will do the first move, and then the second move!  Be careful!
        for a in range(SourceSquare.file+1,8+1): # move file up and rank up
            TargetSquare = Square(a, (a-SourceSquare.file) + SourceSquare.rank)
            if (TargetSquare.rank < 9 and TargetSquare.file < 9):     # don't add the move if we went off the board
                MovesToAddList.append(Move(copy.deepcopy(SourceSquare),copy.deepcopy(TargetSquare),Square(0,0), Square(0,0)))      # whatever was on TargetSquare is moved off the board
        for a in range(SourceSquare.file-1, 1-1,-1): # move file down and rank down
            TargetSquare = Square(a, SourceSquare.rank - (SourceSquare.file - a))
            if (TargetSquare.rank > 0 and TargetSquare.file > 0):
                MovesToAddList.append(Move(copy.deepcopy(SourceSquare),copy.deepcopy(TargetSquare),Square(0,0), Square(0,0)))
        for a in range(SourceSquare.file+1,8+1):    # move file up and rank down
            TargetSquare = Square(a,SourceSquare.rank - (a - SourceSquare.file))
            if (TargetSquare.rank > 0 and TargetSquare.file < 9):
                MovesToAddList.append(Move(copy.deepcopy(SourceSquare),copy.deepcopy(TargetSquare),Square(0,0), Square(0,0)))
        for a in range(SourceSquare.file-1, 1-1,-1):  # move file down and rank up
            TargetSquare = Square(a,  (SourceSquare.file - a) + SourceSquare.rank)
            if (TargetSquare.rank < 9 and TargetSquare.file > 0):
                MovesToAddList.append(Move(copy.deepcopy(SourceSquare),copy.deepcopy(TargetSquare),Square(0,0), Square(0,0)))
    
        return MovesToAddList




class ForwardVerticalMover(Piece):
    def IncludeMoves(self):
        SourceSquare = copy.deepcopy(self.square)
        MovesToAddList = []
        for a in range(SourceSquare.rank+1, 8+1):
            TargetSquare = Square(SourceSquare.file,a)
            MovesToAddList.append(Move(copy.deepcopy(SourceSquare),copy.deepcopy(TargetSquare),Square(0,0), Square(0,0)))
        return MovesToAddList

class BackwardVerticalMover(Piece):
    def IncludeMoves(self):
        SourceSquare = copy.deepcopy(self.square)
        MovesToAddList = []
        for a in range(SourceSquare.rank-1, 1-1,-1):        # I had omitted the -1 here, oops
            TargetSquare = Square(SourceSquare.file,a)
            MovesToAddList.append(Move(copy.deepcopy(SourceSquare),copy.deepcopy(TargetSquare),Square(0,0), Square(0,0)))
        return MovesToAddList


class HorizontalMover(Piece):
    def IncludeMoves(self):
        SourceSquare = self.square
        MovesToAddList = []
        for a in range(SourceSquare.file+1, 8+1):
            TargetSquare = Square(a,SourceSquare.rank)
            MovesToAddList.append(Move(copy.deepcopy(SourceSquare),copy.deepcopy(TargetSquare),Square(0,0), Square(0,0)))
        for a in range(SourceSquare.file-1, 1-1, -1):
            TargetSquare = Square(a,SourceSquare.rank)
            MovesToAddList.append(Move(copy.deepcopy(SourceSquare),copy.deepcopy(TargetSquare),Square(0,0), Square(0,0)))
        return MovesToAddList
    
class KnightMover(Piece):
    def IncludeMoves(self):
        MovesToAddList = []
        SourceSquare = self.square
        for i in range(4):
        # this covers all of the Knight moves
            a = self.square.file + ((-1)**(i%2)) * 2
            b = self.square.rank + ((-1)**((int(i/2))%2)) * 1
            if (a < 9 and a > 0 and b < 9 and b > 0):  # cycle between +2/-2 and +1/-1, then, switch the two expressions and do +1/-1 and +2/-2
                TargetSquare = Square(a,b)
                MovesToAddList.append(Move(copy.deepcopy(SourceSquare), copy.deepcopy(TargetSquare), Square(0,0), Square(0,0)))
            # now redo it with the 1 and 2 swapped between file and rank
            a = self.square.file + ((-1)**(i%2)) * 1
            b = self.square.rank + ((-1)**((int(i/2))%2)) * 2
            if (a < 9 and a > 0 and b < 9 and b > 0):
                TargetSquare = Square(a,b)
                MovesToAddList.append(Move(copy.deepcopy(SourceSquare), copy.deepcopy(TargetSquare), Square(0,0), Square(0,0)))
        return MovesToAddList

                                    

# All inheritable "subsequent move exclusion" classes--all inherit Piece and may
#   be inherited by indiv. chess piece classes, as before.



class LinearObstructionRestricted(Piece):
    # Use an index going from 0 to 7 to handle all 8 linear routes
    # Begin by going through one route (at a time), searching for an obstruction,
    #   which can be a piece of any color.
    # Then, beyond that obstruction, drop all moves from the list.
    # I considered changing all the lists to sets, but decided not to.
    # To remove from a list, just find the element and then remove it.  It's easy
    #   enough to find elements within a list, and probably computationally
    #   cheaper to maintain a list.

    # I'm going to repeat code here, because it's simpler than doing a for loop with index 0 to 7.
    # I am claiming that that is the most efficient way to code this function.

    # I had to include "copy.deepcopy()" for a lot of objects here.

    # Just handle every "line" emanating from the source square--there are 8 "lines."
    def ExcludeMoves(self, chessboard, initialMovesList):
        toReturn = initialMovesList.copy()
        # print ("test")
        # for i in range(len(initialMovesList)):
        #    print(f"Move {i}:  {initialMovesList[i].move1squareSource.file}, {initialMovesList[i].move1squareSource.rank}, to {initialMovesList[i].move1squareTarget.file}, {initialMovesList[i].move1squareTarget.rank}")
        # print ("Zzz")
        #for i in range(len(toReturn)):
        #    print(f"Move {i}:  {toReturn[i].move1squareSource.file}, {toReturn[i].move1squareSource.rank}, to {toReturn[i].move1squareTarget.file}, {toReturn[i].move1squareTarget.rank}")
        

        foundObstruction = Square(0,0)
        targetSquare = copy.deepcopy(self.square)
        for horizontalIncrement in range (-1,2):              # values -1, 0, 1
            for verticalIncrement in range (-1,2):        # values -1, 0, 1
#                print ("begin")
                if horizontalIncrement != 0 or verticalIncrement != 0:
                    currSquare = copy.deepcopy(self.square)
                    for index in range(8):
                        currSquare.file += horizontalIncrement
                        currSquare.rank += verticalIncrement
                        if (currSquare.file < 1 or currSquare.file > 8 or currSquare.rank < 1 or currSquare.rank > 8):
                            break
                        # else
                        obstructionFound = False
                        for p in chessboard.allPieces:
#                            print ("here we go")
#                            print (p.square.rank)
#                            print (p.square.file)
                            if p.square.file == currSquare.file and p.square.rank == currSquare.rank:
                                # print("absolutely")
                                obstructionFound = True
                                foundObstruction = copy.deepcopy(p.square)
                                break
                            # print (currSquare.file)
                            # print (currSquare.rank)
                        if (obstructionFound == True):
                           # print ("indeed")
                           # print( foundObstruction.rank)
                           # print (foundObstruction.file)
                            
                            # use the same values of vertical and horizontal increment
                            dropMovesSquare = copy.deepcopy(foundObstruction)
                            dropMovesSquare.file += horizontalIncrement
                            dropMovesSquare.rank += verticalIncrement
                            while (dropMovesSquare.file < 9 and dropMovesSquare.file > 0 and dropMovesSquare.rank < 9 and dropMovesSquare.rank > 0
                                   and not (dropMovesSquare.file == currSquare.file and dropMovesSquare.rank == currSquare.rank)):
                                # print ("ouch")
                                # print (dropMovesSquare.file)
                                # print (dropMovesSquare.rank)
                                moveToDrop = Move(copy.deepcopy(self.square),copy.deepcopy(dropMovesSquare),Square(0,0),Square(0,0))
                                dropMovesSquare.file += horizontalIncrement
                                dropMovesSquare.rank += verticalIncrement

                                toRemove = []
                                for inToReturn in toReturn:
                                    # print ("yep!")
#                                    if moveToDrop.move1squareSource.file == inToReturn.move1squareSource.file and moveToDrop.move1squareSource.rank == inToReturn.move1squareSource.rank and moveToDrop.move1squareTarget.file == inToReturn.move1squareTarget.file and moveToDrop.move1squareTarget.rank == inToReturn.move1squareTarget.rank:
                                    if moveToDrop == inToReturn:
                                    # print("qqqq")
                                        toRemove.append(inToReturn)
                                for item in toRemove:
                                    toReturn.remove(item)
                            # be careful!  When you remove from a list, you must not mess up the indexing/etc.
#                            break    # we don't need to continue this loop after we've found the obstruction and done the removals
                                         # yes we do, we need to do the other pieces...omit the break statement!
#         for i in range(len(toReturn)):
#            print(f"Move {i}:  {toReturn[i].move1squareSource.file}, {toReturn[i].move1squareSource.rank}, to {toReturn[i].move1squareTarget.file}, {toReturn[i].move1squareTarget.rank}")
        return toReturn



class OneSquareAtATimeRestricted(Piece): # applies only to the King--the pawn needs a separate rule, because it can move two squares at first
    def ExcludeMoves(initialMovesList): # we actually don't need self here...and we don't need chessboard
        toReturn = copy.deepcopy(initialMovesList)
        toRemove = []
        for selectedMove in toReturn:   # we can't remove from the list we're busy iterating over
            horizontalDifference = abs(selectedMove.move1squareSource.file - selectedMove.move1squareTarget.file)
            verticalDifference = abs(selectedMove.move1squareSource.rank - selectedMove.move1squareTarget.rank)
            # print (horizontalDifference)
            # print (verticalDifference)
            # print(f"Move:  {selectedMove.move1squareSource.file}, {selectedMove.move1squareSource.rank}, to {selectedMove.move1squareTarget.file}, {selectedMove.move1squareTarget.rank}")

            if horizontalDifference > 1 or verticalDifference > 1:
                toRemove.append(selectedMove)
        for item in toRemove:
            toReturn.remove(item)       # this should work fine now, because I defined equality for the object
        return toReturn
        



#  THIS FUNCTION IS STILL UNDER CONSTRUCTION!  IT IS NOT DONE!

class PawnRestricted(Piece):  # handles:  pawn capturing when there is no piece there, pawn en passant when there is no piece there, pawn moving forwards to a square that is occupied by an opponent piece
    def ExcludeMoves(self, chessboard, initialMovesList):
        toReturn = initialMovesList.copy()
        toRemove = []
        # be careful about how promotion moves are phrased as Move() objects.  Update:  I changed how pawn promotions work.  Now, the target square is still written down as the second parameter; later, the second component of the move over-writes that square with the piece being promoted to

        # pawn capturing diagonally--is there really an opponent piece there?
        for chosenMove in initialMovesList:
            if abs(chosenMove.move1squareTarget.file - chosenMove.move1squareSource.file) == 1 and abs(chosenMove.move1squareTarget.rank - chosenMove.move1squareSource.file) == 1:   # it's a capture move
                clearTheCapture = False
                for piece in chessboard.allPieces:
                    if piece.color != self.color:           # look at positions of pieces that are not the same color as the pawn's color (self.color)
                        if piece.square.file == chosenMove.move1squareTarget.file and piece.square.rank == chosenMove.move1squareTarget.rank:  # yes, there is an enemy piece at this level
                            clearTheCapture = True
                if clearTheCapture == False:
                    toRemove.append(copy.deepcopy(chosenMove))

#        print ("All items in toReturn:")
#        for item3 in toReturn:
#            item3.printMove()

#        print ("All items in toRemove:")
        for item in toRemove:
#            item.printMove()
            for item2 in toReturn:
                if item == item2:
                    toReturn.remove(item2)
#                    print ("yes")
#                else:
#                    print("no, and:")
#                    item.printMove()
#                    item2.printMove()
#                    print ("???")
        return toReturn
            

class SpecialMovesRestricted(Piece): # restricts castling (King) only--pawn en passant is now down in "pawn restricted"
    pass

class CheckRestricted(Piece):  # disallows moves that leave the moving player's King in check after the move is made; this involves looking ahead 1 move, I'll need that function coded...but it's just
    pass                        # looking "1 move deep," at all legal moves the opponent can make after the first move.

class SameColorPieceOnTargetSquareRestricted(Piece):
    def ExcludeMoves(self, chessboard,initialMovesList):
        toReturn = copy.deepcopy(initialMovesList)
        toRemove = []
        for item in toReturn:
            for selectedPiece in chessboard.allPieces:
                if selectedPiece.square.file == item.move1squareTarget.file and selectedPiece.square.rank == item.move1squareTarget.rank:
                    if selectedPiece.color == self.color:
                        toRemove.append(item)
        for item in toRemove:
            toReturn.remove(item)
        return toReturn







class Queen(DiagonalMover, ForwardVerticalMover, BackwardVerticalMover, HorizontalMover, LinearObstructionRestricted):
    def setup(self):        # We don't want to override the inherited classes'
                            # init functions.
        self.pieceId = 'q'
#    def setSquare(self,file,rank):
#        self.square.file = file
#        self.square.rank = rank
    def testfunc(self, chessboard):             # comment this function out later
        movesList = []
        movesList += ForwardVerticalMover.IncludeMoves(self).copy() # This is crucial--to run a parent class's routine, refer to the
                                                # parentClass and pass self in to the member function, as it is done here
        movesList += DiagonalMover.IncludeMoves(self).copy()
        movesList += BackwardVerticalMover.IncludeMoves(self).copy()
        movesList += HorizontalMover.IncludeMoves(self).copy()
#        print ("flagA")
        for i in range(len(movesList)):
            print(f"Move {i}:  {movesList[i].move1squareSource.file}, {movesList[i].move1squareSource.rank}, to {movesList[i].move1squareTarget.file}, {movesList[i].move1squareTarget.rank}")
        # print("flagB")
        movesList = LinearObstructionRestricted.ExcludeMoves(self,chessboard,movesList)
        movesList = SameColorPieceOnTargetSquareRestricted.ExcludeMoves(self,chessboard, movesList)
#        print("flagB.5")
        for i in range(len(movesList)):
            print(f"Move {i}:  {movesList[i].move1squareSource.file}, {movesList[i].move1squareSource.rank}, to {movesList[i].move1squareTarget.file}, {movesList[i].move1squareTarget.rank}")
#        print("flagC")

class Rook():
    def setup(self):
        self.pieceId = 'r'
    pass






class Bishop():
    def setup(self):
        self.pieceId = 'b'
    pass

class Pawn(PawnSpecialMover, LinearObstructionRestricted, CheckRestricted, SameColorPieceOnTargetSquareRestricted):
    def setup(self):
        self.pieceId = 'p'
    def testfunc(self, chessboard):
        movesList = []
        movesList += PawnSpecialMover.IncludeMoves(self).copy()
        movesList = LinearObstructionRestricted.ExcludeMoves(self,chessboard,movesList)
        movesList = SameColorPieceOnTargetSquareRestricted.ExcludeMoves(self, chessboard, movesList)
        movesList = PawnRestricted.ExcludeMoves(self,chessboard,movesList)
        for i in range(len(movesList)):
            print(f"Move {i}:  {movesList[i].move1squareSource.file}, {movesList[i].move1squareSource.rank}, to {movesList[i].move1squareTarget.file}, {movesList[i].move1squareTarget.rank}")




class Knight(KnightMover):
    def setup(self):
        self.pieceId = 'n'
    def testfunc(self):
        movesList = []
        movesList += KnightMover.IncludeMoves(self).copy()
#        for i in range(len(movesList)):
#            print(f"Move {i}:  {movesList[i].move1squareSource.file}, {movesList[i].move1squareSource.rank}, to {movesList[i].move1squareTarget.file}, {movesList[i].move1squareTarget.rank}")
        

class King(DiagonalMover, ForwardVerticalMover, BackwardVerticalMover, HorizontalMover, KingSpecialMover):
    def setup(self):
        self.pieceId = 'k'
    def testfunc(self, chessboard):
        movesList = []
        movesList += DiagonalMover.IncludeMoves(self).copy() + ForwardVerticalMover.IncludeMoves(self).copy() + BackwardVerticalMover.IncludeMoves(self).copy() + HorizontalMover.IncludeMoves(self).copy() + KingSpecialMover.IncludeMoves(self).copy()
        movesList = OneSquareAtATimeRestricted.ExcludeMoves(movesList)
        for i in range(len(movesList)):
            print(f"Move {i}:  {movesList[i].move1squareSource.file}, {movesList[i].move1squareSource.rank}, to {movesList[i].move1squareTarget.file}, {movesList[i].move1squareTarget.rank}")







q = Queen(1,Square(4,8))
q.setup()  # always run the setup function right away
# q.testfunc()

print()

knight = Knight(1,Square(5,5))
knight.setup()
knight.setSquare(Square(3,3))
knight.testfunc()               # We are eventually going to rename "testfunc"
                                # to be something like "GetAllLegalMoves()".


print("###")

king = King(0,Square(5,1))
king.setup()



pawn = Pawn(1,Square(2,2))
pawn.setup()



chessboard = Board([q,knight,king,pawn])

print ("pre-pawn")

pawn.testfunc(chessboard)

print ("post-pawn")

king.testfunc(chessboard)

print("###")




# print ("Big test is coming:\n")

q.testfunc(chessboard)



chessboard.textDisplay()



# 05-01:  2:34 p.m.:  I coded for about 2 hours and 15 minutes today!  I need a break.




# 04-30, 2:29 p.m.:  I fixed DiagonalMover, I think!



# source:  https://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes (on __eq__ method)
# Something big I learned:  Use the __eq__ method to compare items that are class objects.  That way, you can remove them properly when you go through a list of them....

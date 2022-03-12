#NEWCODE Start
class Corp:
    def __init__(self, name: str, commander):
        self.commandAuthUsed = False    #checks whether this corp has used its command
        self.commander = commander      #commander piece, will either be a bishop or a king
        self.commanding = []       #pieces that are in the corp, not including the commander
        self.defeated = False 
        self.__name = name
        self.smallMove = False

    # returns name of corp
    def get_name(self):
        return self.__name
    
    #sets the whether the commander has used its one spot move to true
    def movedOne(self):
        self.smallMove = True

    #returns whether the commander has taken the one spot move
    def commanderMoved(self):
        return self.smallMove

    #checks if this corp is white side or black side
    def isWhite(self):
        if self.defeated == True:
            return
        return self.commander.is_white()

    #checks if this corp is commanded by an king or a bishop
    def checkKing(self):
        if self.commander.get_type() == 'King':
            return True
        return False

    #checks to see if the max corp size has been reached if this corp is commanded by a bishop
    def checkLeng(self):
        if self.checkKing() == False and len(self.commanding) == 6:
            print('Max core length exceeded')
            return False
        return True

    #checks to see if a piece is already in this corp
    def hasPiece(self, piece):
        if piece not in self.commanding:
            #print('Piece not in corp')
            return False
        return True

    #checks to see whether this corp has used its command authority
    def hasCommanded(self):
        return self.commandAuthUsed

    #adds a specific piece to this corp
    #this is only used by other functions of when initializing the corps
    #do not call directly within the code
    def addToCorp(self, piece):
        if piece.is_white() != self.isWhite():
            print('cant move piece of opposite color')
            return
        if not self.checkLeng():
            return
        if self.hasPiece(piece):
            print('piece already in corp')
            return
        self.commanding.append(piece)
        piece.set_corp(self)
        return

    #removes a piece from this corp
    def removeFromCorp(self, piece):
        if not self.hasPiece(piece):
            print('piece not in corp')
            return
        self.commanding.remove(piece)

    #resets the command authority
    def resetCommand(self):
        self.commandAuthUsed = False
        self.smallMove = False
    
    #sets the command authority to used if it has been
    def command(self):
        if self.hasCommanded():
            print("command authority is already used")
            return
        self.commandAuthUsed = True

    #This corp requests a piece from another corp
    #If the piece can be moved, it is added to this corp and removed from its previous corp
    def request_piece(self, piece):
        if piece.corp.hasCommanded():
            print("command authority is already used")
            return
        if piece.corp.isWhite() != self.isWhite():
            print('cant move piece of opposite color')
            return
        if self.hasPiece(piece):
            print('piece already in corp')
            return
        if self.checkKing() == piece.corp.checkKing():
            print('Bishop cant take from bishop')
            return
        if not self.checkLeng():
            return
        #if self.checkKing == True:   removed because delagation action is not command action
            #self.command()
        #else:
            #piece.corp.command()
        print('moving ', piece.get_name(), ' to ', self.__name )
        piece.corp.removeFromCorp(piece)
        self.addToCorp(piece)

    #This method is called when a bishop is defeated
    #All the pieces in that bishop's corp are added to the king's corp
    #This method is not required to be called when the king dies because the game will end.
    def captured(self, corp):
        if corp.isWhite() != self.isWhite():
            print('cant move piece of opposite color')
            return
        if not corp.checkKing():
            print('must return to king')
            return
        self.defeated = True
        self.commander = None
        #print(self.commanding)
        print('Moving pieces from defeated ', self.__name, ' to ', corp.__name)
        for piece in self.commanding:
            #print(piece.get_name())
            corp.addToCorp(piece)
        self.commanding.clear()

    #Prints the commander and all the pieces commanded in this corp
    def printCorp(self):
        if self.defeated == True:
            print("this corp no longer exists")
            return
        print('\n', self.__name, ':\n', self.commander.get_name())
        for piece in self.commanding:
            print(piece.get_name())
        print('\n')
#NEWCODE End

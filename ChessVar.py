# Author: Alyce Harlan
# GitHub username: chaynz22/aharlan22
# Date: 3 Aug 2023
# Description: A game that is a variant of Chess

class Piece:
    """Basic template for a piece that initializes: name, location, color,
    legal moves"""

    def __init__(self, name, loc, col):
        self._name = name
        self._loc = loc
        self._col = col

    def get_name(self):
        """Get method for the name of a Piece or its descendants"""
        return self._name

    def get_location(self):
        """Get method for the name of a Piece or its descendants"""
        return self._loc
class Rook(Piece):
    """Rook Class inherits from Piece class and in addition to the
    inherited features (name, location, color, etc.), further defines legal moves
    as being straight in any direction, i.e. a to a or 8 to 8"""
    def __init__(self, name, loc, col):
        super().__init__(name, loc, col)

class Bishop(Piece):
    """Bishop Class inherits from Piece class and in addition to the
    inherited features (name, location, color, etc.), further defines legal moves
    to be diagonal in any direction. i.e. 1a to 2b, 3c to 4d etc"""

    def __init__(self, name, loc, col):
        super().__init__(name, loc, col)


class Knight(Piece):
    """DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS:
        Knight Class inherits from Piece class and in addition to the
        inherited features (name, location, color, etc.), initializes legal moves
        to be L shapes 2 up and 1 over or 2 over and 1 down, etc.
        i.e. 2f to 4e"""
    def __init__(self, name, loc, col):
        super().__init__(name, loc, col)

class King(Piece):
        """King Class inherits from Piece class and in addition to the
        inherited features (name, location, color, etc.), defines legal moves
        to be omnidirectional one piece at a time, also has a parameter
        called in_check which returns False if the King can move to get
        out of the "kill zone" or True if all moves will still get it captured
        """
        def __init__(self, name, loc, col):
            super().__init__(name, loc, col)


def set_up_board():
    """Method to set up the board at the beginning of the game"""
    # Black players
    bk = King("bk", 'h1', "black")
    br = Rook("br", 'h2', "black")
    bb = Bishop("bb", 'g1', "black")
    bb2 = Bishop("bb2", 'g2', "black")
    bn = Knight("bn", 'f1', "black")
    bn2 = Knight("bn2", 'f2', "black")

    # White players
    wk = King("wk", 'a1', "white")
    wr = Rook("wr", 'a2', "white")
    wb = Bishop("wb", 'b1', "white")
    wb2 = Bishop("wb2", 'b2', "white")
    wn = Knight("wn", 'c1', "white")
    wn2 = Knight("wn2", 'c2', "white")

    # maybe don't need piece objects...

    row8 = [0, 0, 0, 0, 0, 0, 0, 0]
    row7 = [0, 0, 0, 0, 0, 0, 0, 0]
    row6 = [0, 0, 0, 0, 0, 0, 0, 0]
    row5 = [0, 0, 0, 0, 0, 0, 0, 0]
    row4 = [0, 0, 0, 0, 0, 0, 0, 0]
    row3 = [0, 0, 0, 0, 0, 0, 0, 0]
    row2 = ['wr', 'wb2', 'wn2', 0, 0, 'bn2', 'bb2', 'br']
    row1 = ['wk', 'wb', 'wn', 0, 0, 'bn', 'bb', 'bk']

    board = [row1, row2, row3, row4, row5, row6, row7, row8]
    return board


def convert_to_list_type_loc(loc):
    row = loc[1]  # is a number
    row_num = int(row)  # converts string letter to int
    column = loc[0]  # is a letter
    col = ord(column) - 96  # converts letter to int
    new_loc = (row_num - 1, col - 1)
    return new_loc


class ChessVar:
    """A class that implements methods to play a game similar to Chess
    where the player whose king makes it to row 8 first wins and the king
    cannot be captured"""
    def __init__(self):
        self._board = set_up_board()
        self._game_state = 'UNFINISHED'
        self._turn = "WHITE"

    def get_board(self):
        return self._board
    def get_turn(self):
        """returns the color string associated with the current
        player: black or white"""
        return self._turn

    def set_turn(self):
        """Sets whose turn it is based on who just went"""
        if self._turn == "WHITE":
            self._turn = "BLACK"
            return self._turn
        if self._turn == "BLACK":
            self._turn = "WHITE"
            return self._turn

    def get_game_state(self):
        """DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS: A method to assess how far along the game is.
        If white king is in the 8th row, and black cannot get there in one move, return white won
        if black king is in the 8th row, return black won
        if white king is in row 8 and black king can move to row 8 in one move, return tie
        else, return unfinished
        """
        return self._game_state

    def look_up_piece_by_location(self, location):
        """Takes as a parameter the "current location" of a piece that the user wants to
        make a move from. Returns the name of the piece"""
        # if location is say h1, convert to list[list] format
        row = location[1]  # is a number
        row_num = int(row)  # converts string letter to int
        column = location[0]  # is a letter
        col = ord(column) - 96  # converts letter to int
        board = self.get_board()
        piece = board[row_num - 1][col - 1]
        return piece

    def is_legal_move(self, loc1, loc2):
        """Takes as parameters two locations, where a piece is now and where the user wants to move it
         Then utilizes the look_up_piece_by_location method (and the first location parameter) to see
         what piece is there. Then checks if the move is legal
         Also uses the look_up_piece_by_location method to check if there is another piece
         already at the next location; if so, it will be removed from that player's
         dictionary/set of pieces
         Checks both kings "in check" methods, if either returns true then "is_legal_move"
         returns false"""
        p1 = self.look_up_piece_by_location(loc1)
        p2 = self.look_up_piece_by_location(loc2)

        if p1 == 0:  # if there is no piece at starting loc
            return False
        if p2 != 0:  # check if the destination is not empty
            if p2[0] == p1[0]:  # checks if the piece in the way is the same color
                return False
            if p2 == 'wk' or p2 == 'bk':  # cannot capture kings
                return False
        else:
            return True

    def make_move(self, curr_loc, next_loc):
        """This method takes as parameters where the piece is now and where the user wants to move them next
        If the next location is an illegal move (will put the other king in check or does not follow the
        allowed moves for that piece), raise an error else make the move
        Updates the current location of that piece in the dictionary, and updates the game state
        This method will utilize "is_legal_move" method in order to check the legal moves
        If is_legal_move returns false, raise an error
        At the end, update "turn" parameter"""
        legal = self.is_legal_move(curr_loc, next_loc)
        if legal is False:
            print("That move is illegal, try another one")
        else:
            piece = self.look_up_piece_by_location(curr_loc)
            now = convert_to_list_type_loc(curr_loc)
            later = convert_to_list_type_loc(next_loc)
            board = self.get_board()
            board[now[0]][now[1]] = 0
            board[later[0]][later[1]] = piece
            self._game_state = "unfinished"

            if piece == 'bk' and later[0] == 7:
                self._game_state = "BLACK_WON"
            if piece == 'wk' and 'bk' in board[6]:
                self._game_state = "TIE"

    def print_board(self):
        for n in range(0, 7):
            board = self.get_board()
            row = board[n]
            print(row)


def main():
    game = ChessVar()
    # move_result = game.make_move('c2', 'e3')
    # game.make_move('g1', 'f1')
    state = game.get_game_state()

    game.make_move('h1', 'h7')
    game.make_move('a1', 'a8')
    state = game.get_game_state()
    print(state)
    game.print_board()


if __name__ == "__main__":
    main()

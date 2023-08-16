# Author: Alyce Harlan
# GitHub username: chaynz22/aharlan22
# Date: 3 Aug 2023
# Description: A game that is a variant of Chess

class IllegalMove(Exception):
    """Exception class to be raised if user tries an illegal move"""
    pass


def set_up_board():
    """Method to set up the board at the beginning of the game
    Returns a list of lists for each row of the board"""

    # empty spaces are represented with a '0'
    row8 = [0, 0, 0, 0, 0, 0, 0, 0]
    row7 = [0, 0, 0, 0, 0, 0, 0, 0]
    row6 = [0, 0, 0, 0, 0, 0, 0, 0]
    row5 = [0, 0, 0, 0, 0, 0, 0, 0]
    row4 = [0, 0, 0, 0, 0, 0, 0, 0]
    row3 = [0, 0, 0, 0, 0, 0, 0, 0]
    row2 = ['wr', 'wb2', 'wn2', 0, 0, 'bn2', 'bb2', 'br']
    row1 = ['wk', 'wb', 'wn', 0, 0, 'bn', 'bb', 'bk']

    # rows are put in 8-1 so that printing is accurate
    board = [row1, row2, row3, row4, row5, row6, row7, row8]
    return board


def convert_to_list_type_loc(loc):
    """Converts the algebraic grids like 'a3' to list of list grids like [3][0]
    Returns a tuple of the two new indices"""
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
        """Get method for the board, returns the board in its latest state"""
        return self._board

    def get_turn(self):
        """Returns the color string associated with the current
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
        """Get method for the game state which is updated in the "make move" method"""
        return self._game_state

    def look_up_piece_by_location(self, location):
        """Takes as a parameter the "current location" of a piece that the user wants to
        make a move from. Returns the name of the piece. If the space is empty, returns 0"""
        # if location is say h1, convert to list[list] format
        row = location[1]  # is a number
        row_num = int(row)  # converts string letter to int
        column = location[0]  # is a letter
        col = ord(column) - 96  # converts letter to int
        board = self.get_board()
        piece = board[row_num - 1][col - 1]
        return piece

    def in_check(self):
        """Method to check if either king is in check after a move is made
        Returns a boolean which will be used by "is_legal_move" method"""
    def is_legal_move(self, loc1, loc2):
        """Checks if the desired move is legal and returns a boolean to the "make_move" method
        Utilizes the is_in_check method to check if either king will be in check after the move"""

        p1 = self.look_up_piece_by_location(loc1)  # gets the pieces at both locs
        p2 = self.look_up_piece_by_location(loc2)

        l1 = convert_to_list_type_loc(loc1)  # converts both location list readable indices
        l2 = convert_to_list_type_loc(loc2)

        def king_legal_moves():
            """An internal method for the "is_legal_move" method that checks
            that the king can only make one step at a time"""
            if abs(l2[0] - l1[0]) > 1 or abs(l2[1] - l1[1]) > 1:
                return False
            else:
                return True

        def rook_legal_moves():
            """An internal method for the "is_legal_move method to
            check that next move is in the same row or column for rook"""
            if l2[0] - l1[0] == 0:
                return True
            if l2[1] - l1[1] == 0:
                return True
            else:
                return False

        def bishop_legal_moves():
            """An internal method for the "is_legal_move method to
            check that next move is only in diagonals for bishops"""

        def knight_legal_moves():
            """An internal method for the "is_legal_move method to
            check that next move is in the same row or column for rook"""

        if p1 == 0:  # if there is no piece at starting loc
            return False
        if p2 != 0:  # check if the destination is not empty
            if p2[0] == p1[0]:  # checks if the piece in the way is the same color
                return False
            if p2 == 'wk' or p2 == 'bk':  # cannot capture kings
                return False
            if p1[1] == 'k':
                return king_legal_moves()
            if p1[1] == 'r':
                rook_legal_moves()
        if p2 == 0:
            if p1[1] == 'k':
                return king_legal_moves()

            if p1[1] == 'r':
                rook_legal_moves()

            # # Bishop legal moves
            # if p1[1] == 'b' or (p1[1] == 'b' and p1[2] == '2'):
            #
            #
            # # Knight legal moves
            # if p1[1] == 'n' or (p1[1] == 'n' and p1[2] == '2'):

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
            raise IllegalMove(Exception)
        if self._game_state == "WHITE_WON" or self._game_state == "BLACK_WON":
            return False
        else:
            piece = self.look_up_piece_by_location(curr_loc)
            now = convert_to_list_type_loc(curr_loc)
            later = convert_to_list_type_loc(next_loc)
            board = self.get_board()
            board[now[0]][now[1]] = 0
            board[later[0]][later[1]] = piece
            self.set_turn()  # update turn

            # update game state
            if piece == 'bk' and later[0] == 7:
                self._game_state = "BLACK_WON"
            if piece == 'wk' and 'bk' in board[6]:  # if white king is at row 8 and black king is one step behind
                self._game_state = "TIE"
            if piece == 'wk' and later[0] == 7 and 'bk' not in board[6]:
                self._game_state = "WHITE_WON"
            else:
                self._game_state = "UNFINISHED"

    def print_board(self):
        for n in range(0, 8):
            board = self.get_board()
            row = board[n]
            print(row)


def main():
    game = ChessVar()
    # move_result = game.make_move('c2', 'e3')
    # game.make_move('g1', 'f1')
    # state = game.get_game_state()

    print("move rook")
    try:
        game.make_move('h2', 'h6')
        print("move king")
        game.make_move('h1', 'h5')
        print("move king again")
        game.make_move('h5', 'h4')
    except IllegalMove:
        print("Move is illegal")

    print(game.get_game_state())
    game.print_board()


if __name__ == "__main__":
    main()

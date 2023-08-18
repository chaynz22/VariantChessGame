# Author: Alyce Harlan
# GitHub username: chaynz22/aharlan22
# Date: 3 Aug 2023
# Description: A game that is a variant of Chess where the king cannot be in check
# There are only 6 pieces per player, king, 2 knights, 2 bishops, and 1 rook


def set_up_board():
    """Method to set up the board at the beginning of the game
    Returns a list of lists for each row of the board and both
    player's starting positions"""

    # empty spaces are represented with a '0'
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
    """Converts the algebraic grids like 'a3' to list of list grids like [0][2]
    Returns a tuple of the two new indices"""
    row = loc[1]  # is a number
    row_num = int(row)  # converts string letter to int
    column = loc[0]  # is a letter
    col = ord(column) - 96  # converts letter to int
    new_loc = (row_num - 1, col - 1)
    return new_loc


def convert_loc_to_algebraic(loc_list):
    """Method to convert the list indices like [0][2] back to algebraic notation i.e. 'a3'
    Takes as a parameter the list from "look_up_loc_by_piece" """
    col = loc_list[1]
    row = loc_list[0]

    conversion = col + 1 + 96
    letter = chr(conversion)
    num = str(row + 1)

    alg_loc = letter + num
    return alg_loc


class ChessVar:
    """A class that implements methods to play a game similar to Chess
    where the player whose king makes it to row 8 first wins and the king
    cannot be captured"""
    def __init__(self):
        self._board = set_up_board()
        self._game_state = 'UNFINISHED'
        self._turn = "w"

    def get_board(self):
        """Get method for the board, returns the board in its latest state"""
        return self._board

    def get_turn(self):
        """Returns the color string associated with the current
        player: black or white"""
        return self._turn

    def set_turn(self):
        """Sets whose turn it is based on who just went"""
        if self._turn == "w":
            self._turn = "b"
            return self._turn
        if self._turn == "b":
            self._turn = "w"
            return self._turn

    def update_game_state(self):
        """Method to update the game state based on game rules"""
        board = self.get_board()
        if 'bk' in board[7]:
            self._game_state = "BLACK_WON"
        if 'wk' in board[7] and 'bk' in board[6]:  # if white king is at row 8 and black king is one step behind
            self._game_state = "TIE"
        if 'wk' in board[7] and 'bk' not in board[6]:
            self._game_state = "WHITE_WON"
        else:
            self._game_state = "UNFINISHED"

    def get_game_state(self):
        """Get method for the game state which is updated in the "make move" method
        using the update_game_state method"""
        return self._game_state

    def look_up_piece_by_location(self, location):
        """Takes as a parameter an algebraic location of a piece.
        Returns the name of the piece such as 'wk'. If the space is empty, returns 0"""
        # if location is say h1, convert to list[list] format
        row = location[1]  # is a number
        row_num = int(row)  # converts string letter to int
        column = location[0]  # is a letter
        col = ord(column) - 96  # converts letter to int
        board = self.get_board()
        piece = board[row_num - 1][col - 1]
        return piece

    def look_up_loc_from_piece(self, piece):
        """Method to look up the exact location of a piece using the name as a parameter like 'wk' or 'bk'"""
        board = self.get_board()
        list_loc = []
        for n in range(0, 8):
            for k in range(0, 8):
                if piece == board[n][k]:
                    list_loc.append(n)
                    list_loc.append(k)
                    return list_loc

    def is_legal_move(self, loc1, loc2):
        """Checks if the desired move is legal and returns a boolean to the "make_move" method"""

        p1 = self.look_up_piece_by_location(loc1)  # gets the pieces at both locations
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
            board = self.get_board()
            if l2[0] - l1[0] == 0:
                for n in range(l1[1] + 1, l2[1]):
                    if board[l1[0]][n] != 0:
                        return False
            if l2[1] - l1[1] == 0:
                for n in range(l1[0] + 1, l2[0] - 1):  # checks that the path is clear
                    if board[n][l1[1]] != 0:
                        return False
            if l2[0] - l1[0] != 0 and l2[1] - l1[1] != 0:
                return False
            else:
                return True

        def bishop_legal_moves():
            """An internal method for the "is_legal_move method to
            check that next move is only in diagonals for bishops"""
            board = self.get_board()
            if abs(l2[0] - l1[0]) == abs(l2[1] - l1[1]):  # change in rise/run is same = diagonal
                if l1[0] > l2[0]:  # assigns the high and low parameters so the for statement always works
                    high1 = l1[0]  # this also allows the bishop to move diagonally left or right
                    low1 = l2[0]
                else:
                    high1 = l2[0]
                    low1 = l1[0]
                if l1[1] > l2[1]:
                    high2 = l1[1]
                    low2 = l2[1]
                else:
                    high2 = l2[1]
                    low2 = l1[1]

                for k in range(low1 + 1, high1):  # uses the high and lows calculated above
                    for n in range(low2 + 1, high2 - 1):
                        if board[k][n] != 0:  # checks that the path is clear
                            return False

            if abs(l2[0] - l1[0]) != abs(l2[1] - l1[1]):  # change in rise and run are not equal so not diagonal
                return False
            else:
                return True

        def knight_legal_moves():
            """An internal method for the "is_legal_move method to
            check that next move is in "L" shape for knight, also
            the knight is the only piece that can jump other pieces"""
            if abs(l2[0] - l1[0]) == 2 and abs(l2[1] - l1[1]) == 1:
                return True
            if abs(l2[0] - l1[0]) == 1 and abs(l2[1] - l1[1]) == 2:
                return True
            if abs(l1[0] - l2[0]) == 2 and abs(l1[1] - l2[1]) == 1:
                return True
            if abs(l1[0] - l2[0]) == 1 and abs(l1[1] - l2[1]) == 2:
                return True
            else:
                return False

        if p1 == 0:  # if there is no piece at starting loc
            return False
        if p2 != 0:  # check if the destination is not empty
            if p2[0] == p1[0]:  # checks if the piece in the way is the same color
                return False
            if p1[1] == 'k':
                return king_legal_moves()
            if p1[1] == 'r':
                return rook_legal_moves()
            if p1[1] == 'b':
                return bishop_legal_moves()
            if p1[1] == 'n':
                return knight_legal_moves()

        if p2 == 0:
            if p1[1] == 'k':
                return king_legal_moves()
            if p1[1] == 'r':
                return rook_legal_moves()
            if p1[1] == 'b':
                return bishop_legal_moves()
            if p1[1] == 'n':
                return knight_legal_moves()

    def white_king_in_check(self):
        """Method to check if either king is in check after a move is made.
        If it is in check, make_move method will reverse the move.
        Returns a boolean which will be used by "is_legal_move" method"""
        king1_loc = self.look_up_loc_from_piece('wk')  # finds the white king
        king1_alg_loc = convert_loc_to_algebraic(king1_loc)  # converts location to algebraic
        board = self.get_board()
        list_loc = []
        check = False

        for n in range(0, 8):
            for k in range(0, 8):
                if board[n][k] != 0:
                    piece = board[n][k]
                    if piece[0] == 'b':
                        list_loc.insert(0, n)
                        list_loc.insert(1, k)
                        move = convert_loc_to_algebraic(list_loc)
                        if self.is_legal_move(move, king1_alg_loc):
                            return True
        return check

    def black_king_in_check(self):
        """Method to check if either king is in check after a move is made.
        If it is in check, make_move method will reverse the move.
        Returns a boolean which will be used by "is_legal_move" method"""
        king1_loc = self.look_up_loc_from_piece('bk')  # finds the white king
        king1_alg_loc = convert_loc_to_algebraic(king1_loc)  # converts location to algebraic
        board = self.get_board()
        list_loc = []
        check = False

        for n in range(0, 8):
            for k in range(0, 8):
                if board[n][k] != 0:
                    piece = board[n][k]
                    if piece[0] == 'w':
                        list_loc.insert(0, n)
                        list_loc.insert(1, k)
                        move = convert_loc_to_algebraic(list_loc)
                        if self.is_legal_move(move, king1_alg_loc):
                            return True
        return check

    def make_move(self, curr_loc, next_loc):
        """This method takes as parameters where the piece is now and where the user wants to move them next
        It utilizes the is_legal_move method and white_king_in_check and black_king_in_check methods
        to verify that all movements are legal; returns True if the move is successfully made and updates
        the game status and whose turn it is"""

        legal = self.is_legal_move(curr_loc, next_loc)
        turn = self.get_turn()

        if legal is False:
            return False
        if self._game_state == "WHITE_WON" or self._game_state == "BLACK_WON" or self._game_state == "TIE":
            return False
        else:
            piece = self.look_up_piece_by_location(curr_loc)
            if piece[0] != turn:
                return False
            else:
                now = convert_to_list_type_loc(curr_loc)
                later = convert_to_list_type_loc(next_loc)
                board = self.get_board()
                if board[later[0]][later[1]] == 'wk':  # cannot capture kings
                    return False
                if board[later[0]][later[1]] == 'bk':  # cannot capture kings
                    return False
                else:
                    board[now[0]][now[1]] = 0  # change old spot to 0
                    board[later[0]][later[1]] = piece  # change new spot to piece
                    check_wk = self.white_king_in_check()  # make sure kings aren't in check
                    check_bk = self.black_king_in_check()
                    if check_wk is True or check_bk is True:  # if kings are in check, revert the move
                        board[later[0]][later[1]] = 0
                        board[now[0]][now[1]] = piece
                        return False
                    else:  # passed all the checks :) move is successful
                        self.set_turn()  # update turn
                        self.update_game_state()  # update game state
                        return True

    def print_board(self):
        """Method for printing the board to visualize movements"""
        for n in range(0, 8):
            board = self.get_board()
            row = board[n]
            print(row)


def main():
    """Main method to test cases and run the game"""
    game = ChessVar()
    print("move white rook: legal")
    moved = game.make_move('a2', 'a6')
    print(moved)
    print("move black rook")
    result = game.make_move('h2', 'h4')
    print(result)
    state = game.get_game_state()
    print(state)
    print("move white king")
    king = game.make_move('a1', 'a2')
    print(king)
    print("move black bishop")
    bishop = game.make_move('g2', 'c6')
    print(bishop)
    print("move white king")
    white_king = game.make_move('a2', 'a3')
    print(white_king)
    print("move black rook")
    rook_again = game.make_move('h4', 'h3')
    print(rook_again)
    print(game.get_game_state())
    game.print_board()


if __name__ == "__main__":
    main()

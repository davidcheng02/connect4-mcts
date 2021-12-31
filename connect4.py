import copy 

class Connect4:
    num_rows = 6
    num_cols = 7
    win_cond = 4

    def __init__(self, board, turn):
        # board is current position of gameboard (2D array with 0s (empty), 1s (yellow), 2s (red))
        self.board = board
        # whose turn it is currently (0 for yellow, 1 for red)
        self.turn = turn

    def legal_moves(self):
        ''' Returns list of possible positions after making any move 
        '''
        possible_moves = []

        # go through all columns to drop pieces from
        for col in range(self.num_cols):
            found_move = False
            board_copy = copy.deepcopy(self.board)

            # start from bottom row of list, and find first empty hole 
            for row in range(self.num_rows - 1, -1, -1):
                if board_copy[row][col] == 0:
                    found_move = True
                    board_copy[row][col] = self.turn + 1
                    break

            if found_move:
                possible_moves.append(board_copy)

        return possible_moves

    def next_player(self):
        ''' Returns whose has current turn 
        '''
        return self.turn

    def result(self, new_board):   
        ''' Returns Connect 4 object from with new board and next player's turn 

            new_board -- 2D gameboard
        '''     
        new_turn = 1 - self.turn

        new_pos = Connect4(new_board, new_turn)
        
        return new_pos

    def game_over(self):
        ''' Checks if current position has 4 colors in a row. Returns 0 if not game over,
            1 if yellow has won, -1 if red has won, or 2 if draw 
        '''
        def check_hole(hole):
            ''' Returns values of all_yellow or all_red based on current hole value 
            '''
            if hole == 0:
                return False, False
            # if yellow hole then all_red is false 
            elif hole == 1:
                return True, False
            # if red hole then all_yellow is false
            else:
                return False, True 

        # iterate through 2-D array, checking each hole 
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                all_yellow = True
                all_red = True

                # check left 
                if (col - self.win_cond + 1) >= 0:
                    count = 0
                    # i is the column
                    for i in range(col - self.win_cond + 1, col + 1):
                        count += 1
                        checked_hole = check_hole(self.board[row][i])
                        all_yellow = all_yellow & checked_hole[0] 
                        all_red = all_red & checked_hole[1]

                    if all_yellow:
                        return 1
                    elif all_red:
                        return -1

                    all_yellow = True
                    all_red = True

                # check up-left-diagonal
                if (col - self.win_cond + 1) >= 0 and (row - self.win_cond + 1) >= 0:
                    # i is the row 
                    i = row - self.win_cond + 1
                    # j is the column
                    for j in range(col - self.win_cond + 1, col + 1):
                        checked_hole = check_hole(self.board[i][j])
                        all_yellow = all_yellow & checked_hole[0] 
                        all_red = all_red & checked_hole[1]
                        i += 1 

                    if all_yellow:
                        return 1
                    elif all_red:
                        return -1

                    all_yellow = True
                    all_red = True

                # check top
                if (row - self.win_cond + 1) >= 0:
                    # i is row index
                    for i in range(row - self.win_cond + 1, row + 1):
                        checked_hole = check_hole(self.board[i][col])
                        all_yellow = all_yellow & checked_hole[0] 
                        all_red = all_red & checked_hole[1]

                    if all_yellow:
                        return 1
                    elif all_red:
                        return -1

                    all_yellow = True
                    all_red = True

                # check up-right-diagonal
                if (col + self.win_cond) <= self.num_cols and (row - self.win_cond + 1) >= 0:
                    # i is row index
                    i = row
                    for j in range(col, col + self.win_cond):
                        checked_hole = check_hole(self.board[i][j])
                        all_yellow = all_yellow & checked_hole[0] 
                        all_red = all_red & checked_hole[1]
                        i -= 1

                    if all_yellow:
                        return 1
                    elif all_red:
                        return -1
                    
                    all_yellow = True
                    all_red = True

                # don't need to check any of these below, because they are covered by the above checks
                # check right 
                # check down-right-diagonal
                # check down
                # check down-left-diagonal 

        # if no connect 4's, then check if entire board is filled out
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.board[row][col] == 0:
                    return 0

        return 2

    def winner(self):
        res = self.game_over()

        # if not game over, then no winner 
        if not res:
            return None
        # yellow won
        elif self.game_over() == 1:
            return 1
        # red won 
        elif self.game_over() == -1:
            return -1
        # == 2, draw 
        else:
            return 0
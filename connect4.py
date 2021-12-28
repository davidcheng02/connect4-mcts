import copy 

class Connect4:
    num_rows = 6
    num_cols = 7
    win_cond = 4

    def __init__(self, pos, turn):
        # pos is current position of gameboard (2D array with 0s (empty), 1s (yellow), 2s (red))
        self.pos = pos
        # whose turn it is currently (0 for yellow, 1 for red)
        self.turn = turn

    def legal_moves(self):
        '''
        Returns list of possible positions after making any move 
        '''
        possible_moves = []

        # go through all columns to drop pieces from
        for col in range(self.num_cols):
            found_move = False
            pos_copy = copy.deepcopy(self.pos)

            # start from bottom row of list, and find first empty hole 
            for row in range(self.num_rows - 1, -1, -1):
                if pos_copy[row][col] == 0:
                    found_move = True
                    pos_copy[row][col] = self.turn + 1
                    break

            if found_move:
                possible_moves.append(pos_copy)

        return possible_moves

    def next_player(self):
        return self.turn

    def result(self, move):        
        if self.turn == 1:
            new_turn = 0
        else:
            new_turn = 1

        new_pos = Connect4(move, new_turn)
        
        return new_pos

    def game_over(self):
        '''
        Checks if current position has 4 colors in a row. Returns 0 if not game over,
        1 if yellow has won, -1 if red has won, or 2 if draw 
        '''
        def check_hole(hole):
            '''
            Returns values of all_yellow or all_red based on current hole value 
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
                        checked_hole = check_hole(self.pos[row][i])
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
                        checked_hole = check_hole(self.pos[i][j])
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
                        checked_hole = check_hole(self.pos[i][col])
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
                        checked_hole = check_hole(self.pos[i][j])
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
                if self.pos[row][col] == 0:
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
        # draw 
        else:
            return 0
    

# yellow = 0
# red = 1

# pos =   [[0, 0, 0, 1, 0, 0, 0], 
#         [0, 0, 0, 1, 0, 0, 0], 
#         [0, 0, 0, 1, 0, 0, 0], 
#         [0, 0, 0, 1, 0, 1, 0], 
#         [0, 1, 1, 1, 0, 1, 1], 
#         [1, 1, 1, 1, 1, 1, 1]]

# gameboard = Connect4(pos, yellow)


# for move in gameboard.legal_moves():
#     print_2d_array(move, 6, 7)
#     print()
# print(gameboard.legal_moves())
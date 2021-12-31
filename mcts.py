import random
import math
from connect4 import Connect4

def mcts_strategy(num_iter):
    ''' Returns a function that returns the best move for Kalah given current position and number of iterations.
    '''
    def fxn(pos, num_iter=num_iter):
        move = mcts(num_iter, pos)
        return move

    return fxn

def object_in_pos_dict(pos, pos_dict):
    for key in pos_dict.keys():
        if key.board == pos.board and key.turn == pos.turn:
            return key

    return None

def mcts(num_iter, pos):
    ''' Calculates best move given current position and number of iterations using Monte Carlo tree search, 
        composed of traversal, expansion, rollout, and backpropagation steps.
    '''

    if pos.game_over():
        return None
    # key is position
    # value is [count, total reward]
    # initialize dictionary with parent and its children 
    pos_dict = {pos: [0, 0]}

    for next_move in pos.legal_moves():
        next_pos = pos.result(next_move)
        pos_dict[next_pos] = [0, 0]

    curr_iter = 0

    while curr_iter < num_iter:
        # selects leaf to rollout from and saves the path from root to leaf
        leaf, path = ucb_select(pos, pos_dict, [])

        # gets the win/loss/draw result after randomly rolling out leaf to terminal node 
        result = rollout(leaf, pos_dict)

        # update all nodes from root to leaf with given result in position dictionary 
        pos_dict = backpropagate(path, result, pos_dict)
            
        curr_iter += 1
    
    best_pos = None

    # choose best move based on ucb 
    total = pos_dict[pos][0]
    player = pos.next_player()

    # choose best move based on average reward:
    best_pos_avg = 0
    for next_move in pos.legal_moves():
        # since pos.result creates new object, and we cannot reference it in dictionary,
        # find its equivalent one already in dictionary (memory reference issues)
        next_pos = object_in_pos_dict(pos.result(next_move), pos_dict)
        # if haven't visited before, choose it 
        if pos_dict[next_pos][0] == 0:
            return next_pos
        else:
            avg = pos_dict[next_pos][1] / pos_dict[next_pos][0]
            # if yellow then we chooes max average reward 
            if not player:
                if best_pos == None or avg > best_pos_avg:
                    best_pos = next_pos
                    best_pos_avg = avg
            # if red then we choose min average reward
            else:
                if best_pos == None or avg < best_pos_avg:
                    best_pos = next_pos
                    best_pos_avg = avg

    return best_pos

def ucb_select(pos, pos_dict, path):
    ''' Traverses game tree by recursively selecting best (highest/lowest UCB value) child node of current position that
        we can roll out/return terminal node. 

        pos -- Connect 4 position (2D array)
        pos_dict -- dictionary of Connect 4 positions and [visits, total reward]
        path -- current path of traversal in list format 
    '''
    player = pos.next_player()
    total = pos_dict[pos][0]
    
    # add current position we traversed to
    path.append(pos)

    # if position is terminal node, then return 
    if pos.game_over():
        return pos, path
    elif is_leaf(pos, pos_dict):
        # if 0 visits, then want to roll it out
        if pos_dict[pos][0] == 0:
            return pos, path 
        # want to expand the node and roll out its first child 
        else:
            for next_move in pos.legal_moves():
                next_pos = pos.result(next_move)
                pos_dict[next_pos] = [0, 0]

            first_next_pos = object_in_pos_dict(pos.result(pos.legal_moves()[0]), pos_dict)
            path.append(first_next_pos)

            return first_next_pos, path
    else:
        best_pos = None

        for next_move in pos.legal_moves():
            next_pos = object_in_pos_dict(pos.result(next_move), pos_dict)
            # if a child node is unvisited, then we want that one to be leaf, since its ucb is infinite 
            if pos_dict[next_pos][0] == 0:
                path.append(next_pos)
                return next_pos, path
            # calculate ucb
            else:
                next_pos_ucb = ucb(next_pos, pos_dict, total, player)
                # if player 0's turn, then we want to get the max of its children
                if not player: 
                    if best_pos == None or next_pos_ucb > ucb(best_pos, pos_dict, total, player):
                        best_pos = next_pos
                # if player 1's turn then we want to get min of children 
                else:
                    if best_pos == None or next_pos_ucb < ucb(best_pos, pos_dict, total, player):
                        best_pos = next_pos
        
        return ucb_select(best_pos, pos_dict, path)

            
def is_leaf(pos, pos_dict):
    ''' Returns whether current position is a leaf node.

        pos -- Kalah position
        posDict -- dictionary of Kalah position and [visits, total reward]
    '''
    for next_move in pos.legal_moves():
        next_pos = object_in_pos_dict(pos.result(next_move), pos_dict)
        # if a child node of curr pos is not in dictionary, then we haven't expanded it yet, so it's a leaf 
        if next_pos == None:
            return True

    return False

def ucb(pos, pos_dict, total, player):
    ''' Calculates and returns ucb value of position.

        pos -- Kalah position
        posDict -- dictionary of Kalah position and [visits, total reward]
        total -- parent node's total visits
        player -- next_player of parent node, which will determine how we calculate ucb 
    '''
    visits = pos_dict[pos][0]
    total_reward = pos_dict[pos][1]
    # if player 0's turn, then want to maximize ucb with adding the exploration 
    if not player:
        return (total_reward / visits) + (2*math.log(total) / visits)**0.5
    # if player 1's turn, then want to minimize ucb with subtracting exploration 
    else:
        return (total_reward / visits) - (2*math.log(total) / visits)**0.5

def backpropagate(path, result, pos_dict):
    ''' Updates all nodes in path with result and incrementing visit count 

        path -- path of traversing from root to leaf 
        result -- -1/0/1 score after rolling out from leaf 
        posDict -- dictionary of Kalah position and [visits, total reward]
    '''
    for pos in path:
        # update count 
        pos_dict[pos][0] += 1
        # update total reward 
        pos_dict[pos][1] += result
            
    return pos_dict

def rollout(pos, pos_dict):
    ''' Traverses tree to terminal node with all random moves and returns result of terminal node.

        pos -- Kalah position
    '''
    while not pos.game_over():
        pos = pos.result(get_random_move(pos))

    return pos.winner()

def get_random_move(pos):
    ''' Returns a random move to make from legal moves of current position.
        pos -- Kalah position
    '''
    return random.choice(pos.legal_moves())

def print_2d_array(arr, num_rows, num_cols):
    for row in range(num_rows):
        for col in range(num_cols):
            print(arr[row][col], end=' ')
        print()
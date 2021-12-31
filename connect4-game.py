import numpy as np
import pygame
import sys
import math
from mcts import mcts
from connect4 import Connect4

NUM_ROWS = 6
NUM_COLS = 7
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 - 5)


def draw_board(board):
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            pygame.draw.rect(screen, BLUE, (col*SQUARE_SIZE, SQUARE_SIZE + row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (col*SQUARE_SIZE + SQUARE_SIZE/2, SQUARE_SIZE + row*SQUARE_SIZE + SQUARE_SIZE/2), RADIUS)

    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, YELLOW, (col*SQUARE_SIZE + SQUARE_SIZE/2, SQUARE_SIZE + row*SQUARE_SIZE + SQUARE_SIZE/2), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, RED, (col*SQUARE_SIZE + SQUARE_SIZE/2, SQUARE_SIZE + row*SQUARE_SIZE + SQUARE_SIZE/2), RADIUS)

def valid_selection(col, board):
    return board[0][col] == 0

def drop_piece(col, board, turn):
    # start from bottom row of list, and find first empty hole 
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = turn + 1
            break

def print_2d_array(arr, num_rows, num_cols):
    for row in range(num_rows):
        for col in range(num_cols):
            print(arr[row][col], end=' ')
        print()

pygame.init()

width = NUM_COLS*SQUARE_SIZE
height = (NUM_ROWS + 1)*SQUARE_SIZE

# Set up the drawing window
screen = pygame.display.set_mode((width, height))

game_over = False
ai_turn = int(input("Would you like to play first (0) or second (1)? "))
board =[[0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0]]

pos = Connect4(board, 0)

while not game_over:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw_board(pos.board)

    # Update the display
    pygame.display.update()

    if ai_turn == 0:
        making_turn = True
        while making_turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    x = mouse_pos[0]
                    y = mouse_pos[1]

                    if y >= SQUARE_SIZE:
                        if x >= 0 and x < SQUARE_SIZE:
                            col = 0
                        elif x >= SQUARE_SIZE and x < 2*SQUARE_SIZE:
                            col = 1
                        elif x >= 2*SQUARE_SIZE and x < 3*SQUARE_SIZE:
                            col = 2
                        elif x >= 3*SQUARE_SIZE and x < 4*SQUARE_SIZE:
                            col = 3
                        elif x >= 4*SQUARE_SIZE and x < 5*SQUARE_SIZE:
                            col = 4
                        elif x >= 5*SQUARE_SIZE and x < 6*SQUARE_SIZE:
                            col = 5
                        elif x >= 6*SQUARE_SIZE and x < 7*SQUARE_SIZE:
                            col = 6
        
                        if valid_selection(col, pos.board):
                            # change 2-D array board 
                            drop_piece(col, pos.board, pos.turn)

                            if pos.game_over():
                                draw_board(pos.board)

                                font = pygame.font.Font('freesansbold.ttf', 32)
                                if pos.game_over() == 2:
                                    text = font.render('Draw!', True, WHITE, BLACK)
                                else:
                                    text = font.render('You won!', True, WHITE, BLACK)
                                text_rect = text.get_rect()
                                text_rect.center = (NUM_COLS*SQUARE_SIZE/2, SQUARE_SIZE/2)
                                screen.blit(text, text_rect)     

                                # Update the display
                                pygame.display.update()

                                # nothing to do after game over except close window 
                                while True:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()

                            ai_turn = 1
                            pos.turn = 1 - pos.turn
                            making_turn = False
                        else:
                            print("Invalid move")
        
    # AI turn 
    else:
        next_connect4_pos = mcts(1000, pos)
        pos = next_connect4_pos

        if pos.game_over():
            font = pygame.font.Font('freesansbold.ttf', 32)

            if pos.game_over() == 2:
                text = font.render('Draw', True, WHITE, BLACK)
            else:
                text = font.render('You lost!', True, WHITE, BLACK)

            # create a rectangular object for the
            # text surface object
            text_rect = text.get_rect()
            
            # set the center of the rectangular object.
            text_rect.center = (NUM_COLS*SQUARE_SIZE/2, SQUARE_SIZE/2)

            # copying the text surface object to the display surface object at the center coordinate.
            screen.blit(text, text_rect)            
            
            draw_board(pos.board)

            # Update the display
            pygame.display.update()

            # nothing to do after game over except close window 
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

        # uncomment this to see AI vs AI
        ai_turn = 0

    draw_board(pos.board)

    # Update the display
    pygame.display.update()


import numpy as np
import random
import pygame
import sys
import math
import time

BLUE = (0,0,255)
BLACK = (10,10,10)
WHITE=(255,255,255)
GRAY = (30,30,30)
Lite_Green = (160, 209, 112)
Lite_Blue = (140 , 215, 238)
Green = (30, 110, 53)
Blue = (0 , 32, 96)

NUM_OF_ROWS = 6
NUM_OF_COLUMNS = 7

EMPTY_PLACE = 0
PLAYER_PIECE = 1
AI_PIECE = 2

SLICE_LEN = 4 #used for slicing the board to compute the Heuristics

pygame.init()

#button class
class button():
    def __init__(self,color,x_pos,y_pos,width,height,text=''):
        self.color=color
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.width=width
        self.height=height
        self.text=text
        self.draw_button(screen)
    def draw_button(self,screen):
        # this metiod draw the button on home screen

        pygame.draw.rect(screen,(0,0,0),(self.x_pos-2,self.y_pos-2,self.width+4,self.height+4),0)
        pygame.draw.rect(screen,self.color,(self.x_pos,self.y_pos,self.width,self.height),0)
        if self.text!='':
            font=pygame.font.Font("RAVIE.TTF",41)
            text=font.render(self.text, True, BLACK)
            screen.blit(text,(self.x_pos+(self.width/2-text.get_width()/2),self.y_pos+(self.height/2-text.get_height()/2)))
    def isover(self,pos):
        if pos[0]>self.x_pos and pos[0]<self.x_pos + self.width:
            if pos[1]>self.y_pos and pos[1]< self.y_pos +self.height:
                return True
    def isclick(self,pos):
        if self.isover(pos) and pygame.mouse.get_pressed()[0] == True:
            self.color=(0,128,128)
            self.draw_button(screen)
            pygame.display.update()
            time.sleep(0.1)
            pygame.draw.rect(screen, GRAY, (0, 0, width_of_screen, 100))
            return True

background = pygame.image.load('Untitled.jpg')#background loading
icon = pygame.image.load('icon.jpg')#icon loading
pygame.display.set_icon(icon)
pygame.display.set_caption("Connect 4")#game name
depth = 0 #depth of minimax ; to select the hardness
hardness_selected = False # flag to know is the hardness selected or not
hardness_level = 0 # 1-> easy 2->normal 3->Hard

Cell_size = 100

#each cell will have a 100 * 100 px
width_of_screen = 700
height_of_screen = 700

RADIUS = int(Cell_size / 2 - 4)

screen = pygame.display.set_mode((width_of_screen, height_of_screen))

myfont = pygame.font.Font("RAVIE.TTF",75)

myfont2 = pygame.font.Font("RAVIE.TTF",55)


def create_board():
    arr = [[0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0]]
    # arr = [[1,2,1,2,1,2,0],#drawing
    #        [1,2,1,2,1,2,1],
    #        [1,2,1,2,1,2,1],
    #        [2,1,2,1,2,1,2],
    #        [2,1,2,1,2,1,2],
    #        [2,1,2,1,2,1,2]]
    # global turn
    # turn = PLAYER_PIECE
    board = np.array(arr)
    return np.flip(board,axis=0)

def show_board():
    screen.blit(background, (0, 100))
    for col in range(NUM_OF_COLUMNS):
        for row in range(NUM_OF_ROWS):
            pygame.draw.circle(screen, BLACK, (int(col * Cell_size + Cell_size / 2), int(row * Cell_size + Cell_size + Cell_size / 2)), RADIUS)

    pygame.display.update()

def fill_board(board):

    for col in range(NUM_OF_COLUMNS):
        for row in range(NUM_OF_ROWS):
            if board[row][col] == PLAYER_PIECE:
                pygame.draw.circle(screen, Lite_Green, (int(col * Cell_size + Cell_size / 2), height_of_screen - int(row * Cell_size + Cell_size / 2)), RADIUS)
                pygame.draw.circle(screen, Green, (int(col * Cell_size + Cell_size / 2), height_of_screen - int(row * Cell_size + Cell_size / 2)), RADIUS - 8)

            elif board[row][col] == AI_PIECE:
                pygame.draw.circle(screen, Lite_Blue, (int(col * Cell_size + Cell_size / 2), height_of_screen - int(row * Cell_size + Cell_size / 2)), RADIUS)
                pygame.draw.circle(screen, Blue, (int(col * Cell_size + Cell_size / 2), height_of_screen - int(row * Cell_size + Cell_size / 2)), RADIUS - 8)

    pygame.display.update()

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_available_col(board, col):
    list = board.tolist()
    return list[NUM_OF_ROWS - 1][col] == EMPTY_PLACE

def get_available_cols(board):
    valid_locations = []
    for col in range(NUM_OF_COLUMNS):
        if is_available_col(board, col):
            valid_locations.append(col)
    return valid_locations

def get_next_open_row(board, col):
    for r in range(NUM_OF_ROWS):
        if board[r][col] == EMPTY_PLACE:
            return r

def is_winning(board, piece):
    # Check if we have four pieces in one row
    for row in range(NUM_OF_ROWS):
        for col in range(NUM_OF_COLUMNS - 3):
            count = 0
            for i in range(0,4):
                if board[row][col+i] == piece:
                    count += 1
            if count == 4:
                return True

    # Check if we have four pieces in one col
    for col in range(NUM_OF_COLUMNS):
        for row in range(NUM_OF_ROWS - 3):
            count = 0
            for i in range(0,4):
                if board[row+i][col] == piece:
                    count += 1
            if count == 4:
                return True

    # Check if we have four pieces in one +ve diagaonl
    for row in range(NUM_OF_ROWS - 3):
        for col in range(NUM_OF_COLUMNS - 3):
            count = 0
            for i in range(0,4):
                if board[row+i][col+i] == piece:
                    count += 1
            if count == 4:
                return True

    # Check if we have four pieces in one -ve diagaonl
    for row in range(NUM_OF_ROWS - 1, NUM_OF_ROWS - 4, -1):
        for col in range(NUM_OF_COLUMNS - 3):
            count = 0
            for i in range(0,4):
                if board[row-i][col+i] == piece:
                    count += 1
            if count == 4:
                return True

def is_drawing(board):
    if is_winning(board, AI_PIECE) or is_winning(board,PLAYER_PIECE):
        return False

    for row in range(NUM_OF_ROWS):
        for col in range(NUM_OF_COLUMNS):
            if board[row][col] == EMPTY_PLACE:
                return False

    return True

def slice_score(slice):
    score = 0

    if len(slice) == 5:
        if slice.count(AI_PIECE) == 3 and slice[0] == EMPTY_PLACE and slice[4] == EMPTY_PLACE:
            return  1000
        if slice.count(PLAYER_PIECE) == 3 and slice[0] == EMPTY_PLACE and slice[4] == EMPTY_PLACE:
            return -1000
    if slice.count(AI_PIECE) == 3 and slice.count(EMPTY_PLACE) == 1:
        return 20
    if slice.count(AI_PIECE) == 2 and slice.count(EMPTY_PLACE) == 2:
        return 15
    if slice.count(PLAYER_PIECE) == 3 and slice.count(EMPTY_PLACE) == 1:
        return -25
    if slice.count(PLAYER_PIECE) == 2 and slice.count(EMPTY_PLACE) == 2:
        return -20
    return score

def Heuristic_center_column(board):
    ## Score center column
    score = 0
    center_array = [int(i) for i in list(board[:, 3])]
    center_count = center_array.count(AI_PIECE)
    score += center_count * 4
    return score

def Heuristic_rows(board):
    one_row = []
    score = 0
    for row in range(NUM_OF_ROWS):
        for i in list(board[row,:]):
            one_row.append(i)
        for col in range(NUM_OF_COLUMNS - 3):
            slice = one_row[col:col + SLICE_LEN]
            score += slice_score(slice)
        one_row.clear()
    return score

def Heuristic_cols(board):
    one_col = []
    score = 0
    for col in range(NUM_OF_COLUMNS):
        for i in list(board[:,col]):
            one_col.append(i)
        for row in range(NUM_OF_ROWS - 3):
            slice = one_col[row:row + SLICE_LEN]
            score += slice_score(slice)
        one_col.clear()
    return score

def Heuristic_pos_diag(board):
    one_pos_diagonal = []
    score = 0
    for row in range(NUM_OF_ROWS - 3):
        for col in range(NUM_OF_COLUMNS - 3):
            for i in range(SLICE_LEN):
                one_pos_diagonal.append(board[row+i][col+i])
            slice = one_pos_diagonal
            score += slice_score(slice)
            one_pos_diagonal.clear()
    return score

def Heuristic_neg_diag(board):
    score = 0
    for row in range(NUM_OF_ROWS - 1, NUM_OF_ROWS - 4, -1):
        one_neg_diagonal = []
        for col in range(NUM_OF_COLUMNS - 3):
            for i in range(SLICE_LEN):
                one_neg_diagonal.append(board[row-i][col+i])
            slice = one_neg_diagonal
            score += slice_score(slice)
    return score

def Heuristic_put_into_checkmate_rows(board):
    score = 0
    if(hardness_level == 3):
        one_row = []
        #Check if we have a 5 len slice that make the following -> (0 1 1 1 0) or (0 2 2 2 0) in row
        for row in range(NUM_OF_ROWS):
            for i in list(board[row,:]):
                one_row.append(i)
            for col in range(NUM_OF_COLUMNS - 4):
                slice = one_row[col:col + SLICE_LEN + 1]#SLICE_LEN + 1 ;becuse we need the slice to be 5 places
                score += slice_score(slice)
            one_row.clear()
    return score

def Heuristic_put_into_checkmate_pos_diag(board):
    score = 0
    if(hardness_level == 3):
        one_pos_diagonal = []
        #Check if we have a 5 len slice that make the following -> (0 1 1 1 0) or (0 2 2 2 0) +ve diag
        for row in range(NUM_OF_ROWS - 4):
            for col in range(NUM_OF_COLUMNS - 4):
                for i in range(SLICE_LEN + 1):
                    one_pos_diagonal.append(board[row+i][col+i])
                slice = one_pos_diagonal
                score += slice_score(slice)
                one_pos_diagonal.clear()
    return score

def Heuristic_put_into_checkmate_neg_diag(board):
    score = 0
    if(hardness_level == 3):
        one_neg_diagonal = []
        #Check if we have a 5 len slice that make the following -> (0 1 1 1 0) or (0 2 2 2 0) -ve diag
        for row in range(NUM_OF_ROWS - 1, NUM_OF_ROWS - 3, -1):
            for col in range(NUM_OF_COLUMNS - 4):
                for i in range(SLICE_LEN + 1):
                    one_neg_diagonal.append(board[row-i][col+i])
                slice = one_neg_diagonal
                score += slice_score(slice)
                one_neg_diagonal.clear()
    return score

def total_heuristics_score(board):
    score = Heuristic_center_column(board) + Heuristic_rows(board) + Heuristic_cols(board) + Heuristic_pos_diag(board) + Heuristic_neg_diag(board) + Heuristic_put_into_checkmate_rows(board) + Heuristic_put_into_checkmate_pos_diag(board) + Heuristic_put_into_checkmate_neg_diag(board)
    return score

def is_terminal_node(board):
    return is_winning(board, PLAYER_PIECE) or is_winning(board, AI_PIECE) or is_drawing(board)

def minimax(board, depth, alpha, beta, maximizingPlayer):
    available_cols = get_available_cols(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if is_winning(board, AI_PIECE):
                return (None, math.inf)
            elif is_winning(board, PLAYER_PIECE):
                return (None, -math.inf)
            else: # Drawing case
                return (None, 0)
        else: # Depth is zero
            return (None, total_heuristics_score(board))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(available_cols)
        for col in available_cols:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            if value > alpha:
                alpha = value
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(available_cols)
        for col in available_cols:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            if value < beta:
                beta = value
            if alpha >= beta:
                break
        return column, value

turn = random.randint(PLAYER_PIECE, AI_PIECE)

board = create_board()
show_board()
fill_board(board)

if not hardness_selected :
    left_button=button((50,205,50),20+10,5,200,90,"Easy")
    center_button=button((255,215,0),240+10,5,200,90,"Normal")
    right_button=button((139,0,0),460+10,5,200,90,"Evil !")
    pygame.display.update()

game_over = False

while True:
    for event in pygame.event.get():
        if not hardness_selected:
            pos=pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if left_button.isclick(pos):
                    depth = 1
                    hardness_selected = True
                    continue
                if center_button.isclick(pos):
                    depth = 3
                    hardness_selected = True
                    continue
                if right_button.isclick(pos):
                    depth = 5
                    hardness_selected = True
                    continue

        elif not game_over:
            pygame.draw.rect(screen, GRAY, (0, 0, width_of_screen, 100))
            X_pos=pygame.mouse.get_pos()[0]
            if turn == PLAYER_PIECE:
                pygame.draw.circle(screen, Lite_Green, (X_pos, int(Cell_size / 2)), RADIUS)
                pygame.draw.circle(screen, Green, (X_pos, int(Cell_size / 2)), RADIUS - 8)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, GRAY, (0, 0, width_of_screen, 100))
                # Ask for Player 1 Input
                if turn == PLAYER_PIECE:
                    X_pos = pygame.mouse.get_pos()[0]
                    col = int(math.floor(X_pos / Cell_size))
                    if is_available_col(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if is_winning(board, PLAYER_PIECE):
                            label = myfont2.render("You beat the AI !!", True, WHITE)
                            screen.blit(label, (20,30))
                            game_over = True

                        if is_drawing(board):
                            label = myfont2.render("It's a Draw !!!", True, WHITE)
                            screen.blit(label, (100,30))
                            game_over = True

                        turn = AI_PIECE

                        fill_board(board)

        if event.type == pygame.QUIT:
            sys.exit()

    if turn == AI_PIECE and not game_over and hardness_selected:

        col, minimax_score = minimax(board, depth, -math.inf, math.inf, True)
        row = get_next_open_row(board, col)
        
        drop_piece(board, row, col, AI_PIECE)

        if is_winning(board, AI_PIECE):
            label = myfont.render("AI wins!!", True, WHITE)
            screen.blit(label, (136,17))
            game_over = True

        if is_drawing(board):
            label = myfont2.render("It's a Draw !!!", True, WHITE)
            screen.blit(label, (100,30))
            game_over = True

        fill_board(board)

        turn = PLAYER_PIECE
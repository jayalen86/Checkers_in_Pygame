import pygame
from tkinter import *
from tkinter import messagebox

pygame.init()
pygame.display.set_caption('Checkers')
pygame.display.set_icon(pygame.image.load('images/checkersicon.png'))
screen_height = 640
screen_width = 640
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game_running = True
piece_to_move = None
double_jump_piece = None
current_turn = 'Red'
adversary = 'Black'
extra_jumps = []
gameover = False
grid = [
        ['B_','E_','B_','E_','B_','E_','B_','E_'],
        ['E_','B_','E_','B_','E_','B_','E_','B_'],
        ['B_','E_','B_','E_','B_','E_','B_','E_'],
        ['E_','E_','E_','E_','E_','E_','E_','E_'],
        ['E_','E_','E_','E_','E_','E_','E_','E_'],
        ['E_','R_','E_','R_','E_','R_','E_','R_'],
        ['R_','E_','R_','E_','R_','E_','R_','E_'],
        ['E_','R_','E_','R_','E_','R_','E_','R_'],
    ]
axises = [[[0, 0], [80, 0], [160, 0], [240, 0], [320, 0], [400, 0], [480, 0], [560, 0]],
          [[0, 80], [80, 80], [160, 80], [240, 80], [320, 80], [400, 80], [480, 80], [560, 80]],
          [[0, 160], [80, 160], [160, 160], [240, 160], [320, 160], [400, 160], [480, 160], [560, 160]],
          [[0, 240], [80, 240], [160, 240], [240, 240], [320, 240], [400, 240], [480, 240], [560, 240]],
          [[0, 320], [80, 320], [160, 320], [240, 320], [320, 320], [400, 320], [480, 320], [560, 320]],
          [[0, 400], [80, 400], [160, 400], [240, 400], [320, 400], [400, 400], [480, 400], [560, 400]],
          [[0, 480], [80, 480], [160, 480], [240, 480], [320, 480], [400, 480], [480, 480], [560, 480]],
          [[0, 560], [80, 560], [160, 560], [240, 560], [320, 560], [400, 560], [480, 560], [560, 560]]]

def get_grid_row_col(position):
    for x, val in enumerate(axises):
        for y, val2 in enumerate(val):
            if position[0] >= val2[0] and position[0] <= val2[0]+80:
                if position[1] >= val2[1] and position[1] <= val2[1] +80:
                    return x, y, val2

def draw_grid():
    x_axis = 0
    y_axis = -80
    colors = [(0,0,0),(210,180,140),(0,0,0),(210,180,140),
              (0,0,0),(210,180,140),(0,0,0),(210,180,140)]
    #draws board & pieces
    for row, val in enumerate(grid):
        x_axis = 0
        y_axis += 80
        color = colors[row]
        for col, val2 in enumerate(val):
            pygame.draw.rect(screen, color, (x_axis, y_axis, 80, 80), 0)
            if grid[row][col][0] == 'R':
                pygame.draw.circle(screen, (255,0,0), [x_axis+40, y_axis+40], 30, 0)
                if grid[row][col][1] == 'K':
                    pygame.draw.circle(screen, (255,255,0), [x_axis+40, y_axis+40], 31, 4)
            elif grid[row][col][0] == 'B':
                pygame.draw.circle(screen, (255,255,255), [x_axis+40, y_axis+40], 30, 0)
                if grid[row][col][1] == 'K':
                    pygame.draw.circle(screen, (255,255,0), [x_axis+40, y_axis+40], 31, 4)
            else:
                pass
            color = (210,180,140) if color == (0,0,0) else (0,0,0) 
            x_axis += 80

    #highlights currently selected checker
    if piece_to_move:
       pygame.draw.circle(screen, (0,255,0), [piece_to_move[1]+40, piece_to_move[2]+40], 30, 1)

    #draws blue rectangles around possible double jumps
    for item in extra_jumps:
        x_axis = axises[item[0]][item[1]][0]
        y_axis = axises[item[0]][item[1]][1]
        pygame.draw.rect(screen, (0,0,255), (x_axis, y_axis, 80, 80), 1)
    pygame.display.update()
    return
    
def check_up_left(oldrow, oldcol, row, col):
    if oldrow-1 == row and oldcol-1 == col:
        if grid[row][col] == 'E_':
            return 'NJ'
    elif oldrow-2 == row and oldcol-2 == col:
        if grid[oldrow-1][oldcol-1][0] == adversary[0]:
            if grid[row][col] == 'E_':
                grid[oldrow-1][oldcol-1] = 'E_'
                return 'SJ'
    return False

def check_up_right(oldrow, oldcol, row, col):
    if oldrow-1 == row and oldcol+1 == col:
        if grid[row][col] == 'E_':
            return 'NJ'
    elif oldrow-2 == row and oldcol+2 == col:
        if grid[oldrow-1][oldcol+1][0] == adversary[0]:
            if grid[row][col] == 'E_':
                grid[oldrow-1][oldcol+1] = 'E_'
                return 'SJ'
    return False

def check_down_left(oldrow, oldcol, row, col):
    if oldrow+1 == row and oldcol-1 == col:
        if grid[row][col] == 'E_':
            return 'NJ'
    elif oldrow+2 == row and oldcol-2 == col:
        if grid[oldrow+1][oldcol-1][0] == adversary[0]:
            if grid[row][col] == 'E_':
                grid[oldrow+1][oldcol-1] = 'E_'
                return 'SJ'
    return False

def check_down_right(oldrow, oldcol, row, col):
    if oldrow+1 == row and oldcol+1 == col:
        if grid[row][col] == 'E_':
            return 'NJ'
    elif oldrow+2 == row and oldcol+2 == col:
        if grid[oldrow+1][oldcol+1][0] == adversary[0]:
            if grid[row][col] == 'E_':
                grid[oldrow+1][oldcol+1] = 'E_'
                return 'SJ'
    return False

def check_double_jump_up(row, col):
    jumps = []
    try:
        if grid[row-1][col-1][0] == adversary[0]:
            if grid[row-2][col-2] == 'E_':
                jumps.append([row-2,col-2])
    except:
        pass
    try:
        if grid[row-1][col+1][0] == adversary[0]:
            if grid[row-2][col+2] == 'E_':
                jumps.append([row-2,col+2])
    except:
        pass
    for x in jumps:
        if (x[0] < 0  or x[0] > 7) or (x[1] < 0 or x[1] > 7):
            jumps.remove(x)
    return jumps

def check_double_jump_down(row, col):
    jumps = []
    try:
        if grid[row+1][col-1][0] == adversary[0]:
            if grid[row+2][col-2] == 'E_':
                jumps.append([row+2,col-2])
    except:
        pass
    try:
        if grid[row+1][col+1][0] == adversary[0]:
            if grid[row+2][col+2] == 'E_':
                jumps.append([row+2,col+2])
    except:
        pass
    for x in jumps:
        if (x[0] < 0  or x[0] > 7) or (x[1] < 0 or x[1] > 7):
            jumps.remove(x)
    return jumps

def remove_piece(row, col, oldrow, oldcol):
    if row < oldrow and col < oldcol:
        grid[oldrow-1][oldcol-1] = 'E_'
    elif row < oldrow and col > oldcol:
        grid[oldrow-1][oldcol+1] = 'E_'
    elif row > oldrow and col < oldcol:
        grid[oldrow+1][oldcol-1] = 'E_'
    elif row > oldrow and col > oldcol:
        grid[oldrow+1][oldcol+1] = 'E_'
    return

def check_king_piece():
    for x, val in enumerate(grid[0]):
        if val[0] == 'R' and val[1] == '_':
            grid[0][x] = 'RK'
    for x, val in enumerate(grid[7]):
        if val[0] == 'B' and val[1] == '_':
            grid[7][x] = 'BK'
    return

def check_game_over():
    red, black = False, False
    for x in grid:
        for y in x:
            if y[0] == 'R':
                red = True
            if y[0] == 'B':
                black = True
    return [red, black]

def reset(color):
    Tk().wm_withdraw() #Prevents a second TKinter window from popping up
    msg = messagebox.askyesno(color+" wins!", "Would you like to play again?")
    if msg == True:
        global grid, piece_to_move, double_jump_piece, current_turn, adversary, gameover
        piece_to_move = None
        double_jump_piece = None
        current_turn = 'Red'
        adversary = 'Black'
        del extra_jumps[:]
        gameover = False
        grid = [
        ['B_','E_','B_','E_','B_','E_','B_','E_'],
        ['E_','B_','E_','B_','E_','B_','E_','B_'],
        ['B_','E_','B_','E_','B_','E_','B_','E_'],
        ['E_','E_','E_','E_','E_','E_','E_','E_'],
        ['E_','E_','E_','E_','E_','E_','E_','E_'],
        ['E_','R_','E_','R_','E_','R_','E_','R_'],
        ['R_','E_','R_','E_','R_','E_','R_','E_'],
        ['E_','R_','E_','R_','E_','R_','E_','R_'],]
    else:
        pygame.quit()
        global game_running
        game_running = False
    return
        
            
def check_if_double_jump(UL, UR, DL, DR, row, col, oldrow, oldcol):
    double_jump_piece = None
    if UL or UR or DL or DR:
        grid[row][col] = grid[oldrow][oldcol]
        grid[oldrow][oldcol] = 'E_'
        if (UL == 'SJ' or UR == 'SJ' or DL == 'SJ' or DR == 'SJ') and piece_to_move[0][1] == 'K':
            possible_double_jumps = check_double_jump_up(row, col) + check_double_jump_down(row, col)
            for item in possible_double_jumps:
                extra_jumps.append(item)
                double_jump_piece = [grid[row][col], row, col]
        elif UL == 'SJ' or UR == 'SJ':
            possible_double_jumps = check_double_jump_up(row, col)
            for item in possible_double_jumps:
                extra_jumps.append(item)
                double_jump_piece = [grid[row][col], row, col]
        elif DL == 'SJ' or DR == 'SJ':
            possible_double_jumps = check_double_jump_down(row, col)
            for item in possible_double_jumps:
                extra_jumps.append(item)
                double_jump_piece = [grid[row][col], row, col]
        #switches turn if not any possible double jumps
        if len(extra_jumps) == 0:
            global adversary, current_turn
            adversary = 'Red' if adversary == 'Black' else 'Black'
            current_turn = 'Red' if current_turn == 'Black' else 'Black'
    return double_jump_piece

while game_running:
    clock.tick(10)
    #key strokes
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            game_running = False
    if game_running == False:
        break
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        position = pygame.mouse.get_pos()
        square = get_grid_row_col(position)
        row, col = square[0], square[1] 
        if piece_to_move and len(extra_jumps) == 0:
            UL, UR, DL, DR = False, False, False, False
            oldrow, oldcol  = piece_to_move[3], piece_to_move[4]
            if piece_to_move[0][1] == 'K':
                UL = check_up_left(oldrow, oldcol, row, col)
                UR = check_up_right(oldrow, oldcol, row, col)
                DL = check_down_left(oldrow, oldcol, row, col)
                DR = check_down_right(oldrow, oldcol, row, col)
            elif current_turn == 'Red':
                UL = check_up_left(oldrow, oldcol, row, col)
                UR = check_up_right(oldrow, oldcol, row, col)
            elif current_turn == 'Black':
                DL = check_down_left(oldrow, oldcol, row, col)
                DR = check_down_right(oldrow, oldcol, row, col)
            double_jump_piece = check_if_double_jump(UL, UR, DL, DR, row, col, oldrow, oldcol)
            piece_to_move = None

        elif len(extra_jumps) > 0:
            oldrow, oldcol  = double_jump_piece[1], double_jump_piece[2]
            if [row, col] in extra_jumps:
                remove_piece(row, col, oldrow, oldcol)
                grid[row][col] = grid[oldrow][oldcol]
                grid[oldrow][oldcol] = 'E_'
                del extra_jumps[:]
                if double_jump_piece[0][1] == 'K':
                    possible_jumps = check_double_jump_up(row, col)+ check_double_jump_down(row, col)
                elif current_turn == 'Red':
                    possible_jumps = check_double_jump_up(row, col)
                elif current_turn == 'Black':
                    possible_jumps = check_double_jump_down(row, col)

                if possible_jumps:
                    for square in possible_jumps:
                        extra_jumps.append(square)
                    double_jump_piece = [grid[row][col], row, col]
                else:
                    double_jump_piece  = None
                    adversary = 'Red' if adversary == 'Black' else 'Black'
                    current_turn = 'Red' if current_turn == 'Black' else 'Black'  
        else:
            coordinates = square[2]
            if grid[row][col][0] == current_turn[0]:
                piece_to_move = [grid[row][col], coordinates[0], coordinates[1], row, col]
            else:
                piece_to_move = None

    check_king_piece()
    players = check_game_over()
    
    if (players[0] == False or players[1] == False) and gameover == False:
        color = 'Black' if players[0] == False else 'Red'
        draw_grid()
        gameover = True
        reset(color)
    else:
        draw_grid()

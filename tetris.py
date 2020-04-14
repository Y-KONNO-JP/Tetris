# -*- coding: utf-8 -*-
"""
@author: phd_mech
"""

import os
import sys
import glob
import random
import time
import numpy as np
import cv2

def read_img(file_list, extension):
    """
    SAVE IMAGE FILE
    """
    img_list = []
    for file_id in file_list:
        if extension in file_id:
            img = cv2.imread(file_id)
            img_list.append(img)
    return img_list

def binary(img):
    """
    BGR => BINARY
    """
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary_img = cv2.threshold(gray_img, 1, 1, cv2.THRESH_BINARY)[1]
    return binary_img

def level():
    """
    FALL SPEED
    """
    global LEVEL
    ref_score = REFERENCE_SCORE[LEVEL-1]
    timer = TIMER_TABLE[LEVEL-1]
    if SCORE >= ref_score:
        LEVEL += 1
    return timer

def future_mino_box():
    """
    DRAW FUTURE MINO BOX
    """
    minos_box = np.ones([22, 7, 3], dtype=np.uint8)*255
    minos_box[1:-1, 1:-1] = np.zeros([20, 5, 3], dtype=np.uint8)
    for i in range(4):
        d_h = i*5
        mino_height = MINO_FUTURE[i].shape[0]
        mino_width = MINO_FUTURE[i].shape[1]
        minos_box[2+d_h:2+d_h+mino_height, 2:2+mino_width] += MINO_FUTURE[i]
    return minos_box

def board_show(board, script):
    """
    DRAW MAIN BOARD
    """
    # MAIN BOARD
    board_height = board.shape[0]
    board_width = board.shape[1]
    board[0, 4:-4] = 0
    # EXPAND BOARD
    board_expand = np.zeros([board_height, board_width+10, 3], dtype=np.uint8)
    board_expand[:, 0:board_width] = board
    magnification1 = 4
    board_expand = cv2.resize(board_expand,
                              dsize=None,
                              fx=magnification1,
                              fy=magnification1,
                              interpolation=cv2.INTER_AREA)
    # FUTURE MINO
    x_pos, y_pos = 48, 0
    box = future_mino_box()[:]
    box_height = box.shape[0]
    box_width = box.shape[1]
    board_expand[y_pos:y_pos+box_height, x_pos:x_pos+box_width] = box
    magnification2 = 9
    board_expand = cv2.resize(board_expand,
                              dsize=None,
                              fx=magnification2,
                              fy=magnification2,
                              interpolation=cv2.INTER_AREA)
    # SCRIPT
    if script is not None:
        cv2.rectangle(board_expand, (36, 355), (395, 375), (0, 200, 255), -1)
        cv2.rectangle(board_expand, (36, 375), (395, 420), (255, 255, 255), -1)
        cv2.rectangle(board_expand, (36, 420), (395, 440), (0, 200, 255), -1)
        cv2.putText(board_expand, script,
                    (60, 413), cv2.FONT_HERSHEY_SIMPLEX,
                    1.5, (100, 0, 255), 2, cv2.LINE_AA)
    # GAME INFORMATION
    y_tex = 240
    cv2.putText(board_expand, "@ Level",
                (435, y_tex), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "@ Lines",
                (435, y_tex+30*1), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "@ Score",
                (435, y_tex+30*2), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "@ Turn",
                (435, y_tex+30*3), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(board_expand, str(LEVEL),
                (580, y_tex), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(board_expand, str(LINES),
                (580, y_tex+30*1), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(board_expand, str(SCORE),
                (580, y_tex+30*2), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(board_expand, str(TURN+1),
                (580, y_tex+30*3), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 255), 2, cv2.LINE_AA)
    # MANUAL
    cv2.putText(board_expand, "@ Start:",
                (435, y_tex+30*5), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 100, 0), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "@ Pause:",
                (435, y_tex+30*6), cv2.FONT_HERSHEY_SIMPLEX,
                1, (100, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "@ Exit:",
                (435, y_tex+30*7), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 200, 255), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "Space",
                (600, y_tex+30*5), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 100, 0), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "P",
                (600, y_tex+30*6), cv2.FONT_HERSHEY_SIMPLEX,
                1, (100, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "Esc",
                (600, y_tex+30*7), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 200, 255), 2, cv2.LINE_AA)
    # CONTROL
    cv2.putText(board_expand, "@ Left:",
                (435, y_tex+30*9), cv2.FONT_HERSHEY_SIMPLEX,
                1, (100, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "@ Down:",
                (435, y_tex+30*10), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "@ Right:",
                (435, y_tex+30*11), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 100, 0), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "@ Rotate:",
                (435, y_tex+30*12), cv2.FONT_HERSHEY_SIMPLEX,
                1, (170, 0, 170), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "@ Rotate:",
                (435, y_tex+30*13), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 200, 255), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "A",
                (610, y_tex+30*9), cv2.FONT_HERSHEY_SIMPLEX,
                1, (100, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "S",
                (610, y_tex+30*10), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "D",
                (610, y_tex+30*11), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 100, 0), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "W",
                (610, y_tex+30*12), cv2.FONT_HERSHEY_SIMPLEX,
                1, (170, 0, 170), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "Space",
                (610, y_tex+30*13), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 200, 255), 2, cv2.LINE_AA)
    # STATUS
    cv2.putText(board_expand, STATUS,
                (520, 70), cv2.FONT_HERSHEY_SIMPLEX,
                1.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(board_expand, "+" + str(GAIN),
                (520, 150), cv2.FONT_HERSHEY_SIMPLEX,
                1.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow(WIN_NAME, board_expand)

def key_shift(key, x_pos, y_pos):
    """
    KEY EVENT 1
    """
    if key == 97: # A
        x_pos += -1
    elif key == 115: # S
        y_pos += 1
    elif key == 100: # D
        x_pos += 1
    return x_pos, y_pos

def key_rotate(key, mino):
    """
    KEY EVENT 2
    """
    if key == 32: # Space
        mino = np.rot90(mino, k=-1)
    elif key == 119: # W
        mino = np.rot90(mino, k=1)
    return mino

def ghost_position(x_pos, y_pos, board, board_new, mino):
    """
    DRAW GHOST MINO
    """
    board_h = board.shape[0]
    mino_h = mino.shape[0]
    mino_w = mino.shape[1]
    board_bi = binary(board)
    mino_bi = binary(mino)
    for i in range(board_h - mino_h):
        ghost_check = np.copy(board_bi)
        ghost_check[y_pos+i:y_pos+mino_h+i, x_pos:x_pos+mino_w] += mino_bi
        if np.any(ghost_check > 1):
            y_bottom = i-1
            break
    board_ghost = np.copy(board_new)
    if not mino_h + 1 > y_bottom:
        board_ghost[y_pos+y_bottom:y_pos+mino_h+y_bottom,
                    x_pos:x_pos+mino_w, :] += mino//4
    return board_ghost

def mino_motion(board, mino):
    """
    The process continues until the mino settles down on the board.
    Parameters
    ----------
    board: Game board (matrix)
    mino: New tetrimino  (matrix)

    Returns
    -------
    key: key number
    board: Update board status
    """
    global SCORE
    x_pos, y_pos = 5, 1 # initial mino position
    ref_time = time.time() # reference time for free fall
    hit_bottom = False # bool
    timer = level()
    while True:
        # MINO INFO
        mino_h = mino.shape[0]
        mino_w = mino.shape[1]
        mino_binary = binary(mino)
        # UPDATE BOARD & DRAW MINO
        board_new = np.copy(board)
        board_new[y_pos:y_pos+mino_h, x_pos:x_pos+mino_w, :] += mino
        # BOARD FOR CHECK
        board_1_binary = binary(np.copy(board))  # check mino motion
        board_2_binary = binary(np.copy(board))  # check hit bottom
        board_2_binary[y_pos+1:y_pos+mino_h+1, x_pos:x_pos+mino_w] += mino_binary
        # DRAW GHOST
        board_ghost = ghost_position(x_pos, y_pos, board, board_new, mino)
        # SHOW BOARD
        board_show(board_ghost, None)
        key = cv2.waitKey(1)
        # HIT BOTTOM & FREE FALL
        cur_time = time.time()
        sub_time = cur_time - ref_time
        if np.any(board_2_binary > 1):
            if not hit_bottom:
                hit_bottom = True
                hit_time = time.time() # save hit time
            else:
                if cur_time - hit_time > timer:
                    #  allowable time for the mino until freezed
                    return None, board_new
        else:
            hit_bottom = False
            if sub_time > timer:
                y_pos += 1 # fall
                ref_time = time.time() # update reference time
        # KEY EVENT
        # SHIFT AND DOWN
        if key in (97, 100, 115): # A, S, D
            x_new, y_new = key_shift(key, x_pos, y_pos)
            board_1_binary[y_new:y_new+mino_h, x_new:x_new+mino_w] += mino_binary
            if not np.any(board_1_binary > 1):
                # CAN MOVE
                if y_pos != y_new:
                    # if the mino is dropped by the player give a score
                    SCORE += 1
                x_pos, y_pos = x_new, y_new
        # ROTATE
        elif key in (32, 119): # SPACE, W
            mino_binary_rot = key_rotate(key, mino_binary)
            mino_rot_h = mino_binary_rot.shape[0]
            mino_rot_w = mino_binary_rot.shape[1]
            if board_1_binary[y_pos:y_pos+mino_rot_h,
                              x_pos:x_pos+mino_rot_w].size == mino_binary_rot.size:
                # CAN MOVE
                board_1_binary[y_pos:y_pos+mino_rot_h,
                               x_pos:x_pos+mino_rot_w] += mino_binary_rot
                if not np.any(board_1_binary > 1):
                    # CAN MOVE
                    mino = key_rotate(key, mino)
        # PAUSE
        elif key == 112: # P
            scripts = ("PAUSE GAME", "ENTER SPACE")
            index = 1
            while True:
                if index == 1:
                    index = 0
                else:
                    index = 1
                board_show(BOARD, scripts[index])
                key = cv2.waitKey(500)
                # RESTART
                if key in (32, 112): # SPACE, P
                    ref_time = time.time()
                    break
                # EXIT
                if key == 27: # Esc
                    return key, board
        # EXIT
        elif key == 27: # Esc
            return key, board

def delete_line(board):
    """
    DELETE FILLED LINES
    """
    global GAIN, SCORE, LINES, STATUS
    board_h = board.shape[0]
    wo_frame = board[1:-1, 1:-1, :]
    wo_frame_bi = binary(wo_frame)
    wo_frame_h = wo_frame.shape[0]
    wo_frame_new = []
    for i in range(wo_frame_h):
        if not np.all(wo_frame_bi[i, :] == 1):
            wo_frame_new.append(wo_frame[i, :, :])
    wo_frame_new = np.array(wo_frame_new)
    wo_frame_new_h = len(wo_frame_new)
    board[board_h-wo_frame_new_h-1:-1, 1:-1, :] = wo_frame_new
    delete_num = wo_frame_h - wo_frame_new_h
    if delete_num == 0:
        STATUS = "d(^v^)b"
        GAIN = 0
    elif delete_num == 1:
        GAIN = SCORE_TABLE[0]*LEVEL
        SCORE += GAIN
        LINES += 1
        STATUS = "NICE"
    elif delete_num == 2:
        GAIN = SCORE_TABLE[1]*LEVEL
        SCORE += GAIN
        LINES += 2
        STATUS = "GREAT"
    elif delete_num == 3:
        GAIN = SCORE_TABLE[2]*LEVEL
        SCORE += GAIN
        LINES += 3
        STATUS = "AWESOME"
    elif delete_num == 4:
        GAIN = SCORE_TABLE[3]*LEVEL
        SCORE += GAIN
        LINES += 4
        STATUS = "AMAZING"
    return board

def main():
    """
    MAIN PROGRAM
    """
    global TURN, SCORE, MINO_FUTURE, STATUS
    # SET INITIAL PARAMETER
    board = BOARD
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE)
    # SET INITIAL MINO
    minos = []
    loop = 0
    while loop < 5:
        minos.append(MINO_TABLE[random.randint(0, MINO_NUM-1)])
        loop += 1
    # START SCREEN
    scripts = (" START GAME", "ENTER SPACE")
    index = 1
    while True:
        MINO_FUTURE = minos[TURN:TURN+4]
        if index == 1:
            index = 0
        else:
            index = 1
        board_show(board, scripts[index])
        key = cv2.waitKey(500)
        if key == 32: # SPACE
            break
        if key == 27: # Esc
            board_show(board, "  SEE YOU  ")
            cv2.waitKey(500)
            cv2.destroyAllWindows()
            sys.exit()
    # GAME START
    STATUS = "GO!!!!"
    while True:
        mino = minos[TURN] # CURRENT MINO
        MINO_FUTURE = minos[TURN+1:TURN+5] # FUTURE MINO
        key, board = mino_motion(board, mino) # ACTIVATE MINO
        # GAME OVER
        if np.any(board[1, 4:-4, :] != 0):
            scripts = (" GAME OVER", r" ENTER Esc")
            index = 1
            while True:
                if index == 1:
                    index = 0
                else:
                    index = 1
                board_show(board, scripts[index])
                key = cv2.waitKey(500)
                if key == 27:
                    break
        # EXIT
        if key == 27:
            board_show(board, "  SEE YOU  ")
            cv2.waitKey(500)
            cv2.destroyAllWindows()
            break
        # UPDATE BOARD
        TURN += 1
        board = delete_line(board)
        minos.append(MINO_TABLE[random.randint(0, len(MINO_TABLE)-1)]) # eat memory
        board_show(board, None)

if __name__ == "__main__":
    # SET PARAMETERS
    WIN_NAME = "TETRIS"
    STATUS = "READY?"
    TURN = 0
    SCORE = 0
    LINES = 0
    LEVEL = 1
    GAIN = 0
    MINO_FUTURE = None
    SCORE_TABLE = (50, 100, 200, 500)
    TIMER_TABLE = []
    REFERENCE_SCORE = []
    COUNTER = 1
    while COUNTER < 100:
        TIMER_TABLE.append(1 - 0.01*COUNTER)
        REFERENCE_SCORE.append(1000*COUNTER)
        COUNTER += 1

    # IMPORT IMAGE FILE
    PATH = os.getcwd()
    BOARD_FILE = glob.glob(PATH + "\\01_board\\" + "*.*")
    MINO_FILE = glob.glob(PATH + "\\02_tetrimino\\" + "*.*")
    BOARD = read_img(BOARD_FILE, ".png")[0]
    MINO_TABLE = read_img(MINO_FILE, ".png")
    MINO_NUM = len(MINO_TABLE)

    # MAIN PROGRAM
    main()

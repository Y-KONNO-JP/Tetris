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
    save image files in list
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

def manual_box(board):
    """
    prepare controller manual
    """
    x_0, y_0 = 276, 327
    x_1, y_1 = 242, 357
    x_2, y_2 = 276, 357
    x_3, y_3 = 312, 357
    x_4, y_4 = 242, 395
    x_5, y_5 = 257, 427
    x_6, y_6 = 294, 427
    cv2.rectangle(board, (x_0, y_0), (x_0+25, y_0-25), (127, 127, 127), -1)
    cv2.rectangle(board, (x_1, y_1), (x_1+25, y_1-25), (127, 127, 127), -1)
    cv2.rectangle(board, (x_2, y_2), (x_2+25, y_2-25), (127, 127, 127), -1)
    cv2.rectangle(board, (x_3, y_3), (x_3+25, y_3-25), (127, 127, 127), -1)
    cv2.rectangle(board, (x_4, y_4), (x_4+95, y_4-33), (127, 127, 127), -1)
    cv2.rectangle(board, (x_5, y_5), (x_5+25, y_5-25), (127, 127, 127), -1)
    cv2.rectangle(board, (x_6, y_6), (x_6+25, y_6-25), (127, 127, 127), -1)
    cv2.putText(board, "W", (276, 325),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(board, "A S D", (245, 355),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(board, "Space", (243, 386),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(board, "Q P", (259, 425),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

def future_mino_box():
    """
    prepare future mino
    """
    minos_frame = np.ones([22, 7, 3], dtype=np.uint8)*225
    minos_frame[1:-1, 1:-1] = np.zeros([20, 5, 3], dtype=np.uint8)
    for i in range(4):
        d_h = i*5
        mino_height = MINO_FUTURE[i].shape[0]
        mino_width = MINO_FUTURE[i].shape[1]
        minos_frame[2+d_h:2+d_h+mino_height, 2:2+mino_width] += MINO_FUTURE[i]
    return minos_frame

def ghost_position(x_pos, y_pos, board, board_new, mino):
    """
    draw ghost mino position
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
    board_ghost[y_pos+y_bottom:y_pos+mino_h+y_bottom,
                x_pos:x_pos+mino_w, :] += mino//2
    return board_ghost

def board_show(board, script):
    """
    draw main board
    """
    board_height = board.shape[0]
    board_width = board.shape[1]
    board[0, 4:-4] = 0
    # MAIN BOARD
    magnification = 20
    board_entire = np.zeros([board_height, board_width+10, 3], dtype=np.uint8)
    board_entire[:, 0:board_width] = board
    board_entire = cv2.resize(board_entire,
                              dsize=None,
                              fx=magnification,
                              fy=magnification,
                              interpolation=cv2.INTER_AREA)
    # FUTURE MINO
    magnification = 10
    x_pos, y_pos = 240, 0
    mino_future_frame = future_mino_box()
    mino_future_frame = cv2.resize(mino_future_frame,
                                   dsize=None,
                                   fx=magnification,
                                   fy=magnification,
                                   interpolation=cv2.INTER_AREA)
    mino_future_height = mino_future_frame.shape[0]
    mino_future_width = mino_future_frame.shape[1]
    board_entire[y_pos:y_pos+mino_future_height,
                 x_pos:x_pos+mino_future_width] = mino_future_frame
    # MANUAL
    manual_box(board_entire)
    # SCRIPT
    if script is not None:
        cv2.rectangle(board_entire, (20, 104), (219, 75), (0, 255, 255), -1)
        cv2.putText(board_entire, script, (15, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(board_entire, "{} MODE".format(MODE),
                (315, 15), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1)
    cv2.putText(board_entire, "Turn = {}".format(TURN),
                (315, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1)
    cv2.putText(board_entire, "Score = {}".format(SCORE),
                (315, 45), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1)
    magnification = 1.5
    board_entire = cv2.resize(board_entire,
                              dsize=None,
                              fx=magnification,
                              fy=magnification,
                              interpolation=cv2.INTER_AREA)
    cv2.imshow(WIN_NAME, board_entire)

def key_shift(key, x_pos, y_pos):
    """
    key event 1
    """
    if key == 97:
        x_pos += -1
    elif key == 115:
        y_pos += 1
    elif key == 100:
        x_pos += 1
    return x_pos, y_pos

def key_rotate(key, mino):
    """
    key event 2
    """
    if key == 32:
        mino = np.rot90(mino, k=-1)
    elif key == 119:
        mino = np.rot90(mino, k=1)
    return mino

def mino_motion(board, mino):
    """
    move mino
    """
    x_pos, y_pos = 5, 1 # INITIAL MINO POSITION
    t_save = round(time.time(), 1) # REFERENCE TIME
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
        # CHECK FREE FALL
        if not np.any(board_2_binary > 1):
            # IF NOT HIT BOTTOM
            if round(time.time(), 1) - t_save > SPEED:
                # FREE FALL
                y_pos += 1
                # UPDATE REFERENCE TIME
                t_save = round(time.time(), 1)
        else:
            # HIT BOTTOM
            return None, board_new
        # KEY EVENT
        if key in (97, 100, 115): # A, S, D
            # SHIFT AND DOWN
            x_new, y_new = key_shift(key, x_pos, y_pos)
            board_1_binary[y_new:y_new+mino_h, x_new:x_new+mino_w] += mino_binary
            if not np.any(board_1_binary > 1):
                # CAN MOVE
                x_pos, y_pos = x_new, y_new
        if key in (32, 119): # SPACE, W
            # ROTATE
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
        if key == 27: # Esc
            # EXIT
            return key, board_new
        if key == 112: # P
            # PAUSE
            scripts = ("PAUSE GAME", "ENTER SPACE")
            index = 0
            while True:
                if index%2 == 0:
                    script_id = 0
                else:
                    script_id = 1
                index += 1
                board_show(board, scripts[script_id])
                key = cv2.waitKey(500)
                if key in (32, 112): # Space, P
                    # RESTART
                    t_save = round(time.time(), 1)
                    break
                if key == 27: # Esc
                    # EXIT
                    return key, board_new

def delete_line(board, score):
    """
    delete bottom lines and count score
    """
    wo_frame = board[1:-1, 1:-1, :]
    wo_frame_bi = binary(wo_frame)
    wo_frame_h = wo_frame.shape[0]
    wo_frame_new = []
    for i in range(wo_frame_h):
        if not np.all(wo_frame_bi[i, :] == 1):
            wo_frame_new.append(wo_frame[i, :, :])
    wo_frame_new = np.array(wo_frame_new)
    board_h = board.shape[0]
    wo_frame_new_h = wo_frame_new.shape[0]
    board[board_h-wo_frame_new_h-1:-1, 1:-1, :] = wo_frame_new
    delete_num = wo_frame_h - wo_frame_new_h
    if delete_num == 1:
        score += 5
    elif delete_num == 2:
        score += 10
    elif delete_num == 3:
        score += 20
    elif delete_num == 4:
        score += 100
    return board, score

def select_difficulty(mode):
    """
    return fall speed from the selected mode
    """
    if mode == "EASY":
        speed = .8
    elif mode == "NORMAL":
        speed = .5
    elif mode == "HARD":
        speed = .3
    elif mode == "DEATH":
        speed = .01
    return speed

if __name__ == "__main__":
    # IMPORT BOARD AND TETRIMINOS
    PATH = os.getcwd()
    BOARD_FILE = glob.glob(PATH + "\\01_board\\" + "*.*")
    MINO_FILE = glob.glob(PATH + "\\02_tetrimino\\" + "*.*")
    BOARD = read_img(BOARD_FILE, ".png")[0]
    MINO_TABLE = read_img(MINO_FILE, ".png")
    MINO_NUM = len(MINO_TABLE)
    # PREPARE PARAMETERS
    MODE = "NORMAL"
    WIN_NAME = "GAME WINDOW"
    TURN = 0
    SCORE = 0
    SPEED = select_difficulty(MODE)
    # SET INITIAL TETRIMINOS RANDOMLY
    MINOS = []
    for loop in range(5):
        MINOS.append(MINO_TABLE[random.randint(0, MINO_NUM-1)])
    # OPEN WINDOW
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE)
    SCRIPTS = ("START GAME", "ENTER SPACE")
    INDEX = 0
    while True:
        MINO_FUTURE = MINOS[TURN:TURN+4]
        if INDEX%2 == 0:
            SCRIPT_ID = 0
        else:
            SCRIPT_ID = 1
        INDEX += 1
        board_show(BOARD, SCRIPTS[SCRIPT_ID])
        KEY = cv2.waitKey(500)
        if KEY == 32: # SPACE
            break
        if KEY == 27: # Esc
            board_show(BOARD, "BYE d(^.^)b")
            cv2.waitKey(500)
            cv2.destroyAllWindows()
            sys.exit()
    # GAME START
    while True:
        MINO = MINOS[TURN] # CURRENT MINO
        MINO_FUTURE = MINOS[TURN+1:TURN+5] # FUTURE MINO
        KEY, BOARD = mino_motion(BOARD, MINO) # ACTIVATE MINO
        # GAME OVER
        if np.any(BOARD[1, 4:-4, :] != 0):
            SCRIPTS = ("GAME OVER", r"\(*_*)/Esc")
            INDEX = 0
            while True:
                if INDEX%2 == 0:
                    SCRIPT_ID = 0
                else:
                    SCRIPT_ID = 1
                INDEX += 1
                board_show(BOARD, SCRIPTS[SCRIPT_ID])
                KEY = cv2.waitKey(500)
                if KEY == 27:
                    board_show(BOARD, "BYE d(^.^)b")
                    cv2.waitKey(500)
                    cv2.destroyAllWindows()
                    sys.exit()
        # EXIT
        if KEY == 27:
            board_show(BOARD, "BYE d(^.^)b")
            cv2.waitKey(500)
            cv2.destroyAllWindows()
            break
        # UPDATE BOARD
        TURN += 1
        BOARD, SCORE = delete_line(BOARD, SCORE)
        MINOS.append(MINO_TABLE[random.randint(0, len(MINO_TABLE)-1)])
        board_show(BOARD, None)
        cv2.waitKey(1)

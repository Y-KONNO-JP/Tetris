# -*- coding: utf-8 -*-
"""
@author: phd_mech
"""

import os
import glob
import random
import time
import numpy as np
import cv2

def read_img(file_list, extension):
    """
    save image files as np.array in list
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

def board_manual(board):
    """
    draw manual
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
    cv2.putText(board, 'W', (276, 325),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(board, 'A S D', (245, 355),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(board, 'Space', (243, 386),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(board, 'Q P', (259, 425),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

def board_mino_future():
    """
    draw future mino
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
    board_ghost[y_pos+y_bottom:y_pos+mino_h+y_bottom, x_pos:x_pos+mino_w, :] += mino//2
    return board_ghost

def board_show(board, script):
    """
    draw main board
    """
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE)
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
    magnification = 12
    x_pos, y_pos = 240, 0
    mino_future_frame = board_mino_future()
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
    board_manual(board_entire)
    # SCRIPT
    if script is not None:
        cv2.rectangle(board_entire, (20, 104), (219, 75), (0, 255, 255), -1)
        cv2.putText(board_entire, script, (35, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    magnification = 2
    board_entire = cv2.resize(board_entire,
                              dsize=None,
                              fx=magnification,
                              fy=magnification,
                              interpolation=cv2.INTER_AREA)
    cv2.putText(board_entire, '{} MODE'.format(MODE),
                (650, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(board_entire, 'Turn = {}'.format(TURN),
                (650, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(board_entire, 'Score = {}'.format(SCORE),
                (650, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow(WIN_NAME, board_entire)

def key_shift(key, x_pos, y_pos):
    """
    key control 1
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
    key control 2
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
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE)
    x_pos, y_pos = 5, 1 # INITIAL MINO POSITION
    t_save = round(time.time(), 1) # ORIGIN TIME
    while True:
        # mino info
        mino_h = mino.shape[0]
        mino_w = mino.shape[1]
        mino_binary = binary(mino)
        # current board info
        board_new = np.copy(board)
        board_new[y_pos:y_pos+mino_h, x_pos:x_pos+mino_w, :] += mino
        # board for check
        board_1_binary = binary(np.copy(board))  # check mino motion
        board_2_binary = binary(np.copy(board))  # check hit bottom
        board_2_binary[y_pos+1:y_pos+mino_h+1, x_pos:x_pos+mino_w] += mino_binary
        # board for show
        board_ghost = ghost_position(x_pos, y_pos, board, board_new, mino)
        board_show(board_ghost, None)
        key = cv2.waitKey(1)
        # check free fall
        if not np.any(board_2_binary > 1):
            # if not hit bottom
            if round(time.time(), 1) - t_save > FALL_SPEED:
                # timer for free fall
                y_pos += 1
                t_save = round(time.time(), 1) # reset time
            else:
                pass
        else:
            # hit bottom
            return None, board_new
        # KEY EVENT
        # SHIFT AND DOWN
        if key in (97, 100, 115): # A, S, D
            x_new, y_new = key_shift(key, x_pos, y_pos)
            board_1_binary[y_new:y_new+mino_h, x_new:x_new+mino_w] += mino_binary
            if not np.any(board_1_binary > 1):
                # if mino does not overlap
                x_pos, y_pos = x_new, y_new
        # ROTATE
        if key in (32, 119): # SPACE, W
            mino_binary_rot = key_rotate(key, mino_binary)
            mino_rot_h = mino_binary_rot.shape[0]
            mino_rot_w = mino_binary_rot.shape[1]
            if board_1_binary[y_pos:y_pos+mino_rot_h,
                              x_pos:x_pos+mino_rot_w].size == mino_binary_rot.size:
                # if mino does not overlap
                board_1_binary[y_pos:y_pos+mino_rot_h,
                               x_pos:x_pos+mino_rot_w] += mino_binary_rot
                if not np.any(board_1_binary > 1):
                    # if mino does not overlap
                    mino = key_rotate(key, mino)
        # EXIT
        if key == 27: # Esc
            return key, board_new
        # PAUSE
        if key == 112: # P
            board_show(board_ghost, 'PAUSE GAME')
            cv2.waitKey(500)
            while True:
                board_show(board_ghost, 'SPACE KEY')
                key = cv2.waitKey(500)
                # RESTART
                if key in (32, 112): # Space, P
                    t_save = round(time.time(), 1)
                    break
                # EXIT
                if key == 27: # Esc
                    return key, board_new
                board_show(board_ghost, 'TO RESTART')
                key = cv2.waitKey(500)

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

if __name__ == '__main__':
    # IMPORT BOARD AND TETRIMINO AS A IMAGE FILE
    PATH = os.getcwd()
    FILE_BOARD = glob.glob(PATH + '\\01_board\\' + '*.*')
    FILE_MINO = glob.glob(PATH + '\\02_tetrimino\\' + '*.*')
    BOARD = read_img(FILE_BOARD, '.png')[0]
    MINO_LIST = read_img(FILE_MINO, '.png')
    NUM_MINO = len(MINO_LIST)

    # PREPARE PARAMETERS
    WIN_NAME = 'GAME WINDOW'
    MODE = "NORMAL"
    TURN = 0
    SCORE = 0
    FALL_SPEED = select_difficulty(MODE)
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE)

    # PREPARE INITIAL MINO LIST RANDOMLY
    MINOS = []
    for loop in range(5):
        MINOS.append(MINO_LIST[random.randint(0, NUM_MINO-1)])

    # OPEN WINDOW
    while True:
        MINO_FUTURE = MINOS[TURN:TURN+4]
        board_show(BOARD, 'SPACE KEY')
        KEY = cv2.waitKey(500)
        # START
        if KEY == 32:
            break
        board_show(BOARD, 'START GAME')
        KEY = cv2.waitKey(500)
        if KEY == 32:
            break

    # GAME START
    while True:
        MINO = MINOS[TURN] # CURRENT MINO
        MINO_FUTURE = MINOS[TURN+1:TURN+5] # FUTURE MINO
        KEY, BOARD = mino_motion(BOARD, MINO) # DROP MINO
        # GAME OVER
        if np.any(BOARD[1, 4:-4, :] != 0):
            while True:
                board_show(BOARD, 'GAME OVER')
                KEY = cv2.waitKey(500)
                if KEY == 27:
                    board_show(BOARD, 'BYE (^.^)b')
                    cv2.waitKey(1500)
                    cv2.destroyAllWindows()
                    break
                board_show(BOARD, '(*_*)/Esc')
                KEY = cv2.waitKey(500)
            break
        # EXIT
        if KEY == 27:
            board_show(BOARD, 'BYE (^.^)b')
            cv2.waitKey(1500)
            cv2.destroyAllWindows()
            break
        # UPDATA BOARD
        TURN += 1
        BOARD, SCORE = delete_line(BOARD, SCORE)
        MINOS.append(MINO_LIST[random.randint(0, len(MINO_LIST)-1)])
        board_show(BOARD, None)
        cv2.waitKey(1)

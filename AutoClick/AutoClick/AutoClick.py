import pyautogui
import cv2
import os
import numpy as np
import time

from mss import mss

TIME_BETWEEN_FRAMES = 0.01

def find_game_position(sct, threshold):
    # ham de tim game position
    dino_template = cv2.imread(os.path.join('templates', 'btn.png'), 0)
    w, h = dino_template.shape[::-1]
    landscape_template = cv2.imread(os.path.join('templates','template-btn.png'), 0)
    lw, lh = landscape_template.shape[::-1]

    landscape = {}

    # mac dinh la se hien thi o screenshot 1, du co nhieu man hinh
    monitor = sct.monitors[0]
    image = np.array(sct.grab(monitor))[:,:,:3]
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_image, dino_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    if len(loc[0]):
        pt = next(iter(zip(*loc[::-1])))
        landscape = dict(monitor, height = lh, left = pt[0], top = pt[1] - lh + h, width = lw)
    return landscape

def get_game_landscape_and_set_focues_or_die(sct, threshold = 0.7):
    # ham ho tro
    landscape = find_game_position(sct, threshold)
    if not landscape:
        print("Can't find the game!")
        #exit(1)
    else:
        print("Found object")
        time.sleep(TIME_BETWEEN_FRAMES)
        pyautogui.click(landscape["left"] + 5, landscape['top'] + landscape['height'] - 5)
    return landscape

def compute_region_of_interest(landscape):
    # tu thong tin ve landscape, ta lay ra duoc 1 vung chua day du cac vat the can xem xet, nhung lai nho hon landscape(do do giam dc khoi luong tinh toan)
    ground_height = 12
    y1 = landscape['height'] - 44
    y2 = landscape['height'] - ground_height
    x1 = 44 + 24
    x2 = landscape['width'] - 1
    return x1,x2,y1,y2

def play_game():
    global LANDSCAPE
    with mss() as sct:
        while True:
            landscape = get_game_landscape_and_set_focues_or_die(sct, .8)
            LANDSCAPE = landscape.copy()

            if landscape:
                x1, x2, y1, y2 = compute_region_of_interest(landscape)                
            
            time.sleep(TIME_BETWEEN_FRAMES)


play_game()
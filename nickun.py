import multiprocessing

import cv2
import mediapipe as mp
import time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import webbrowser
import numpy as np

global coordinate
global hand_side
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2)
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0

# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)


# finger_val = [(8,5),(12,9),(16,13),(20,17)]
finger_val = [(8, 6), (12, 10), (16, 14), (20, 18)]
status_left = [-1 for _ in finger_val]
status_right = [-1 for _ in finger_val]


def calculate(upper, lower):
    print("from calculate",upper,lower)
    point1 = np.array(upper)
    point2 = np.array(lower)
    dist = np.linalg.norm(point1 - point2)
    return dist


def openBrowser():
    webbrowser.open("https://cus.ac.in/index.php/en/")
    # driver = webdriver.Chrome('./chromedriver.exe')
    # driver.get("https://cus.ac.in/index.php/en/")
    # driver.get(url)


def check_left_right(cord):
    if cord[4][0] > cord[20][0]:
        return 0
    return 1



def checkUp(fing, coordinate):
    tip = coordinate[fing[0]][1]
    base = coordinate[fing[1]][1]
    if tip > base:
        return 1
    return 0


coordinate = {val:(0,0) for val in range(0,21)}
coordinate_1 = {val: (0, 0) for val in range(0, 21)}
coordinate_2 = {val: (0, 0) for val in range(0, 21)}
count_main = 0


while cap.isOpened():
    status_left = [0 for _ in finger_val]
    status_right = [0 for _ in finger_val]
    start = time.perf_counter()
    success, img = cap.read()
    height,width,channel = img.shape
    mid_point = width//2
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    count = 0
    if results.multi_hand_landmarks:
        for hand in results.multi_handedness:
            hand_side = hand.classification[0].index
            print("hand_side",hand_side)
            for handlms in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)

                for id, lm in enumerate(handlms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    coordinate[id] = (cx,cy)
                # and coordinate[20][0] > mid_point
                if hand_side and coordinate[20][0] > mid_point and check_left_right(coordinate):
                    for idx, val in enumerate(finger_val):
                        status_right[idx] = checkUp(val, coordinate)
                        print("val",val)
                        print("coordinate",coordinate[val[0]],coordinate[val[1]])
                        print("distance",calculate(coordinate[val[0]], coordinate[val[1]]))



                    cv2.putText(img, "right" + str(status_right), (150, 100), cv2.FONT_HERSHEY_PLAIN, 3,
                                    (255, 0, 255), 2)

                if hand_side == 0 and coordinate[20][0] < mid_point and check_left_right(coordinate) == 0:
                    for idx, val in enumerate(finger_val):
                        status_left[idx] = checkUp(val,coordinate)
                    status_left.reverse()
                    cv2.putText(img, "left" + str(status_left), (200, 200), cv2.FONT_HERSHEY_PLAIN, 3,
                                (255, 0, 255), 2)
    print(status_left+status_right)
    comb = status_left+status_right
    command = [1, 1, 1, 0, 0, 1, 1, 1]
    t1 = None
    if not t1 and comb == command:
        openBrowser()
        # t1 = multiprocessing.Process(target=openBrowser)
        # t1.start()
        # t1.join()
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 200), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)
    end = time.perf_counter()
    peformance = end - start

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

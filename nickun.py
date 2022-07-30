
import cv2
import mediapipe as mp
import time
import numpy as np
from orientation import checkOrientation
global coordinate
global hand_side
from commands import check_available, fire_up_commands

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2)
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0

finger_val = [(4, 2), (8, 6), (12, 10), (16, 14), (20, 18)]
# finger_val = [(4, 5), (8, 5), (12, 9), (16, 13), (20, 17)]
status_left = [-1 for _ in finger_val]
status_right = [-1 for _ in finger_val]
trigger_command = [[0],[0]]
default_command = [0 for val in range(10)]

def calculate(upper, lower):
    print("from calculate",upper,lower)
    point1 = np.array(upper)
    point2 = np.array(lower)
    dist = np.linalg.norm(point1 - point2)
    return dist


def openBrowser():
    webbrowser.open("https://cus.ac.in/index.php/en/")


def check_left_right(cord):
    if cord[4][0] > cord[20][0]:
        return 0
    return 1

def thumb(fing,coordinate,side,orient):
    axis = 0
    upper = 0
    lower = 1
    if orient == "upside":
        axis = 1
        upper = 1
        lower = 0
    tip = coordinate[fing[upper]][axis]
    base = coordinate[fing[lower]][axis]
    if side == "left":
        if tip > base:
            return 0
        return 1
    if tip < base:
        return 0
    return 1

def checkUp(fing , coordinate,orient):
    axis = 1
    upper = 0
    lower = 1
    if orient == "upside":
        x = 0
        upper = 1
        lower = 0
    tip = coordinate[fing[upper]][axis]
    base = coordinate[fing[lower]][axis]
    # distance = calculate(tip, base)
    # if distance > 25:
    #     return 0
    # return 1
    if tip > base:
        return 1
    return 0

# def checkUp(fing , coordinate,orient):
#     x = 1
#     if orient == "upside":
#         x = 0
#     tip = coordinate[fing[0]][x]
#     base = coordinate[fing[1]][x]
#     # distance = calculate(tip, base)
#     # if distance > 25:
#     #     return 0
#     # return 1
#     if tip > base:
#         return 1
#     return 0



coordinate = {val:(0, 0) for val in range(0,21)}
coordinate_1 = {val: (0, 0) for val in range(0, 21)}
coordinate_2 = {val: (0, 0) for val in range(0, 21)}
count_main = 0



while cap.isOpened():
    status_left = [0 for _ in finger_val]
    status_right = [0 for _ in finger_val]
    start = time.perf_counter()
    success, img = cap.read()
    height, width, channel = img.shape
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
                    coordinate[id] = (cx, cy)
                handle = checkOrientation(coordinate)

                if handle[0] == 'right':
                    for idx, val in enumerate(finger_val):
                        if idx == 0:
                            status_right[idx] = thumb(val, coordinate, side="right",orient=handle[1])
                        else:
                            status_right[idx] = checkUp(val, coordinate,orient=handle[1])
                        # status_right[idx] = checkUp(val,coordinate)

                    # cv2.putText(img, "right" + str(status_right), (70, 450), cv2.FONT_HERSHEY_PLAIN, 3,
                    #                 (255, 0, 255), 2)
                #
                elif handle[0] == 'left':
                    for idx, val in enumerate(finger_val):
                        if idx == 0:
                            status_left[idx] = thumb(val, coordinate, side="left",orient=handle[1])
                        else:
                            status_left[idx] = checkUp(val, coordinate,orient=handle[1])
                    status_left.reverse()
                    # cv2.putText(img, "left" + str(status_left), (70, 400), cv2.FONT_HERSHEY_PLAIN, 3,
                    #             (255, 0, 255), 2)
    print(status_left+status_right)
    cv2.putText(img, "Command" + str(status_left+status_right), (0, 400), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 0, 255), 2)
    comb = status_left+status_right
    command = [1, 1, 1, 0, 1, 1, 0, 1, 1, 1]
    #TRIGGER SIGNAL
    if comb != trigger_command[1]:
        trigger_command[0] = trigger_command[1]
        trigger_command[1] = comb

    # cv2.putText(img, "Command" + str(trigger_command[0]) + str(trigger_command[1]), (0, 400), cv2.FONT_HERSHEY_PLAIN, 2,
    #             (255, 0, 255), 2)

    if trigger_command[0] != trigger_command[1] and trigger_command[1] == default_command:
        print("unique")
        print("both",trigger_command[0],trigger_command[1])
        if check_available(trigger_command[0]):
            print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            fire_up_commands(trigger_command[0])

        trigger_command[0] = trigger_command[1]
        trigger_command[1] = default_command







    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 200), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)
    end = time.perf_counter()
    peformance = end - start

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

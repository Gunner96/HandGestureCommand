import cv2
import mediapipe as mp
import time
import winsound
import keyboard
import concurrent.futures
                                                                                                                                                                                                                                                                                       
global coordinate
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0

finger_val = [(8,5),(12,9),(16,13),(20,17)]

def checkUp(fing):
    tip = coordinate[fing[0]][1]
    base = coordinate[fing[1]][1]
    if tip > base:
        # winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        return 1
    return 0




coordinate = {val:(0,0) for val in range(0,21)}

while cap.isOpened():
    start = time.perf_counter()
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)
            for id, lm in enumerate(handlms.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                cv2.putText(img, str(int(id)), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                coordinate[id] = (cx, cy)
    # print(coordinate)
    # checkUp(tip=8,base=6)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        res = executor.map(checkUp, finger_val)
        status = [val for val in res]
    print(status)
    # def getLandmarks(points):
    #     coordinate = {}
    #     if results.multi_hand_landmarks:
    #         for handlms in results.multi_hand_landmarks:
    #             for id,lm in enumerate(handlms.landmark):
    #                 ih, iw, ic = img.shape
    #                 point1 = handlms.landmark[points]
    #                 x, y = int(iw * point1.x), int(ih * point1.y)
    # print(coordinate[8])

    # print(handlms.landmark[8])

    # print(getLandmarks(20))
    # checkUp(8, 6)
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,200),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)
    end = time.perf_counter()
    peformance = end - start
    # print(peformance)
    cv2.putText(img, str(peformance), (150, 300), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

    cv2.putText(img, str(str(status)), (150, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
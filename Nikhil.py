import cv2
import mediapipe as mp
import time
import winsound
import keyboard

import Mapping

global hand_side
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0

finger_val = [(8, 6), (12, 10), (16, 14), (20, 18)]


coordinate = {val: (0, 0) for val in range(0, 21)}



def getHand(id,handlms,results):
    output= None
    c=0
    for hand in results.multi_handedness:
        c=c+1
        #print(hand.classification[0].index)
        if (hand.classification[0].index == id):
            h, w, c = img.shape
            x = int((handlms.landmark[0].x) * w)
            y = int((handlms.landmark[0].y) * h)
            coord = (x, y)
            label = hand.classification[0].label
            output = label,coord
            #print("id: ",hand.classification[0].index, "output ",output,"\n")

    #print(c)
    return output



while cap.isOpened():
    start = time.perf_counter()
    success, img = cap.read()
    img=cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    count1=0
    landmarks_list1 = []
    landmarks_list2 = []
    total_hand=0
    # If Landmarks Detected i.e., Hand Detected Sucessfully
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[-1]

        for index, lm in enumerate(results.multi_hand_landmarks):
            total_hand=index+1
            for id,coord in enumerate(lm.landmark):
                h, w, c = img.shape  # Height, Width, Channels
                cx, cy = int(coord.x * w), int(coord.y * h)
                if(index==0):
                    landmarks_list1.append([id, cx, cy])
                else:
                    landmarks_list2.append([id, cx, cy])
            mpDraw.draw_landmarks(img, lm, mpHands.HAND_CONNECTIONS)

        print(total_hand)
        # Drawing the Landmarks for only One Hand
        # Landmarks will be drawn for the Hand which was Detected First

    # If Hand Detected
    if results.multi_hand_landmarks != None:
        if(total_hand==1):
            if landmarks_list1[3][1] > landmarks_list1[17][1]:
                """ when x-coordinate of 3index(thumb)is greater than 17th index(pinky) then its left"""
                if(landmarks_list1[0][2] > landmarks_list1[12][2]):
                    #but only if it is upright i.e y-coordinate of 12th index is less than 0th index(palm)
                    cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Left", (landmarks_list1[0][1], landmarks_list1[1][2]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    Mapping.mappingGestureUpright(landmarks_list1, landmarks_list2)
                else:
                    """else it will be right hand properties which is upside down"""
                    cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Right", (landmarks_list1[0][1], landmarks_list1[1][2]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    Mapping.mappingGestureUpsideDown(landmarks_list1, landmarks_list2)
            else:
                if (landmarks_list1[0][2] > landmarks_list1[12][2]):
                    """#upright left hand 1"""
                    cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Right", (landmarks_list1[0][1], landmarks_list1[1][2]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    Mapping.mappingGestureUpright(landmarks_list1, landmarks_list2)
                else:
                    """#upside down right hand 1"""
                    cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Left", (landmarks_list1[0][1], landmarks_list1[1][2]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    Mapping.mappingGestureUpsideDown(landmarks_list1, landmarks_list2)
        elif(total_hand==2):
            if landmarks_list1[3][1] > landmarks_list1[17][1]:
                """main logic here is if one is right then other is surely left as total hand is 2.
                now if landmars_list1 is right then landmarks_list2 is surely left but we need to check
                if they are upside down or not """
                if (landmarks_list1[0][2] > landmarks_list1[12][2]):
                    """To check upside down y coord of middle finger tip should be greater than palm y coord"""
                    """This is upside down"""
                    cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Left", (landmarks_list1[0][1], landmarks_list1[1][2]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Right", (landmarks_list2[0][1], landmarks_list2[1][2]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                else:
                    cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Right", (landmarks_list1[0][1], landmarks_list1[1][2]), cv2.FONT_HERSHEY_SIMPLEX,2, (255, 0, 0), 5)

                    cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Left", (landmarks_list2[0][1], landmarks_list2[1][2]), cv2.FONT_HERSHEY_SIMPLEX,2, (255, 0, 0), 5)

            else:
                if (landmarks_list1[0][2] > landmarks_list1[12][2]):
                    cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Right", (landmarks_list1[0][1], landmarks_list1[1][2]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Left", (landmarks_list2[0][1], landmarks_list2[1][2]), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                else:
                    cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Left", (landmarks_list1[0][1], landmarks_list1[1][2]), cv2.FONT_HERSHEY_SIMPLEX,
                                2, (255, 0, 0), 5)
                    cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Right", (landmarks_list2[0][1], landmarks_list2[1][2]), cv2.FONT_HERSHEY_SIMPLEX,
                                2, (255, 0, 0), 5)




    # if results.multi_hand_landmarks:
    #     for id,handlms in enumerate(results.multi_hand_landmarks):
    #         #print(handlms)
    #         mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)
    #         count1+=1
    #         print("first loop: ",count1)
    #         count2=0
    #         for hand in results.multi_handedness:
    #             count2+=1
    #             print("second loop: ", count2)
    #             # print(hand.classification[0].index)
    #             if (hand.classification[0].index == id ):
    #                 h, w, c = img.shape
    #                 x = int((handlms.landmark[0].x) * w)
    #                 y = int((handlms.landmark[0].y) * h)
    #                 coord = (x, y)
    #                 label = hand.classification[0].label
    #                 output = label, coord
    #                 print("first" ,"id: ",hand.classification[0].index, "output ",output,"\n")
    #                 cv2.putText(img, label, coord, cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)







    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 200), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)
    end = time.perf_counter()
    peformance = end - start

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
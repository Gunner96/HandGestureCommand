def checkOrientation(landmarks_list1):
    if landmarks_list1[3][0] > landmarks_list1[17][0]:
        """ when x-coordinate of 3index(thumb)is greater than 17th index(pinky) then its left"""
        if (landmarks_list1[0][1] > landmarks_list1[12][1]):
            return "left"
            # but only if it is upright i.e y-coordinate of 12th index is less than 0th index(palm)
            # cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
            # cv2.putText(img, "Left", (landmarks_list1[0][1], landmarks_list1[1][2]), cv2.FONT_HERSHEY_SIMPLEX, 2,
            #             (255, 0, 0), 5)
            # Mapping.mappingGestureUpright(landmarks_list1, landmarks_list2)
        else:
            """else it will be right hand properties which is upside down"""
            return "right"
            # cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
            # cv2.putText(img, "Right", (landmarks_list1[0][1], landmarks_list1[1][2]), cv2.FONT_HERSHEY_SIMPLEX, 2,
            #             (255, 0, 0), 5)
            # Mapping.mappingGestureUpsideDown(landmarks_list1, landmarks_list2)
    else:
        if (landmarks_list1[0][1] > landmarks_list1[12][1]):
            """#upright left hand 1"""
            return "right"
            # cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
            # cv2.putText(img, "Right", (landmarks_list1[0][1], landmarks_list1[1][2]), cv2.FONT_HERSHEY_SIMPLEX, 2,
            #             (255, 0, 0), 5)
            # Mapping.mappingGestureUpright(landmarks_list1, landmarks_list2)
        else:
            """#upside down right hand 1"""
            return "left"
            # cv2.rectangle(img, (20, 335), (200, 425), (0, 255, 0), cv2.FILLED)
            # cv2.putText(img, "Left", (landmarks_list1[0][1], landmarks_list1[1][2]), cv2.FONT_HERSHEY_SIMPLEX, 2,
            #             (255, 0, 0), 5)
            # Mapping.mappingGestureUpsideDown(landmarks_list1, landmarks_list2)
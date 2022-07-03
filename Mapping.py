import webbrowser
def mappingGestureUpright(landmarks_list1,landmarks_list2):
    if(landmarks_list1[8][2]>landmarks_list1[6][2]):
        openYt();

def mappingGestureUpsideDown(landmarks_list1, landmarks_list2):
    if (landmarks_list1[8][2] < landmarks_list1[6][2]):
        openYt();

def openYt():
    webbrowser.open('http://www.youtube.com')
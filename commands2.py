import webbrowser
import subprocess
########################################
# for audio

from ctypes import cast, POINTER

import cv2
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


###########################################
# The commands have been stored a values and keys are the function that will be executed of the commands match

# The get_key() function get teh key for a particular command
def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key


# this function is used to check if the command is available in the dictionary
def check_available(val):
    if val in command_function_dict.values():
        return True
    return False


# this function is used to fire up the function associated with the commands
def fire_up_commands(val):
    comm = get_key(val, command_function_dict)
    comm()


# list of commands that will be used.

def command1():
    print("open youtube")
    webbrowser.open('http://www.youtube.com')


def command2():
    print("Notepad")
    '''os.system() will stop the current process untill the called process is finished
    we could use multi-threading in mthreading we cannot close our main application until we close our subprocess
     so Popen method does the work '''
    subprocess.Popen("C:\\Windows\\notepad.exe")


def command3():
    print("Notepad")
    '''os.system() will stop the current process untill the called process is finished
    we could use multi-threading in mthreading we cannot close our main application until we close our subprocess
     so Popen method does the work '''
    subprocess.Popen("calc.exe")


def command4():
    """Volume range is from [-65.25,0.0]"""
    volumeValue = volume.GetMasterVolumeLevel()
    print("Volume Down")
    volumeValue = float(volumeValue - 5.0)  # decreasing volume by 5units
    if (volumeValue < -65.25):
        volumeValue = -65.25
    volume.SetMasterVolumeLevel(volumeValue, None)


def command5():
    """Volume range is from [-65.25,0.0]"""
    volumeValue = volume.GetMasterVolumeLevel()
    print("Volume Raise")
    volumeValue = float(volumeValue + 5.0)  # increasing volume by 5 unit
    if (volumeValue > 0):  # this will ensume max volume will never increase beyond the limit
        volumeValue = 0.0
    volume.SetMasterVolumeLevel(volumeValue, None)


# Dictionary for storing key and values, keys are the function that will be triggered and the values are the commands
# that gets fired off if the value matches

command_function_dict = {command1: [0, 0, 0, 0, 0, 1, 1, 1, 1, 1], command2: [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                         command3: [0, 1, 1, 1, 0, 0, 1, 1, 1, 0], command4: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                         command5: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]}

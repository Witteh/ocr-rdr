import os
import time

import PIL
import pyautogui
from PIL import Image
from pynput.keyboard import Controller, Key

keyboard = Controller()
path = os.path.abspath(__file__.replace("screenshot.py", ""))
tempPath = os.path.join(path, "temp")
outputPath = os.path.join(path, "output")
allowedResolutions = [
    [2560, 1440, [0, 50, 2560, 95]],
    [1920, 1080, [0, 25, 1920, 90]]
]


def getScreenResolution():
    screenResolution = pyautogui.size()
    for i in range(len(allowedResolutions)):
        if (allowedResolutions[i][0] == screenResolution[0] and allowedResolutions[i][1] == screenResolution[1]):
            return i
    return -1


def fullScreenCapture(path, screenResolution):
    pyautogui.screenshot(path, region=(
        0, 0, allowedResolutions[screenResolution][0], allowedResolutions[screenResolution][1]))
    print("Screenshot saved to: " + path)
    scaleImage(path)


def scaleImage(path):
    print("Resizing image")
    maxsize = (1600, 900)
    image = Image.open(path)
    image.thumbnail(maxsize, PIL.Image.Resampling.LANCZOS)
    image.save(path)
    print("Image Resized")


def main():
    currentId = 1
    screenResolution = getScreenResolution()
    os.makedirs(tempPath, exist_ok=True)
    os.makedirs(outputPath, exist_ok=True)
    if (screenResolution != -1):
        print("Started Capture")
        while (True):
            fileName = "unsorted_" + str(currentId) + ".png"
            screenShotPath = os.path.join(outputPath, fileName)
            fullScreenCapture(screenShotPath, screenResolution)
            currentId += 1
            keyboard.press(Key.right)
            time.sleep(0.05)
            keyboard.release(Key.right)
            print("\nWaiting for next item\n")
            time.sleep(0.5)
    else:
        print("Unsupported Resolution")
        print("Supported Resolutions: " + str(allowedResolutions))


main()

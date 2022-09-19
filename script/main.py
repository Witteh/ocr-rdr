import glob
import os
import re
import time

import easyocr
import PIL
import pyautogui
from PIL import Image
from pynput.keyboard import Controller, Key

keyboard = Controller()
reader = easyocr.Reader(["en"], gpu=True)
allowedResolutions = [
    [2560, 1440, [0, 50, 2560, 95]],
    [1920, 1080, [0, 25, 1920, 90]]
]

path = os.path.abspath(__file__.replace("main.py", ""))
tempPath = path + "\\temp"
outputPath = path + "\\output"


def getScreenResolution():
    screenResolution = pyautogui.size()
    for i in range(len(allowedResolutions)):
        if(allowedResolutions[i][0] == screenResolution[0] and allowedResolutions[i][1] == screenResolution[1]):
            return i
    return -1


def readText(img):
    result = reader.readtext(img)
    return result


def getItemIdFromOCR(screenResolution):
    try:
        pyautogui.screenshot(tempPath + "\\ocr.png",
                             region=(
                                 allowedResolutions[screenResolution][2][0],
                                 allowedResolutions[screenResolution][2][1],
                                 allowedResolutions[screenResolution][2][2],
                                 allowedResolutions[screenResolution][2][3]
                             ))
        text = readText(tempPath + "\\ocr.png")[0][1]
        return re.search("([0-9]+)", text).group()
    except Exception as e:
        return ""


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
    screenResolution = getScreenResolution()
    os.makedirs(tempPath, exist_ok=True)
    os.makedirs(outputPath, exist_ok=True)
    if(screenResolution != -1):
        print("Program Started, waiting 10 seconds for you to tab into the game")
        # time.sleep(10)
        print("Started Capture")
        while(True):
            id = getItemIdFromOCR(screenResolution)
            if(id != None and id != ""):
                screenShotPath = outputPath + "\\" + id + ".png"
                if(not (os.path.exists(screenShotPath))):
                    print("Found item id: " + id + "\nTaking Screenshot")
                    fullScreenCapture(screenShotPath, screenResolution)
                else:
                    print("Screenshot of item " + id + " already exists")
            keyboard.press(Key.right)
            time.sleep(0.05)
            keyboard.release(Key.right)
            print("\n\nWaiting for next item\n\n")
            time.sleep(0.05)
    else:
        print("Unsupported Resolution")
        print("Supported Resolutions: " + str(allowedResolutions))


main()

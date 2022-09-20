import os

import easyocr

reader = easyocr.Reader(["en"], gpu=True)
path = os.path.abspath(__file__.replace("imageocr.py", ""))
outputPath = path + "\\final_output"
imagesPath = path + "\\output"


def getAllPngs(path):
    allFiles = os.listdir(path=path)
    for i in range(len(allFiles)):
        splitFileName = allFiles[i].split(".")
        fileExtension = splitFileName[len(splitFileName)-1]
        if str.lower(fileExtension) != "png":
            allFiles.pop(i)
    return allFiles


def readText(img):
    result = reader.readtext(img)
    return result


def getIdFromResult(result):
    bounds = result[0]
    text = result[1]
    accuracy = result[2]
    desiredAccuracy = 0.25
    if (str.lower("id:") in str.lower(text)):
        if (accuracy >= desiredAccuracy):
            id = [int(i) for i in text.split() if i.isdigit()]
            if(len(id) > 0):
                return id[0]
            else:
                updatedText = text.replace("G", "6").replace(
                    "Q", "0").replace("O", "0").replace("E", "6")  # ocr doesn't like rdr font, so we replace some characters
                id = [int(i) for i in updatedText.split() if i.isdigit()]
                if(len(id) > 0):
                    return id[0]
                return -1
    else:
        if (accuracy >= desiredAccuracy):
            id = [int(i) for i in text.split() if i.isdigit()]
            if(len(id) > 0):
                return id[0]
            else:
                return -1
    return -1


def main():
    os.makedirs(outputPath, exist_ok=True)
    os.makedirs(imagesPath, exist_ok=True)
    images = getAllPngs(imagesPath)
    for image in images:
        print("checking image: " + image)
        imagePath = imagesPath + "\\" + image
        ocrResult = readText(imagePath)
        for result in ocrResult:
            id = getIdFromResult(result)
            if id == -1:
                continue
            else:
                outputFilePath = outputPath + "\\" + str(id) + ".png"
                exists = os.path.exists(outputFilePath)
                if not exists:
                    os.rename(imagePath, outputFilePath)
                    print("renamed and moved")
                else:
                    print("conflict - skipping")


main()

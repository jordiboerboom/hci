import os
import os.path
import random
from datetime import datetime
from os import path
from os import sys
from flask import Flask
from flask import render_template
from flask import redirect
from flask import render_template
from flask import request

testDictionary = {}
testID = 0
testSize = 3
random.seed(datetime.now())

#example images
class popupParameters:
    def __init__(self, startWidth, startHeight, width, height, message):
        self.startWidth = startWidth
        self.startHeight = startHeight
        self.width = width
        self.height = height
        self.message = message

class Image:
    parametersList = []
    id = 0
    fileLocation = ""
    imageLocation = ""
    def __init__(self, id, imageType):
        self.parametersList = []
        self.id = 0
        self.fileLocation = ""
        self.imageLocation = ""
        self.id = id
        add = ""
        if (imageType == "facebook"):
            add = "FacebookExamples/"
        elif (imageType == "twitter"):
            add = "TwitterExamples/"
        elif (imageType == "websites"):
            add = "WebsiteExamples/"
        self.fileLocation = "./static/images/exampleImages/" + add + str(id) + ".txt"
        self.imageLocation = "images/exampleImages/" + add + str(id) + ".png"
        file = open(self.fileLocation, "r")
        for line in file:
            newLine = ""
            for i in range(0, len(line)):
                if (line[i] != "\n"):
                    newLine += line[i]
            valuesList = newLine.split("+")
            parameters = popupParameters(valuesList[0], valuesList[1], valuesList[2], valuesList[3], valuesList[4])
            self.parametersList.append(parameters)

class TestImageParameters:
    def __init__(self, id, imageType):
        self.parametersList = []
        self.fileLocation = []
        self.id = 0
        if (imageType == "facebook"):
            self.fileLocation = "./static/images/FacebookTestConf/" + str(id) + ".txt"
        elif (imageType == "twitter"):
            self.fileLocation = "./static/images/TwitterTestConf/" + str(id) + ".txt"
        elif (imageType == "websites"):
            self.fileLocation = "./static/images/WebTestConf/" + str(id) + ".txt"
        file = open(self.fileLocation, "r")
        for line in file:
            newLine = ""
            for i in range(0, len(line)):
                if (line[i] != "\n"):
                    newLine += line[i]
            valuesList = newLine.split("+")
            parameters = popupParameters(valuesList[0], valuesList[1], valuesList[2], valuesList[3], valuesList[4])
            self.parametersList.append(parameters)

class generateTest:
    def __init__(self, testType):
        self.fakeValues = []
        self.fileLocations = []
        self.imageParameters = []
        self.urlForFileLocations = []
        self.testsLocation = ""
        self.urlForTestsLocation = ""
        self.true = "T"
        self.false = "F"
        self.extension = ".png"
        self.textextension = ".txt"
        del self.fileLocations[:]
        del self.fakeValues[:]
        del self.urlForFileLocations[:]
        del self.imageParameters[:]
        if (testType == "facebook"):
            self.testsLocation = "./static/images/FacebookTest/"
            self.urlForTestsLocation = "images/FacebookTest/"
        elif(testType == "twitter"):
            self.testsLocation = "./static/images/TwitterTest/"
            self.urlForTestsLocation = "images/TwitterTest/"
        elif(testType == "websites"):
            self.testsLocation = "./static/images/WebTest/"
            self.urlForTestsLocation = "images/WebTest/"
        fileList = os.listdir(self.testsLocation)
        amountOfFiles = len(fileList)
        randomList = []
        for i in range(0, testSize):
            while (len(randomList) != testSize):
                randomNumber = random.randint(1,amountOfFiles)
                if (randomNumber not in randomList):
                    randomList.append(randomNumber)
        for j in range(0, len(randomList)):
            possibility1 = self.testsLocation + str(randomList[j]) + "T" + self.extension
            possibility2 = self.testsLocation + str(randomList[j]) + "F" + self.extension
            urlForPossibility1 = self.urlForTestsLocation + str(randomList[j]) + "T" + self.extension
            urlForPossibility2 = self.urlForTestsLocation + str(randomList[j]) + "F" + self.extension
            if (path.exists(possibility1)):
                self.fileLocations.append(possibility1)
                self.urlForFileLocations.append(urlForPossibility1)
                self.fakeValues.append(1)
            elif (path.exists(possibility2)):
                self.fileLocations.append(possibility2)
                self.urlForFileLocations.append(urlForPossibility2)
                self.fakeValues.append(0)
            self.imageParameters.append(TestImageParameters(randomList[j], testType))

app = Flask(__name__, template_folder='./templates')

def addTest (test):
    global testID
    global testDictionary
    testDictionary[testID] = test
    testID += 1
    return (testID - 1)

@app.route("/")
def hello():
    return render_template("menu.html")

@app.route("/main")
def mainMenu():
    return render_template("main.html")

@app.route("/uitleg", methods=['POST', 'GET'])
def uitleg():
    testType = request.args.get("testType")
    return render_template('uitleg.html', myTestType=testType)

@app.route("/voorbeeld", methods=['POST', 'GET'])
def voorbeeld():
    exampleType = request.args.get("testType")
    myImage = Image("1", exampleType)
    testType = request.args.get("testType")
    return render_template('voorbeeld.html', image=myImage, myTestType=testType)

@app.route("/uitleg2", methods=['POST', 'GET'])
def uitleg2():
    testType = request.args.get("testType")
    return render_template('uitleg2.html', myTestType=testType)

@app.route("/test", methods=['POST', 'GET'])
def test():
    testType = request.args.get("testType")
    viewType = request.args.get("showAnswers")
    testID = request.args.get("testID")
    if (int(viewType) == 0):
        myTest = generateTest(testType)
        myIndex = addTest(myTest)
        return render_template('test.html', testSize=testSize, test=testDictionary[myIndex], ID=myIndex, myTestType=testType, viewType=viewType)
    else:
        rightAnswers = request.args.get("rightAnswers");
        wrongAnswers = request.args.get("wrongAnswers");
        return render_template('test.html', testSize=testSize, test=testDictionary[int(testID)], ID=testID, myTestType=testType, viewType=viewType, right=rightAnswers, wrong=wrongAnswers)

@app.route("/testresults", methods=['POST'])
def testresults():
    result1 = request.args.get("rightAnswers")
    result2 = request.args.get("wrongAnswers")
    result3 = request.args.get("rightAnswersText")
    result4 = request.args.get("wrongAnswersText")
    myIndex = request.args.get("testID")
    return render_template('testresults.html', right=result1, wrong=result2, righttext=result3, wrongtext=result4, ID=myIndex)

@app.route("/goodbye")
def goodbye():
    return render_template('goodbye.html')

if __name__ == "__main__":
    app.run()
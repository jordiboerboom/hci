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
        elif (imageType == "website"):
            add = "WebsiteExamples/"
        self.fileLocation = "./static/images/exampleImages/" + add + str(id) + ".txt"
        self.imageLocation = "./static/images/exampleImages/" + add + str(id) + ".png"
        file = open(self.fileLocation, "r")
        for line in file:
            newLine = ""
            for i in range(0, len(line)):
                if (line[i] != "\n"):
                    newLine += line[i]
            valuesList = newLine.split(",")
            parameters = popupParameters(valuesList[0], valuesList[1], valuesList[2], valuesList[3], valuesList[4])
            self.parametersList.append(parameters)
    
class generateTest:
    def __init__(self, testType):
        self.fakeValues = []
        self.fileLocations = []
        self.urlForFileLocations = []
        self.testsLocation = ""
        self.urlForTestsLocation = ""
        self.true = "T"
        self.false = "F"
        self.extension = ".png"
        del self.fileLocations[:]
        del self.fakeValues[:]
        del self.urlForFileLocations[:]
        if (testType == "facebook"):
            testsLocation = "./static/images/FacebookTest/"
            urlForTestsLocation = "images/FacebookTest/"
        elif(testType == "twitter"):
            testsLocation = "./static/images/TwitterTest/"
            urlForTestsLocation = "images/TwitterTest/"
        elif(testType == "websites"):
            testsLocation = "./static/images/WebTest/"
            urlForTestsLocation = "images/WebTest/"
        fileList = os.listdir(testsLocation)
        amountOfFiles = len(fileList)
        randomList = []
        for i in range(0, testSize):
            while (len(randomList) != testSize):
                randomNumber = random.randint(1,amountOfFiles)
                if (randomNumber not in randomList):
                    randomList.append(randomNumber)
        for j in range(0, len(randomList)):
            possibility1 = testsLocation + str(randomList[j]) + "T" + self.extension
            possibility2 = testsLocation + str(randomList[j]) + "F" + self.extension
            urlForPossibility1 = urlForTestsLocation + str(randomList[j]) + "T" + self.extension
            urlForPossibility2 = urlForTestsLocation + str(randomList[j]) + "F" + self.extension
            if (path.exists(possibility1)):
                self.fileLocations.append(possibility1)
                self.urlForFileLocations.append(urlForPossibility1)
                self.fakeValues.append(1)
            elif (path.exists(possibility2)):
                self.fileLocations.append(possibility2)
                self.urlForFileLocations.append(urlForPossibility2)
                self.fakeValues.append(0)

app = Flask(__name__, template_folder='./templates')

@app.route("/")
def hello():
    return render_template("menu.html")

@app.route("/main")
def mainMenu():
    return render_template("main.html")

@app.route("/goodbye")
def goodbye():
    return render_template('goodbye.html')

@app.route("/uitleg", methods=['POST', 'GET'])
def uitleg():
    testType = request.args.get("testType")
    return render_template('uitleg.html', testType=testType)

@app.route("/test", methods=['POST', 'GET'])
def test():
    myTest = generateTest("facebook")
    return render_template('test.html', testSize=testSize, test=myTest)

@app.route("/testresults", methods=['POST'])
def testresults():
    result1 = request.args.get("rightAnswers")
    result2 = request.args.get("wrongAnswers")
    print (result1)
    print (result2)
    return render_template('testresults.html', right=result1, wrong=result2)

@app.route("/voorbeeld")
def voorbeeld():
    myImage = Image("1", "website")
    return render_template('voorbeeld.html', image=myImage)

if __name__ == "__main__":
    app.run()
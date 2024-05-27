from flask import Flask, request, render_template, redirect, url_for
import jsonify
from flask_restful import Resource, Api
import pandas as pd
from Logic import labelList, labelsList, insertDaysRem, insert_label, insert_labelImportance, createLabelDict
from Logic import insertLabels, sortAllLists, daysRemList, insertTask, taskList, calculateScore, insertScore, scoreList
from Logic import createDf

app = Flask(__name__)
api = Api(app)

newLabelList=[]

def returnList():
   return labelList

@app.route('/')
def getLandingPage():
   return render_template('index.html')

@app.route('/input/labels', methods=['POST', 'GET'])
def LabelInput():
   if request.method == 'POST':
      webLabel = request.form['labelName']
      insert_label(webLabel, labelList)
   return render_template("inputLabel.html", labelList=labelList)

@app.route('/input/labels/sort', methods=['POST', 'GET'])
def LabelSort():
   if request.method== 'POST':
      webIndex = request.form['removeIndexer']
      webIndex = int(webIndex)
      webIndex -= 1
      newLabelList.append(labelList[webIndex])
      labelList.remove(labelList[webIndex])
      if (len(labelList) == 0):
         return redirect(url_for('TaskInput'))
   return render_template("labelSort.html", labelList=labelList, newLabelList=newLabelList, maxList=len(labelList))


@app.route('/input/tasks', methods=['POST', 'GET']) # TODO: Finish creating a list of the options using the labels, fix any other bugs
def TaskInput():
   if request.method == 'POST':
      webTask = request.form['taskName']
      insertTask(webTask, taskList)
      webTaskLabel = request.form['taskLabel']
      insertLabels(webTaskLabel, labelsList)
      webTaskImportance = request.form['taskImportance']
      webDaysRem = request.form['taskDaysRem']
      insertDaysRem(webDaysRem, daysRemList)
      labelImportanceList = insert_labelImportance(newLabelList)
      labelDict = createLabelDict(newLabelList, labelImportanceList)
      webScore = calculateScore(webTaskImportance, webTaskLabel, webDaysRem, labelDict)
      insertScore(webScore, scoreList)

      sortAllLists(scoreList, taskList, labelsList, daysRemList)


   return render_template("inputTask.html")

@app.route('/output')
def output():
    if (request.method == 'POST'):
       listOfLists = [taskList, labelsList, daysRemList, scoreList]
       df = createDf(listOfLists)
    return render_template('output.html', df=df)



if __name__ == '__main__':
    app.run(debug=True)
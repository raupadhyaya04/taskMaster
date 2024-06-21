from flask import Flask, request, render_template, redirect, url_for
from flask_restful import Api
# Importing the backend functions we may need:
from Logic import insertDaysRem, insert_label, insert_labelImportance, createLabelDict
from Logic import insertLabels, sortAllLists, insertTask, calculateScore, insertScore, createDf, createCSV
# Importing the variables we would need from backend
from Logic import labelList, labelsList, daysRemList, taskList, scoreList
newLabelList=[] # Created here to keep within scope, used int multiple functions, same with the imported ones

# Flask setup:
app = Flask(__name__)
api = Api(app)

# API begins here:
@app.route('/')
def getLandingPage():
   return render_template('index.html')

@app.route('/input/labels', methods=['POST', 'GET'])
def LabelInput():
   if request.method == 'POST':
      webLabel = request.form['labelName']
      if ((webLabel in labelList) or ((" " in webLabel == False) and (webLabel.isalpha() == False))): # Error handling, prevents duplication/non-alphabetical labels
         pass
      else:
         insert_label(webLabel, labelList)
   return render_template("inputLabel.html", labelList=labelList)

@app.route('/input/labels/sort', methods=['POST', 'GET'])
def LabelSort(): # Measures importance of a type of task vs other tasks, eg Uni Homework vs Household Chores
   if request.method== 'POST':
      webIndex = request.form['removeIndexer']
      webIndex = int(webIndex)
      if (webIndex > len(labelList)): # Error handling, prevents page from crashing:
          pass
      else:
         webIndex -= 1
         newLabelList.append(labelList[webIndex])
         labelList.remove(labelList[webIndex])
         if (len(labelList) == 1):
            newLabelList.append(labelList[0])
            labelList.remove(labelList[0])
            return redirect(url_for('TaskInput'))
   return render_template("labelSort.html", labelList=labelList, newLabelList=newLabelList, maxList=len(labelList))

@app.route('/input/tasks', methods=['POST', 'GET'])
def TaskInput():
   if request.method == 'POST':
      webTask = request.form['taskName']
      if ((webTask in taskList) or ((" " in webTask == False) and (webTask.isalpha() == False))): # Error handling, prevents duplication/non-alphabetical task names
         pass
      else:
         insertTask(webTask, taskList)
         webTaskLabel = request.form['taskLabel']
         insertLabels(webTaskLabel, labelsList)
         webTaskImportance = int(request.form['taskImportance'])
         webDaysRem = int(request.form['taskDaysRem'])
         insertDaysRem(webDaysRem, daysRemList)
         labelImportanceList = insert_labelImportance(newLabelList)
         labelDict = createLabelDict(newLabelList, labelImportanceList)
         webScore = calculateScore(webTaskImportance, webTaskLabel, webDaysRem, labelDict)
         insertScore(webScore, scoreList)
         sortAllLists(scoreList, taskList, labelsList, daysRemList)
   return render_template("inputTask.html", newLabelList=newLabelList, taskList=taskList)

@app.route('/output')
def output():
   if (request.method == 'GET'):
      listOfLists = [taskList, labelsList, daysRemList, scoreList]
      df = createDf(listOfLists)
      createCSV(df)

   return render_template("output.html", df_html=df.to_html(classes='display', table_id='dataframe', index=False))

"""""""""
@app.route('/download')
def download():
   listOfLists = [taskList, labelsList, daysRemList, scoreList]
   df = createDf(listOfLists)
   return render_template("download.html", df_html=df.to_html(classes='display', table_id='dataframe', index=False))
"""""""""


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
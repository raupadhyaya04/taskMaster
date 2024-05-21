# -*- coding: utf-8 -*-
"""logic.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1j0X96COERbxNGOcM3nEVcOktppio1_Ah
"""

import pandas as pd

def insert_label(label, labelList):
  labelList.append(label)

def createLabelDict(labelList, importanceList):
  labelDict = dict(zip(labelList, importanceList))
  return labelDict

def rankLabels(labelList):
  newList = []

  while (len(labelList) != 1):
    for i in range(0, len(labelList)):
      print(str(i + 1) + ".", labelList[i])
      continue

    indexRemover = int(input("Choose the most important task from the list by the associated number: "))
    while ((indexRemover > len(labelList) + 1) or (indexRemover < 0)):
      print("invalid input, please try again")
      indexRemover = int(input("Choose the most important task from the list by the associated number: "))
      continue

    indexRemover -= 1
    newList.append(labelList[indexRemover])
    labelList.remove(labelList[indexRemover])
    continue

  if (len(labelList) == 1):
    newList.append(labelList[0])
    labelList.remove(labelList[0])

  newList.reverse()
  return newList

def insert_labelImportance(labelList):
  importanceList = []
  for i in range(len(labelList)):
    importanceList.append(i + 1)

  importanceList.reverse()
  labelList.reverse()
  return importanceList

def insertTask(task, taskList):
  taskList.append(task)

def insertLabels(label, labelsList):
  labelsList.append(label)

def calculateScore(task, importance, label, daysRemaining, labelDict):
  score = importance + labelDict[label] - daysRemaining
  return score

def insertScore(score, scoreList):
  scoreList.append(score)

def insertDaysRem(daysRem, daysRemList):
  daysRemList.append(daysRem)

def sortScoreList(scoreList):
  newScoreList = []
  while (len(scoreList) != 0):
    newScoreList.append(scoreList[scoreList.index(max(scoreList))])
    scoreList.remove(scoreList[scoreList.index(max(scoreList))])

def sortTaskList(scoreList, taskList):
  newTaskList = []
  while (len(scoreList) != 0):
    newTaskList.append(taskList[scoreList.index(max(scoreList))])
    scoreList.remove(scoreList[scoreList.index(max(scoreList))])
  return newTaskList

def sortLabelsList(scoreList, labelsList):
  newLabelsList = []
  while (len(scoreList) != 0):
    newLabelsList.append(labelsList[scoreList.index(max(scoreList))])
    scoreList.remove(scoreList[scoreList.index(max(scoreList))])

def sortDaysRemList(scoreList, daysRemList):
  newDaysRemList = []
  while (len(scoreList) != 0):
    newDaysRemList.append(daysRemList[scoreList.index(max(scoreList))])
    scoreList.remove(scoreList[scoreList.index(max(scoreList))])
  return newDaysRemList

def sortAllLists(scoreList, taskList, labelsList, daysRemList):

  testScoreList = scoreList.copy()
  taskList = sortTaskList(testScoreList, taskList)

  testScoreList = scoreList.copy()
  labelsList = sortLabelsList(testScoreList, labelsList)

  testScoreList = scoreList.copy()
  daysRemList = sortDaysRemList(testScoreList, daysRemList)

  testScoreList = scoreList.copy()
  scoreList = sortScoreList(testScoreList)

print("Welcome to the taskMaster!")

# Label List
labelList = []

# Task Lists
taskList = []
labelsList = []
daysRemList = []
scoreList = []

# Label frontend:
quitLabels = False
while (quitLabels != True):
  labelName = input("Insert Label name: ")

  insert_label(labelName, labelList)

  print(labelList)

  end = input("Are you done? (y/n): ")

  if (end == "y"):
    quitLabels = True
  else:
    continue
labelList = rankLabels(labelList)
labelImportanceList = insert_labelImportance(labelList)
labelDict = createLabelDict(labelList, labelImportanceList)

print("\nNow let's insert some tasks:")
# Task frontend:
quitTasks = False

while (quitTasks != True):
  task = input("Insert task name: ")
  importance = float(input("Insert task's importance on a scale of 1-5: "))
  while (importance > 5 or importance < 1):
    print("Incorrect input, please try again")
    importance = float(input("Insert task's importance on a scale of 1-5: "))
    continue

  for index in range(0, len(labelList)):
    print(str(index + 1) + ".", labelList[index])
  label = input("Insert task label: ")
  while (label not in labelList):
    print("Invalid input, try again")
    label = input("Insert task label: ")

  insertLabels(label, labelsList)

  daysRemaining = int(input("How many days are remaining for this task? \n"))
  insertDaysRem(daysRemaining, daysRemList)\

  while (daysRemaining < 0):
    print("Incorrect input, please try again")
    daysRemaining = input("How many days are remaining for this task? \n")
    continue
  insertTask(task, taskList)

  score = calculateScore(task, importance, label, daysRemaining, labelDict)
  insertScore(score, scoreList)

  end = input("Are you done? (y/n): ")
  if (end == "y"):
    quitTasks = True

sortAllLists(scoreList, taskList, labelsList, daysRemList)

listOfLists = [taskList, labelsList, daysRemList, scoreList]

df = pd.DataFrame(listOfLists).transpose()
df.columns = ["Task", "Label", "Days Remaining", "Score"]

print(str(df))
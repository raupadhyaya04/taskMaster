import pandas as pd

from Logic import labelList, labelsList, insertDaysRem, insert_label, insert_labelImportance, rankLabels, createLabelDict
from Logic import insertLabels, sortAllLists, daysRemList, insertTask, taskList, calculateScore, insertScore, scoreList
from Logic import createDf



# Terminal interface:
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
  insertDaysRem(daysRemaining, daysRemList)

  while (daysRemaining < 0):
    print("Incorrect input, please try again")
    daysRemaining = input("How many days are remaining for this task? \n")
    continue
  insertTask(task, taskList)

  score = calculateScore(importance, label, daysRemaining, labelDict)
  insertScore(score, scoreList)

  end = input("Are you done? (y/n): ")
  if (end == "y"):
    quitTasks = True

sortAllLists(scoreList, taskList, labelsList, daysRemList)

listOfLists = [taskList, labelsList, daysRemList, scoreList]

df = createDf(listOfLists)

print(str(df))
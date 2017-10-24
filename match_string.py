import csv
import re

#Script is trying to find vehicles that have not been reviewed yet.

#open csv file that has been reviewed
evaluatorSurveyList = open('G:/Products/Evaluator Survey/List for Vehicle Requests from OEMs/EvaluatorSurveyResultsAug2016.csv', 'r')
#open csv file that has all models in market
exhaustiveList = open('G:/Products/Evaluator Survey/List for Vehicle Requests from OEMs/ExhaustiveListofModelsApr2016.csv', 'r')
#save csv file
outpuList = open('G:/Products/Evaluator Survey/List for Vehicle Requests from OEMs/OutputList1234.csv', 'w')

evaluateReader = csv.reader(evaluatorSurveyList)
exhaustiveReader = csv.reader(exhaustiveList)

# loop through csv file that has all models in market and compare against csv file that has been reviewed.
# Goal is to output models that have NOT been reviewed.

outputCarList = []

evaluateCar2Darray = []
exhaustiveCar2Darray = []

evaluateCarDict = {}
exhaustiveCarModelDict = {}

#looping through each evaulateReader and put in a 2d array
for evaluateCar in evaluateReader:
        evaluateCarString = ''.join(evaluateCar)
        evaluateCarSplit = evaluateCarString.split(' ') #split by blank space
        evaluateCar2Darray.append(evaluateCarSplit)
        #print(evaluateCar2Darray)

#looping through each exhaustiveReader and put in a 2d array
for exhaustiveCar in exhaustiveReader:
    exhaustiveCarString = ','.join(exhaustiveCar)
    exhaustiveCarSplit = exhaustiveCarString.split(',') #split by comma
    exhaustiveCar2Darray.append(exhaustiveCarSplit)
    #print(exhaustiveCar2Darray)

for exhaustiveItem in exhaustiveCar2Darray:
    exhaustiveCarMake = str(exhaustiveItem[0]).upper().strip()
    exhaustiveCarModel = str(exhaustiveItem[1]).upper().strip()
    if(exhaustiveCarModel not in exhaustiveCarModelDict):
        exhaustiveCarModelDict[exhaustiveCarModel] = exhaustiveCarModel
    for evaluateCar in evaluateCar2Darray:
        evaluateCarMake = str(evaluateCar[0]).upper().strip()
        if(evaluateCarMake == exhaustiveCarMake):
            for item in evaluateCar[1:]:
                itemCheck = str(item).upper().strip()
                regex = re.compile(itemCheck)
                matches = [string for string in exhaustiveCarModelDict if re.match(regex,string)]
                if(exhaustiveCarModel == ''.join(matches)):
                    if exhaustiveCarModel not in evaluateCarDict:
                        evaluateCarDict[exhaustiveCarModel] = str(item).upper().strip()




# for exhaustiveItem in exhaustiveCar2Darray:
#     exhaustiveCarMake = str(exhaustiveItem[0]).upper().strip()
#     exhaustiveCarModel = str(exhaustiveItem[1]).upper().strip()
#     if(exhaustiveCarModel not in exhaustiveCarModelDict):
#         exhaustiveCarModelDict[exhaustiveCarModel] = exhaustiveCarModel
#     for evaluateCar in evaluateCar2Darray:
#         evaluateCarMake = str(evaluateCar[0]).upper().strip()
#         if(evaluateCarMake == exhaustiveCarMake):
#             for item in evaluateCar[1:]:
#                 itemCheck = str(item).upper().strip()
#                 if(exhaustiveCarModel == itemCheck):
#                     if exhaustiveCarModel not in evaluateCarDict:
#                         evaluateCarDict[exhaustiveCarModel] = str(item).upper().strip()


#delete any vehicles that have been evaluated already
for model in evaluateCarDict:
    exhaustiveCarModelDict.pop(model)

#output to output file
with outpuList as writer:
    for x in exhaustiveCarModelDict:
        writer.write(x + '\n')



#
import re
regex = re.compile('glc')

l = ['this', 'is', 'just', 'a', 'glc-class']

matches  = [string for string in l if re.match(regex,string)]
print(matches)

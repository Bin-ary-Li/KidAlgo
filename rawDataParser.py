import csv
import pandas as pd
import re


kidDataPath = 'KIDALGORITHMS_DEMO.csv'
outputPath = './NewKidAlgoData_test.csv'

newData = {'ID':[], 'DOB':[],'AGE':[],'GENDER':[],'ALGOTYPE':[],'DEMO':[],'RESPONSE':[],'L/R':[]}


def parser (s):
    for ri, response in enumerate(re.split(r"\s*,\s*", s)): # split on commas
        print ri, response
        lb, rb = re.split(r"/", response) # split left and right buckets
        parsedList = []
        ## Process annotations
        
        # add in corrections -- any characters followed by c, put into other bucket
        for x in re.findall("([A-Z])c", lb):
            rb += x
        for x in re.findall("([A-Z])c", rb):
            lb += x
        # now remove these from the original side
        lb = re.sub(r"[A-Z]c", "", lb)
        rb = re.sub(r"[A-Z]c", "", rb)

        # toss out m annotation for now
        lb = re.sub(r"m", "", lb)
        rb = re.sub(r"m", "", rb)
        
        # b -- put back into original container 
        # for now, we'll remove these
        lb = re.sub(r"[A-Z]b", "", lb)
        rb = re.sub(r"[A-Z]b", "", rb)
          
        # a little check that there's nothing else weird in the strings
        print lb, rb
        assert not re.search(r"[^A-Z]", lb)
        assert not re.search(r"[^A-Z]", rb)
        
        # for ai, a in enumerate(lb):
        #     print ri, ai, "left", a 
        
        # for ai, a in enumerate(rb):
        #     print ri, ai, "right", a

        parsedList=[lb,rb]
        return parsedList


def itr (list): 
	for x in list[0]:
		newData['ID'].append(childID)
		newData['DOB'].append(childDOB)
		newData['AGE'].append(childAge)
		newData['GENDER'].append(childGender)
		newData['L/R'].append('L')
		newData['RESPONSE'].append(x)
	for x in list[1]:
		newData['ID'].append(childID)
		newData['DOB'].append(childDOB)
		newData['AGE'].append(childAge)
		newData['GENDER'].append(childGender)
		newData['L/R'].append('R')
		newData['RESPONSE'].append(x)

with open(kidDataPath) as csvfile:
	childAlgoData = csv.DictReader(csvfile)
	for child in childAlgoData:
		childID = child['ID']
		childDOB = child['DOB']
		childAge = child['AGE']
		childGender = child['GENDER']
		childSortDM = child['SORT_DEMO']
		childSortOut = child['SORT_OUTPUT']
		childDbDM = child['DOUBLE_DEMO']
		childDbOut = child['DOUBLE_OUTPUT']
		childHchDM = child['HITCH_DEMO']
		childHchOut = child['HITCH_OUTPUT']
		print childHchOut
		HchOutL = parser(childHchOut)
		itr(childSortOut)
		itr(childDbOut)
		itr(childHchOut)


df = pd.DataFrame(data=newData)
df.to_csv(path_or_buf=outputPath, index=False)

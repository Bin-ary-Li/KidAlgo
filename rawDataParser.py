import pandas
import re

inputPath = "./KA_DATA/DEMO_OUTPUT-Table 1.csv"
outputPath = "./experimentData.csv"
outputCSVHeaders = ['AGE', 'ALGOTYPE', 'DEMO', 'OVERALL.RESPONSE', 'DOB', 'GENDER', 'ID', 'OVERALL.RESPONSE.NO', 'RESPONSE.NO', 'ACTION.NO', 'BUCKET', 'RESPONSE']


# read in data
dRaw = pandas.read_csv(inputPath)

# cleaning, drop completely null and 0 response
d = dRaw.loc[ (dRaw['SORT_OUTPUT'].notnull()) | (dRaw['DOUBLE_OUTPUT'].notnull()) | (dRaw['HITCH_OUTPUT'].notnull()) ]
d = d.loc[ (d['SORT_OUTPUT']!="0") | (d['DOUBLE_OUTPUT']!="0") | (d['HITCH_OUTPUT']!="0") ]

# Parser function
def regexParse (row, algoType):
    algoLabel = algoType + "_OUTPUT"
    demoLabel = algoType + "_DEMO"
    resString = row[algoLabel]
    dataStr = []
    overall_response_count = 0
    if pandas.isna(resString) : resString = " / "
    for ri, response in enumerate(re.split(r"\s*,\s*", resString)): # split on commas
        lb, rb = re.split(r"/", response) # split left and right buckets

        # remove whitespace
        lb = re.sub(r"\s", "", lb) 
        rb = re.sub(r"\s", "", rb)

        ##############################
        ## Process annotations
        ##############################

        # Remove xes
        lb = re.sub(r"x", "", lb)
        rb = re.sub(r"x", "", rb)

        # b -- put back into original container 
        # for now, we'll remove these
        # sometimes cm may occur if they correct and then put it back
#         lb = re.sub(r"[A-Z][cm]*b", "", lb)
#         rb = re.sub(r"[A-Z][cm]*b", "", rb)
#         or just remove all the b
        lb = re.sub(r"b", "", lb)
        rb = re.sub(r"b", "", rb)

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

#         print rb + "," + lb
        assert not re.search(r"[^A-Z]", lb)
        assert not re.search(r"[^A-Z]", rb)

        for ai, a in enumerate(lb):
            singleAct = [row["AGE"], algoType, row[demoLabel], row[algoLabel], row['DOB'], row['GENDER'], row['ID'],overall_response_count, ri, ai, "left", a] 
            dataStr.append(singleAct)
            overall_response_count += 1

        for ai, a in enumerate(rb):
            singleAct = [row["AGE"], algoType, row[demoLabel], row[algoLabel], row['DOB'], row['GENDER'], row['ID'],overall_response_count, ri, ai, "right", a] 
            dataStr.append(singleAct)
            overall_response_count += 1
    return dataStr

# take in cleaned dataframe, output string of single ball moving actions
def parseAll (d):
    dataStr = []
    for subjecti, row in d.iterrows(): 
        dataStr += regexParse(row, "SORT") + regexParse(row, "DOUBLE") + regexParse(row, "HITCH")
    return dataStr



dataStr = parseAll(d)
finalDF = pandas.DataFrame(dataStr, columns=outputCSVHeaders)
finalDF.to_csv(outputCSVHeaders)





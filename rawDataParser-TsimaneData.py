
import pandas
import re
import math
import warnings

# specify raw data csv file and output path
pathToRawDataCSV = "./KA_DATA/ALGORITHMS_TSIMANE_newAlgo_format.csv"
saveTo = "./experimentTsimaneData.csv"

# specify output csv header format
outputCSVHeaders = ['AGE', 'ALGOTYPE', 'DEMO', 'OVERALL.RESPONSE', 'KNOWERLEV','GENDER', 'ID','PASS_SORT','PASS_DOUBLE','PASS_HITCH','PASS_SORT_1','PASS_DOUBLE_1','PASS_HITCH_1', 'OVERALL.RESPONSE.NO', 'RESPONSE.NO', 'ACTION.NO', 'BUCKET', 'RESPONSE']


# read csv
dRaw = pandas.read_csv(pathToRawDataCSV)
d = dRaw.loc[ (dRaw['OUTPUT']!="0") & (dRaw['OUTPUT_SIDE'] != "0") ]



# parser function
def parseTsiData (data): 
    dataStr = []
    # iterate through rows
    for i, row in d.iterrows():
        # get id, algotype, age, etc for current row
        ID = row["ID"]
        algoType = row["ALGO TYPE"]
        age = row['AGE']
        overall_response_count = row["NUMBER_MOVEMENTS"]
        # set counter for responses and number of total balls moved
        ri = 0
        BallMovedCount = 0

        # for current row, save the columns that contain response and side of output into a iterator, then iterate through results in these columns
        iterRow = iter(row[5:-2])
        for outputCol in iterRow:
            # get the pairwised result (since the columns for response alternate in pair, i.e., ball1, side1, ball2, side2)
            ballMoved = outputCol
            side = next(iterRow)
            # check nan
            if (not pandas.isna(ballMoved)) & (not pandas.isna(side)):
                ri+=1
                # regex finds what balls are moved (blue/black/red) in the response
                for ai, ball in enumerate(re.findall(r"blue|black|red", ballMoved)):
                    BallMovedCount+=1
                    # append each ball movement with relevant info into a big list, which will later convert to output csv, so order need to conform to specified csv header parameter
                    singleAct = [age, algoType, None, None, None, None, ID ,None,None,None,None,None,None, BallMovedCount, ri, ai, side, ball]
                    dataStr.append(singleAct)
        # just checking (might be superfluous)
        if overall_response_count != ri:
            print overall_response_count, ri
            warnings.warn("reported response count doesn't match actual number of response parsed at ID: {ID}, Algo: {Algo}".format(ID=ID, Algo=algoType))
    # return the big list of all the ball movements for outputting to csv
    return dataStr
                    



# run and save
dataStr = parseTsiData(d)
finalDF = pandas.DataFrame(dataStr, columns=outputCSVHeaders)
finalDF.to_csv(saveTo)
            






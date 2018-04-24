import pandas as pd
import argparse
import numpy
import sys
from io import StringIO

if(len(sys.argv) != 2):
    print("\n\tPlease enter the path of the csv as the only arguement\n")
    exit(1)

config = pd.read_csv("./config.csv", header=None, engine='python')
config.drop([0], inplace=True)

config_dict = {}
for index, row in config.iterrows():
    temp = map(str.strip,row[1:3])
    config_dict[row[0]] = list(map(float, temp))
    config_dict[row[0]].append(row[3])

dataFile = open(sys.argv[1], "r", errors="replace")

print("Loading csv into memory...")

df_chunks = pd.read_csv(dataFile, dtype=object, chunksize=1000)

print("Running Transformations...")

index = 0
units = []

for df in df_chunks:


    if(index == 0):
        units = df.loc[0]
        df.drop(0)

    date = df.loc[:, 'Unnamed: 0']
    time = df.loc[:, 'Unnamed: 1']
    df = df.apply(pd.to_numeric, errors="coerce")


    if(index == 0):
        for num, column in enumerate(list(df.columns[2:])):
            df.loc[0, column] = units[num + 2]
            if(column in config_dict):
                df.loc[0, column] = "[ " + config_dict[column][2] + "]"
                df.loc[1:, column] = ((df.loc[1:, column] + config_dict[column][1]) * config_dict[column][0])
            df.loc[1:, column] = df.loc[1:, column].apply(lambda x: str("{:.3f}".format(x)))

    else:
        for num, column in enumerate(list(df.columns[2:])):
            if(column in config_dict):
                df.loc[:, column] = ((df.loc[:, column] + config_dict[column][1]) * config_dict[column][0])
            df.loc[:, column] = df.loc[:, column].apply(lambda x: str("{:.3f}".format(x)))




    df['Unnamed: 0'] = date
    df['Unnamed: 1'] = time

    df.replace(numpy.nan, '', regex=True, inplace=True)

    df.replace(['nan', 'None'], '', inplace=True)


    

    if(index == 0):
        df.to_csv(sys.argv[1][:-4] + "_new.csv", index=False)
    else:
        df.to_csv(sys.argv[1][:-4] + "_new.csv", index=False, header=False, mode='a')


    index += 1


print("Finished transformations, outputting into {}_new.csv...".format(
    sys.argv[1][:-4]))

print("All Done")

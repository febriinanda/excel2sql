from datetime import datetime
from os import path, mkdir
import sys
import pandas as pd
import os
import time


def tz_checking(data):
    if int(data) == 0:
        return tz_def
    else:
        return data


def convert(data):
    return datetime.strptime(data, '%Y%m%d').strftime('%d-%b-%y')


def reverse(data, def_value):
    if int(data) == 0:
        return def_value

    data.zfill(8)
    return datetime.strptime(data, '%d%m%Y').strftime('%d-%b-%y')


print("Number of arguments:", len(sys.argv))
print("Args list:", str(sys.argv))

tz = []
tz_def = 0

tz_rev = []
tz_rev_def = 0

nn = []
nn_def = 0

exc = []

table_name = sys.argv[1]
excel_name = sys.argv[2]
limitation = int(sys.argv[3])
advanced = sys.argv[4]
rules = advanced.split(";")

for i in rules:
    rule = i.split(":")
    if rule[0] == "NN":
        nn_def = rule[1]
        nn = rule[2].split(",")
    elif rule[0] == "TZ":
        tz_def = rule[1]
        tz = rule[2].split(",")
    elif rule[0] == "TZ-":
        tz_rev_def = rule[1]
        tz_rev = rule[2].split(",")
    else:
        exc = rule[2].split(",")

excelData = pd.read_excel(os.getcwd() + "\\" + excel_name, "Sheet1", dtype=object)
headers = list(excelData)

counter = 0
generated_path = os.getcwd() + "\\generated\\"
if not path.exists(generated_path):
    mkdir(generated_path)

timestamp_now = time.time()
ex_name = excel_name.split(".")
file_name = ex_name[0] + "_insert_" + str(int(round(timestamp_now)))
f = open(generated_path + file_name + ".sql", "w+")

copied = excelData.copy()
part = 1
limit = limitation
for i in range(len(excelData)):
    if i == limit and limit != 0:
        part = part + 1
        limit = limitation * part
        f.close()
        print("**Open for part:"+str(part))
        f = open(generated_path + file_name + "_" + str(part) + ".sql", "w+")

    line_headers = headers.copy()
    col_list = []

    for y in headers:
        try:
            if y in exc:
                line_headers.remove(y)
                continue

            val = str(excelData[y][i])
            if pd.isna(excelData[y][i]):
                if y in nn:
                    val = nn_def
                else:
                    line_headers.remove(y)
                    continue
            else:
                if y in tz:
                    val = convert(tz_checking(val))
                elif y in tz_rev:
                    val = reverse(val, tz_rev_def)

            if "\'" in val:
                val = val.replace("\'", "\'\'")
            col_list.append(val)
        except ValueError:
            print("Error - Row:"+str(i)+", Field:"+y+", Value:"+str(val))
            continue

    counter = counter + 1
    counter_txt = "-- Query insert No #" + str(counter) + "\n"
    sql_txt = "INSERT INTO {0}({1}) VALUES(\'{2}\'); \n".format(table_name, ",".join(line_headers),
                                                                "','".join(col_list))

    f.write(counter_txt)
    f.write(sql_txt)

f.close()

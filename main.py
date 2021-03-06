from os import path, mkdir
import sys
import pandas as pd
import os
import time

import utility


table_name = "TABLE_NAME"
excel_name = "Sample1.xlsx"
mode = "insert"
pk_name = None
pk_value = None
limitation = 0

nn = []
nn_def = 0

tz = []

exc = []
for i in range(len(sys.argv)):
    args = sys.argv[i]
    print("arg:" + str(i) + ", value:" + args)

    if "=" in args:
        arg = args.split("=")
        if len(arg) > 0:
            arg_key = arg[0]
            arg_val = arg[1]
            if arg_key == "--table":
                table_name = arg_val
            elif arg_key == "--file":
                excel_name = arg_val
            elif arg_key == "--mode":
                mode = arg_val.lower()
            elif arg_key == "--pk":
                pk_name = arg_val
            elif arg_key == "--limit":
                limitation = int(arg_val)
            elif arg_key == "--nn":
                nn = arg_val.split(",")
            elif arg_key == "--nn_value":
                nn_def = arg_val
            elif arg_key == "--tz":
                tz = arg_val.split(",")
            elif arg_key == "--tz_value":
                utility.tz_def = arg_val
            elif arg_key == "--exc":
                exc = arg_val.split(",")

excelData = pd.read_excel(os.getcwd() + "\\" + excel_name, "Sheet1", dtype=object)
headers = list(excelData)

counter = 0
generated_path = os.getcwd() + "\\generated\\"
if not path.exists(generated_path):
    mkdir(generated_path)

timestamp_now = time.time()
ex_name = excel_name.split(".")
file_name = ex_name[0] + "_" + mode + "_" + str(int(round(timestamp_now)))
f = open(generated_path + file_name + ".sql", "w+")

if pk_name is not None:
    if pk_name not in headers:
        pk_name = headers[0]
else:
    pk_name = headers[0]

copied = excelData.copy()
part = 1
limit = limitation
for i in range(len(excelData)):
    if i == limit and limit != 0:
        part = part + 1
        limit = limitation * part
        f.close()

        print("**Open for part: {0}".format(str(part)))
        f = open(generated_path + file_name + "_" + str(part) + ".sql", "w+")

    line_headers = headers.copy()
    col_list = []
    pk_value = None
    val = None
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
                    val = utility.convert(utility.tz_checking(val))
                # elif y in tz_rev:
                #     val = reverse(val, tz_rev_def)

            if "\'" in val:
                val = val.replace("\'", "\'\'")

            if mode == "insert":
                col_list.append(val)
            else:
                if y == pk_name:
                    pk_value = val
                else:
                    update_set = "{0}='{1}'".format(y, str(val))
                    col_list.append(update_set)
        except ValueError:
            print("Error - Row: {0}, Field: {1}, Value: {2}".format(str(i), y, str(val)))
            continue

    counter = counter + 1
    counter_txt = "-- Query {1} No #{0} \n".format(str(counter), mode)

    if mode == "insert":
        sql_txt = "INSERT INTO {0}({1}) VALUES(\'{2}\'); \n".format(table_name, ",".join(line_headers),
                                                                    "','".join(col_list))
    else:
        sql_txt = "UPDATE {0} SET {1} WHERE {2}='{3}'; \n".format(table_name, ",".join(col_list),
                                                                  pk_name, pk_value)

    f.write(counter_txt)
    f.write(sql_txt)

f.close()

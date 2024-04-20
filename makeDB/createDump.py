import csv

def is_float(element: any) -> bool:
    #If you expect None to be passed:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def rowDump(tableName: str, columns : str, row : list[str]):
    first = True

    rowStr = "("
    for value in row:
        if value == "":
            value = "NULL"
        if not value.isnumeric() and not is_float(value) and not value == "NULL":
            rowStr = rowStr + "'"
        rowStr = rowStr + value
        if not value.isnumeric() and not is_float(value) and not value == "NULL":
            rowStr = rowStr + "'"

        rowStr = rowStr + ','


    rowStr = rowStr[:-1]
    rowStr = rowStr + '),\n'
    return rowStr


# Given the name of each column of a table and also a 2d value matrix
# this fucntion will return a string with the sql version of each row
# that can be ran to add all values into the database

def tableDump(tableName: str, columns : list[str], values : list[list[str]]) -> str:
    numCols = len(columns)
    outStr = ""
    columnNamesStr = ""
    
    count2 = 0
    for value in columns:
        count2 = count2 + 1
        columnNamesStr = columnNamesStr + value
        if count2 < numCols:
            columnNamesStr = columnNamesStr + ','
    outStr += "INSERT INTO %s (%s) VALUES" % (tableName, columnNamesStr)
    for row in values:
        if numCols != len(row):
            print("Incorrect number of Columns")
            continue
        rowStr = rowDump(tableName, columnNamesStr, row)
        outStr += rowStr
    outStr = outStr[:-2]
    outStr += ";\n"
    return outStr


def CSVToDump(fileName : str,
              table_name : str,
              use_custom_headers : bool = False,
              custom_headers : list[str] = None

              ) -> str:
    fileName = "readyTables/" + fileName
    file = open(fileName, 'r')
    reader = csv.reader(file)
    #hoping this actually works
    dataList : list[list[str]] = list(reader)

    if file.closed:
        print('Error: ' + fileName + 'could not be opened')
        return "ERROR"

    headers : list[str] = None
    if use_custom_headers:
        headers = custom_headers
    else:
        headers = dataList[0]
        dataList.pop(0)
    return tableDump(tableName=table_name,columns=headers, values=dataList)


















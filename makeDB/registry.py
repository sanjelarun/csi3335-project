#file is able to parse a registry to get
#all table names, and any custom headers and
#table schema

#registry file: the first line is a fileName which contains all table creations,
# each next line is a fileName. After is a tableName and a custom header list if used

import csv
import createDump

class registry:
    registryFileName : str = None
    fileNames : list[str] = []
    tableNames: dict[str,str] = {}
    customHeaders : dict[str,list[str]] = {}
    tableSchema : str = None


    def __init__(self, registryName : str):
        self.registryFileName = registryName
        #open file and read each line
        file = open(self.registryFileName, 'r')
        if file.closed:
            print("Could not open registry")
            return
        reader = csv.reader(file)
        dataList: list[list[str]] = list(reader)

        #do first line
        if(len(dataList) < 2):
            print("Error: registry must contain at least the table schema and 1 data file")
            return

        if len(dataList[0]) != 1:
            print("Error in table Schema line (first line)")
            return

        tableFile = open(dataList[0][0], 'r')
        if tableFile.closed:
            print("Error could not open table schema file")
            return

        self.tableSchema = tableFile.read()


        #parse rest of lines
        first = True
        #pop first registry line

        for row in dataList:
            print(row)
            if first:
                first = False
                continue

            if len(row) < 2:
                print("Each table needs a fileName and a tableName. Headers are optional")
                return

            self.fileNames.append(row[0])
            self.tableNames.update({row[0] : row[1]})
            row.pop(0)
            row.pop(0)

            headers : list[str]= []
            for val in row:
                headers.append(val)

            if len(headers) > 0:
                self.customHeaders.update("{%s: %s}" % (self.fileNames, headers))


    def createDumpFromRegistry(self, outputFileName : str):
        file = open(outputFileName, 'w')
        if file.closed:
            print("An error occurred when trying to open/create the output file")
            return

        #file.write(self.tableSchema + '\n\n\n')

        for fileName in self.fileNames:
            useCustomHeaders = False
            if fileName in self.customHeaders.keys():
                useCustomHeaders = True
            if not fileName in self.tableNames.keys():
                print("Error: " + fileName + " is missing an associated tableName")
            if useCustomHeaders:
                file.write(createDump.CSVToDump(fileName,
                                     table_name=self.tableNames.get(fileName),
                                     use_custom_headers=True,
                                     custom_headers=self.customHeaders.get(fileName)) + '\n\n\n')
            else:
                file.write(createDump.CSVToDump(fileName, table_name=self.tableNames.get(fileName)) +'\n\n\n')









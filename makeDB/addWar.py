import csv


def getEntriesFromCSV(fileName) -> list[list[str]]:
    entries : list[list[str]]
    file = open(fileName, 'r')
    reader = csv.reader(file)
    # hoping this actually works
    dataList: list[list[str]] = list(reader)

    if file.closed:
        print('Error: ' + fileName + 'could not be opened')
        return "ERROR"

    dataList.pop(0)
    outList : list[list[str]] = []
    for entry in dataList:
        line : list[str] = []
        entry[2] = entry[2].replace("'", "''")

        line.append(entry[2]) #playerid
        line.append(entry[3]) #yearid
        line.append(entry[5]) #stint
        line.append(entry[41])  # p_war162
        line.append(entry[18]) #b_war162
        line.append(entry[59]) #WAR162
        outList.append(line)

    return outList

'UPDATE BATTING SET b_WAR162 = line[3] WHERE yearID = line[x] AND playerid = line[x] AND stint = line[x]'

def makeSQLUpdates(entries : list[list[str]]) -> str:
    outStr = "INSERT INTO advancedstats(playerId,yearId,stint,as_pitchWar162,as_batWar162,as_war162) VALUES "
    for entry in entries:
        outStr += ("('" + entry[0] + "', " + entry[1] + ", " + entry[2] + ", " + entry[3] + ", " + entry[4] + ", " + entry[5] + "),\n")

    outStr = outStr[:-2]
    outStr += ";"
    return outStr


print("RUNNIN")
myList = getEntriesFromCSV("jeffbagwell_war_historical_2023.csv")
output = makeSQLUpdates(myList)
file = open("WARCREATE.txt", 'w')
if file.closed:
    print("An error occurred when trying to open/create the output file")

file.write(output)


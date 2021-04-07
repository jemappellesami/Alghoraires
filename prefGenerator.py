import csv, random

numbList = []
nStudent = 200
for i in range(1,6) :
    numbList.append(i)
    numbList.append(i+5)
    numbList.append(i+10)

dateList = [str(elem) + "/06/2021" for elem in numbList]
matricList = random.sample(range(400000, 500000), nStudent)
with open("preferences.csv", "w") as file :
    csvWriter = csv.writer(file)
    for matricule in matricList :
        toWrite = [matricule] + random.sample(dateList, 3)
        csvWriter.writerow(toWrite)
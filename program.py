import csv, random

class student :
    def __init__(self, matricule, date1, date2, date3):
        self.matricule = matricule
        self.date1 = date1
        self.date2 = date2
        self.date3 = date3
    
    def __init__(self, row) :
        self.matricule = row[0]
        self.date1 = row[1]
        self.date2 = row[2]
        self.date3 = row[3]

    def __str__(self) :
        return self.matricule
    
    def addDate(self,date) :
        self.allowedDate = date

    def appreciation(self) :
        if self.allowedDate == self.date1 :
            return 10
        elif self.allowedDate == self.date2 :
            return 7
        elif self.allowedDate == self.date3 :
            return 5
        else : 
            return -10


class chromosome :
    def __init__(self, studentList):
        self.studentList = studentList
    
    def computeScore(self) :
        score = 0
        for stud in self.studentList :
            score += stud.appreciation()
        return score
            

        

numbList = []
nStudent = 0 # sera incrémenté par après

# Dates par défaut : 01 juin à 05 juin, 08 juin à 12 juin
for i in range(1,6) :
    numbList.append(i)
    numbList.append(i+5)
    numbList.append(i+10)

dateList = [str(elem) + "/06/2021" for elem in numbList]
studentList = []
nParJour = 14

with open("preferences.csv", "r") as file :
    csvReader = csv.reader(file)
    for row in csvReader :
        studentList.append(student(row))

chrom = chromosome(studentList)
population = [chromosome(chrom.studentList.copy()) for i in range(10)]
for chromo in population:
    studList = []
    for stud in chromo.studentList :
        studList.append(str(stud))
    print(str(studList) + "\n")            


occupation = dict()
for date in dateList :
    occupation[date] = 0 

    
for stud in studentList :
    if(occupation[stud.date1] < nParJour) :
        #print("Préférence 1 pour l'étudiant {}".format(stud.matricule))
        stud.addDate(stud.date1)
        occupation[stud.date1] += 1

    elif (occupation[stud.date2] < nParJour) :
        #print("Préférence 2 pour l'étudiant {}".format(stud.matricule))
        stud.addDate(stud.date2)
        occupation[stud.date2] += 1
    
    elif (occupation[stud.date3] < nParJour) :
        #print("Préférence 3 pour l'étudiant {}".format(stud.matricule))
        stud.addDate(stud.date3)
        occupation[stud.date3] += 1

    else :
        date = random.sample(dateList, 1)[0]
        while occupation[date] > nParJour :
            date = random.sample(dateList, 1)[0]
        stud.addDate(date)
        occupation[date] += 1
        #print("Pour l'étudiant {} de date préférées {}, {}, {}, nous n'avons trouvé aucune date. Nous allons vers {}".format(stud.matricule, stud.date1, stud.date2, stud.date3, date))


"""
Two-point crossover
"""

def crossover(chrom1, chrom2) :
    size = len(chrom1.studentList)
    [x,y] = random.sample(range(size), 2)

    # Putting order if x > y
    if x > y :
        t = x
        x = y
        y = t

    print(chrom1.studentList)
    print(chrom2.studentList)

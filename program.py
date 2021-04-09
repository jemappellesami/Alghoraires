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


"""
Un chromosome est une liste d'étudiants pour lesquels on a attribué un horaire de passage pour l'exam.
Un chromosome est une "alternative" une proposition de solution au problème.
Donc pour calculer le score de ce chromosome, qui est l'appréciation globale de l'attribution d'horaires, on calcule le score par étudiant (cf. classe student)
"""
class chromosome :
    def __init__(self, studentList):
        self.studentList = studentList
    
    def __str__(self) :
        matricList = []
        for stud in self.studentList :
            matricList.append(str(stud))
        return str(matricList) + "\n"

    def computeScore(self) :
        score = 0
        for stud in self.studentList :
            score += stud.appreciation()
        return score
            

        
"""
Génération des dates : par défaut -> 01 juin à 05 juin, 08 juin à 12 juin
"""
numbList = []

for i in range(1,6) :
    numbList.append(i)
    numbList.append(i+5)
    numbList.append(i+10)

dateList = [str(elem) + "/06/2021" for elem in numbList]
nParJour = 14

"""
Réception des préférences via le fichier csv "preferences.csv" où les données commencent à la première ligne
"""
studentList = []

with open("preferences.csv", "r") as file :
    csvReader = csv.reader(file)
    for row in csvReader :
        # colonne = matricule, date1, date2, date3
        studentList.append(student(row))


"""
Génération d'une population de 10 chromosomes : 10 listes d'étudiants, dans un ordre aléatoire 
"""
population = []
for i in range(10) :
    copied = studentList.copy()
    random.shuffle(copied)
    population.append(chromosome(copied))



"""
Pour chaque chromosome dans la population, on commence par attribuer la date préférée au n°1 de la liste, puis on s'attaque au numéro 2, etc.
S'il y a un conflit (jour déjà complet), on passe à la 2eme date préférée. Etc.

Le problème est qu'ici, l'ordre dans la liste des étudiants compte. Mais ça ne sera pas un problème par la suite.
"""
for chrom in population :
    occupation = dict()
    for date in dateList :
        occupation[date] = 0 
    studentList = chrom.studentList
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
            #print("Pour l'étudiant {} de date préférées {}, {}, {}, nous n'avons trouvé aucune date. Nous allons vers {}".format(stud.matricule, stud.date1, stud.date2, stud.date3, date))
            stud.addDate(date)
            occupation[date] += 1

    #print(chrom.computeScore())


"""
Two-point crossover
"""

### CROSS OVER (cf. algorithm for Flowshop (INFO-H3000))
def cleanChromosome(givenChromosome, nLeft, nRight, matriculesToClean):
    print(nLeft, nRight)
    chrom = givenChromosome.studentList.copy()
    studentsToRemove = []

    """
    Here we generate list of students from chromosomes whose ID match the students from matriculesToClean

    Explanation : matriculesToClean comes from chromosome A, and we want to clean chromosome B. Students from chromosome A have a certain assigned date, thus
    they are not the same students as in chromosome B, even with the same ID.
    """
    for stud in matriculesToClean :
        for elem in givenChromosome.studentList :
            if elem.matricule == stud :
                studentsToRemove.append(elem)
    
    for stud in studentsToRemove :
        chrom.pop(chrom.index(stud))

    """
    Now we split our chromosome in two parts : right and left zone of the crossover.
    We fill the right zone by pushing all present genes to the left, then filling the right part (still in the zone
    located at the right of the exchange zone !) with the first gene of the "chromosome of lefts", until we reach
    length of the chromosome
    Then, we fill the left part with the remaining
    """
    listRight = []
    sizeListRight = len(givenChromosome.studentList) - nRight
    listLeft = []
    sizeListLeft = nLeft

    # Extracting genes from remaining chromosome to form the right part
    for gene in reversed(chrom) :
        if gene in givenChromosome.studentList[nRight:] :
            listRight.append(gene)
            chrom.pop(-1)
    listRight.reverse()

    # Extracting from remaining chromosome to build the remaining right part with the first genes of the remaining chrom
    while len(listRight) < sizeListRight :
        listRight.append(chrom[0])
        chrom.pop(0)

    # Remaining genes are the left part of the exchange
    listLeft = chrom
    return chromosome(listLeft + studentsToRemove + listRight)



def crossover(chrom1, chrom2) :
    size = len(chrom1.studentList)
    [x,y] = random.sample(range(size), 2)

    # Putting order if x > y
    if x > y :
        t = x
        x = y
        y = t
    toCleanFrom1 = (stud.matricule for stud in chrom2.studentList.copy()[x:y])
    toCleanFrom2 = (stud.matricule for stud in chrom1.studentList.copy()[x:y])

    firstChild = cleanChromosome(chrom1, x, y, toCleanFrom1)
    secondChild = cleanChromosome(chrom2, x, y, toCleanFrom2)

    return [firstChild, secondChild]




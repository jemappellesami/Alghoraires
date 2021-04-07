import random 

list = random.sample(range(40, 500), 15)

population = []
for i in range(10) :
    copied = list.copy()
    random.shuffle(copied)
    population.append(copied)

for item in population :
    print(item)
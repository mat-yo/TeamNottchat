import csv
long_arr = []
with open('food.csv', "rt", encoding='ascii') as infile:
    read = csv.reader(infile)
    for row in read:
        long_arr.append(row)
long_arr.pop(0)

malay_food = []
mamak_food = []
korean_food = []
japanese_food = []
beverage = []

for i in long_arr:
    #print(i[0])
    if (i[0] == "Malay"):
        malay_food.append(i)
    elif (i[0] == "Mamak"):
        mamak_food.append(i)
    elif (i[0] == "Beverage"):
        beverage.append(i)
    elif (i[0] == "Korean"):
        korean_food.append(i)
    elif (i[0] == "Japanese"):
        japanese_food.append(i)
        
print(malay_food,"\n----------------")
print(mamak_food,"\n----------------")
print(beverage,"\n----------------")
print(korean_food,"\n----------------")
print(japanese_food,"\n----------------")
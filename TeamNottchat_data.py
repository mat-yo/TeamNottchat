import csv

def categorize(intent):
    long_arr = []
    with open('TeamNottchat_food.csv', "rt", encoding='ascii') as infile:
        read = csv.reader(infile)
        for row in read:
            long_arr.append(row)
    long_arr.pop(0)

    malay_food = []
    mamak_food = []
    korean_food = []
    japanese_food = []
    beverage = []
    delivery=[]

    for i in long_arr:
        if (i[3] == "yes"):
            delivery.append(i)

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

    if (intent == "Malay"):
        return malay_food
    elif (intent == "Mamak"):
        return mamak_food
    elif (intent == "Beverage"):
        return beverage
    elif (intent == "Korean"):
        return korean_food
    elif (intent == "Japanese"):
        return japanese_food
    elif (intent == "delivery"):
        return delivery
    else:
        return False
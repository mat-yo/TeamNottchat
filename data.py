import pandas as pd

df = pd.read_csv(r'D:/Team nottchat/food.csv')

stall_name = df["stall_name"]

print(stall_name)

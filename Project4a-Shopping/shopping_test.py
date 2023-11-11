import csv
import sys

import shopping as sp

import pandas as pd

df = pd.read_csv('shopping.csv')


for column in df.columns:
    print(f"Column: {column}")
    print(df[column].unique())
    print()  # 為了更好的可讀性，添加空行


# sp.load_data("shopping_test.csv")

# sp.train_model(sp.load_data)

months = {
    "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "Jun": 5,
    "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
    }



# test_month = months["Jan"]

# print(test_month)


# list1 = [1, 2, 3]
# list2 = ['a', 'b', 'c']
# zipped = zip(list1, list2)
# print(zipped)  # <zip object at 0x7f27876a1240>

# # 遍歷配對的元組
# for i, (a, b) in enumerate(zipped):
#     print(i, a, b)
#     # 0 1 a
#     # 1 2 b
#     # 2 3 c

# # 將三個列表配對成元組
# list1 = [1, 2, 3]
# list2 = ['a', 'b', 'c']
# # list3 = [1.0, 2.0, 3.0]
# zipped = zip(list1, list2)
# print(zipped)


# for i in zipped:
#     print(i)


# sp.evaluate()
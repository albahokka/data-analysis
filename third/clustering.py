import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans

# Снимаем ограничение на вывод столбцов датафрейма
pd.set_option('display.max_columns', None)

# Загрузка данных из таблицы
df1 = pd.read_excel('statistics_indicators_2020.xlsx')

print(df1)


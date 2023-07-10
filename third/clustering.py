import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Снимаем ограничение на вывод столбцов датафрейма
pd.set_option('display.max_columns', None)

# Загрузка данных из таблицы
df1 = pd.read_excel('statistics_indicators_2020.xlsx')

# Замена всех значений null и удаление первых двух строк
df1.fillna(0, inplace=True)
df1 = df1.drop([0, 1])

# Осуществим определение весов для каждого признака
weights = {
    'Зп 2020 в % к 2019': 0.3,
    'Количество населения': 0.2,
    'Индекс роста зп': 0.15,
    'Объем жилищного строительства, млн': 0.1,
    'Годы жизни населения': 0.05,
    'Бедность 2018': 0.1,
    'Бедность 2019': 0.05,
    'Бедность 2020': 0.05
}

# Рассчитываем оценку губернатора методом агрегирования
df1['Оценка губернатора'] = df1.apply(lambda row: sum(row[col] * weights[col] for col in weights.keys()), axis=1)

# Находим минимальное и максимальное значение в колонке 'Оценка губернатора'
min_score = df1['Оценка губернатора'].min()
max_score = df1['Оценка губернатора'].max()

# Применяем минимаксную нормализацию к колонке 'Оценка губернатора'
df1['Оценка губернатора'] = (df1['Оценка губернатора'] - min_score) / (max_score - min_score)

# Выбор колонок для сегментации
columns_for_segmentation = ['Индекс роста зп']

# Создание модели K-средних
kmeans = KMeans(n_clusters=3, n_init=10)

# Обучение модели на данных
kmeans.fit(df1[columns_for_segmentation])

# Получение меток кластеров для каждой строки данных
labels = kmeans.labels_

# Добавление меток кластеров в исходный df
df1['Кластер'] = labels

# Построение графика для визуализации сегментации
plt.scatter(df1.index, df1['Индекс роста зп'], c=labels)
plt.xlabel('Регион')
plt.ylabel('Индекс роста зп')
plt.title('Сегментация регионов по индексу роста зп')
plt.show()

# Описание полученных кластеров
cluster_0 = df1[df1['Кластер'] == 0]
cluster_1 = df1[df1['Кластер'] == 1]
cluster_2 = df1[df1['Кластер'] == 2]

# Выведем краткую характеристику по кластерам с количеством регионов в них
df2 = df1.copy()
df2 = df2.drop('Регион', axis=1)

df2['KMeans'] = kmeans.labels_ + 1
res = df2.groupby('KMeans').mean()
res['Количество'] = df2.groupby('KMeans').size().values

res['Кластер'] = res['Кластер'].astype(int)

# Запись результатов в excel
res.to_excel('Результаты.xlsx', index=False)

# Выведем на экран регионы с минимальными оценками губернаторов
print(cluster_2['Регион'])
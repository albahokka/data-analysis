import pandas as pd

# Снимаем ограничение на вывод столбцов датафрейма
pd.set_option('display.max_columns', None)

# Создаем массив массивов из файла csv
rows = []
with open('Транзакции.csv', 'r') as csvfile:
    for line in csvfile:
        row = line.strip().split('\t')
        rows.append(row)

# Массив массивов преобразовываем в датафрейм
df = pd.DataFrame(rows[1:], columns=rows[0])
# print(df)

# Преобразование даты в формат datetime и добавление столбца "Month"
df['Date'] = pd.to_datetime(df['Date']).dt.date
df['Month'] = pd.to_datetime(df['Date']).dt.month

# Очистка других данных и преобразование столбцов в нужные типы данных
df['Paid'] = df['Paid'].str.replace(',', '.').astype(float)
df['Cost'] = df['Cost'].astype(float)
df['Доставка'] = df['Доставка'].astype(int)
df['Плохой отзыв'] = df['Плохой отзыв'].astype(int)
df['Promo'] = df['Promo'].astype(int)

# Отфильтруем заказы по отсутствию доставки в них
df = df[df['Доставка'] == 0]
df = df.reset_index(drop=True)


# print(df)
# print(df['Доставка'].unique())

# Расчет количество транзакций, процента плохих отзывов и доходности по месяцам и наличию/отсутствию промокода
result = df.groupby([df['Month'], 'Promo']).agg({
    'TransactionID': 'count',
    'Плохой отзыв': lambda x: x.sum() / x.count() * 100,
    'Paid': lambda x: (x.sum() - df['Cost'].sum()) / df['Cost'].sum() * 100
}).reset_index()

# Переименование столбцов
result.columns = ['Месяц', 'Введен промокод', 'Кол-во транзакций', 'Плохих отзывов, %', 'Доходность, %']
print(result)

# Запись результатов в excel
result.to_excel('Результаты.xlsx', index=False)
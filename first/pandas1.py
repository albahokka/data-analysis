import pandas as pd
import matplotlib.pyplot as plt
import random
import names

# assign data of lists
data = {'Process': ['Playing chess', 'Reading', 'Music', 'Walking', 'Sports',
                   'Walking', 'Vokals'],
        'Participant': [names.get_full_name() for name in range(7)],
        'Elapsed_time_min': [random.randint(1, 100) for time in range(7)]}

# create df from data
df = pd.DataFrame(data)
df1 = df.copy(deep=True)
print(df)

# show hist from df
df['Elapsed_time_min'].plot(kind='hist', bins=20, legend=True, color='red')
plt.show()

# нужно вывести две hist в одном окне, назвать оси
fig, axs = plt.subplots(nrows= 2 , ncols= 1 )
df.hist()
df.plot()
df1['Elapsed_time_min'].plot(kind='kde')
df1['Elapsed_time_min'].plot(kind='hist', bins=20)
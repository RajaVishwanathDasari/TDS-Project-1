import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('repositories.csv')
df['created_at'] = pd.to_datetime(df['created_at'])
df['year'] = df['created_at'].dt.year
language_trend = df.groupby(['year', 'language']).size().reset_index(name='count')
top_languages = language_trend.groupby('language')['count'].sum().nlargest(5).index
filtered_data = language_trend[language_trend['language'].isin(top_languages)]
pivot_data = filtered_data.pivot(index='year', columns='language', values='count').fillna(0)

# Plotting
plt.figure(figsize=(14, 8))  
sns.set_palette("husl")  
sns.lineplot(data=pivot_data, dashes=False)
plt.title('Trend of Programming Languages Over Years in repositories from Stockholm users', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Number of Repositories Created', fontsize=14)
plt.xticks(rotation=45)  
plt.legend(title='Programming Language', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
plt.grid()
plt.tight_layout()
plt.show()

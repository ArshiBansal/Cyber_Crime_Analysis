import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for black background and white text
plt.style.use('dark_background')
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['xtick.labelsize'] = 6
plt.rcParams['ytick.labelsize'] = 6
plt.rcParams['axes.labelsize'] = 8

# Read the Excel file
df = pd.read_excel('data-security-incidents-trends-q1-2019-to-q4-2024.xlsx')

# Show column names for quick debug
print("\n📁 Columns in Dataset:")
print(df.columns)

# Convert 'No. Data Subjects Affected' to numeric ranges
def convert_range_to_midpoint(range_str):
    if pd.isna(range_str):
        return np.nan
    range_str = str(range_str).strip()
    if 'to' in range_str:
        low, high = map(lambda x: int(x.replace('k', '000').replace(',', '')), range_str.split(' to '))
        return (low + high) / 2
    elif range_str == 'Unknown':
        return np.nan
    elif 'and above' in range_str:
        return float(range_str.replace(' and above', '').replace('k', '000').replace(',', ''))
    else:
        return float(range_str.replace('k', '000').replace(',', ''))

# Create the numerical column
df['No. Data Subjects Affected Num'] = df['No. Data Subjects Affected'].apply(convert_range_to_midpoint)

# === BASIC INFO SECTION ===

print("\n📌 Top 5 Rows of the Data:")
print(df.head())

print("\n📌 Bottom 5 Rows of the Data:")
print(df.tail())

print("\nℹ️ DataFrame Info:")
print(df.info())

print("\n📊 Basic Statistical Summary (Numerical Columns):")
print(df.describe())

print("\n❓ Missing Values by Column:")
print(df.isnull().sum())

print("\n🔥 Top 5 Most Frequent Incident Types:")
print(df['Incident Type'].value_counts().head(5))

print("\n🏢 Top 5 Sectors with Most Incidents:")
print(df['Sector'].value_counts().head(5))

print("\n💻 Cyber vs Non-Cyber Incident Counts:")
print(df['Incident Category'].value_counts())

print("\n📅 Average Number of Affected Subjects by Year:")
print(df.groupby('Year')['No. Data Subjects Affected Num'].mean().round(2))

print("\n✅ Decision Taken Counts:")
print(df['Decision Taken'].value_counts())

# === VISUALIZATION SECTION ===

# Create a figure with 8 subplots in a 2x4 grid
fig, axes = plt.subplots(2, 4, figsize=(22, 12))
fig.suptitle('Cyber Crime (2019-2024) Analysis', fontsize=20, y=1.00)

# 1. Bar Plot - Sector Distribution
sns.countplot(data=df, x='Sector', color='#9932CC', ax=axes[0, 0])
axes[0, 0].set_title('Distribution of Incidents by Sector')
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].set_xticklabels(axes[0, 0].get_xticklabels(), rotation=45, ha='right')
axes[0, 0].grid(False)

# 2. Horizontal Bar Chart - Decision Taken
decision_counts = df['Decision Taken'].value_counts()
sns.barplot(y=decision_counts.index, x=decision_counts.values,
            palette=['#E9967A', '#4682B4'], ax=axes[0, 1], orient='h')
axes[0, 1].set_title('Decision Taken Counts')
axes[0, 1].set_xlabel('Count')
axes[0, 1].set_ylabel('Decision Taken')
axes[0, 1].grid(False)

# 3. KDE Plot - Affected Subjects Distribution
sns.kdeplot(data=df, x='No. Data Subjects Affected Num',
            color='#B8860B', fill=True, ax=axes[0, 2])
axes[0, 2].set_title('Density of Affected Subjects')
axes[0, 2].grid(False)

# 4. Pie Chart - Cyber vs Non-Cyber
cyber_counts = df['Incident Category'].value_counts()
axes[0, 3].pie(cyber_counts, labels=cyber_counts.index,
               colors=['#006400', '#90EE90'], autopct='%1.1f%%', startangle=90)
axes[0, 3].set_title('Cyber vs Non-Cyber Incident Counts')
axes[0, 3].axis('equal')

# 5. Violin Plot - Affected Subjects by Year
sns.violinplot(data=df, x='Year', y='No. Data Subjects Affected Num',
               color='#00CED1', ax=axes[1, 0])
axes[1, 0].set_title('Affected Subjects Distribution by Year')
axes[1, 0].tick_params(axis='x', rotation=0)
axes[1, 0].grid(False)

# 6. Bar Plot - Top 5 Incident Types
top_incidents = df['Incident Type'].value_counts().head(5)
sns.barplot(x=top_incidents.index, y=top_incidents.values,
            color='#8FBC8F', ax=axes[1, 1])
axes[1, 1].set_title('Top 5 Incident Types by Frequency')
axes[1, 1].tick_params(axis='x', rotation=45)
axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=45, ha='right')
axes[1, 1].grid(False)

# 7. Stacked Bar - Incident Category by Sector
sector_incident = pd.crosstab(df['Sector'], df['Incident Category'])#pivot table
sector_incident.plot(kind='bar', stacked=True, color=['#8B0000', '#F08080'],
                     ax=axes[1, 2], legend=False)
axes[1, 2].set_title('Incident Category by Sector')
axes[1, 2].tick_params(axis='x', rotation=45)
axes[1, 2].set_xticklabels(axes[1, 2].get_xticklabels(), rotation=45, ha='right')
axes[1, 2].set_ylabel('Count')
axes[1, 2].grid(False)

# 8. Line Plot - Trend of Affected Subjects Over Quarters
df['Year-Quarter'] = df['Year'].astype(str) + ' ' + df['Quarter']
quarterly_avg = df.groupby('Year-Quarter')['No. Data Subjects Affected Num'].mean().dropna()
axes[1, 3].plot(quarterly_avg.index, quarterly_avg.values, color='#008B8B', marker='o')
axes[1, 3].set_title('Trend of Average Affected Subjects Over Quarters')
axes[1, 3].tick_params(axis='x', rotation=45)
if len(quarterly_avg) > 10:
    axes[1, 3].set_xticks(range(0, len(quarterly_avg), 2))
    axes[1, 3].set_xticklabels(quarterly_avg.index[::2], rotation=45, ha='right')
axes[1, 3].set_ylabel('Average No. of Affected Subjects')
axes[1, 3].grid(False)

# Adjust layout and spacing
plt.tight_layout(pad=3.0)
fig.subplots_adjust(hspace=0.75)
plt.show()

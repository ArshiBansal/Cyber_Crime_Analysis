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
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7

# Read the Excel file
df = pd.read_excel('data-security-incidents-trends-q1-2019-to-q4-2024.xlsx')  # Update path if needed

# Convert 'No. Data Subjects Affected' to numeric midpoints
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

df['No. Data Subjects Affected Num'] = df['No. Data Subjects Affected'].apply(convert_range_to_midpoint)

# Basic Info
# 1. Top 5 Rows
print("\n📌 Top 5 Rows of the Data:")
print(df.head())

# 2. Bottom 5 Rows
print("\n📌 Bottom 5 Rows of the Data:")
print(df.tail())

# 3. DataFrame Info
print("\nℹ️ DataFrame Info:")
print(df.info())

# 4. Basic Statistics
print("\n📊 Basic Statistical Summary (Numerical Columns):")
print(df.describe())

# 5. Missing Values Count
print("\n❓ Missing Values by Column:")
print(df.isnull().sum())

# 6. Top 5 Most Frequent Incident Types
print("\n🔥 Top 5 Most Frequent Incident Types:")
print(df['Incident Type'].value_counts().head(5))

# 7. Top 5 Sectors with Most Incidents
print("\n🏢 Top 5 Sectors with Most Incidents:")
print(df['Sector'].value_counts().head(5))

# 8. Cyber vs Non-Cyber Incident Counts
print("\n💻 Cyber vs Non-Cyber Incident Counts:")
print(df['Incident Category'].value_counts())

# 9. Average Affected Subjects by Year
print("\n📅 Average Number of Affected Subjects by Year:")
print(df.groupby('Year')['No. Data Subjects Affected Num'].mean().round(2))

# 10. Most Common Decision Taken
print("\n✅ Decision Taken Counts:")
print(df['Decision Taken'].value_counts())
# Helper function to show chart
def show_chart():
    plt.tight_layout(pad=2.0)
    plt.show()
    plt.close()

# 1. Hist Plot - Sector Distribution (Color: Dark Orchid)
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Sector', color='#9932CC', discrete=True, shrink=0.8)
plt.title('Distribution of Incidents by Sector')
plt.xticks(rotation=45, ha='right')
plt.grid(False)
show_chart()

# 2. Horizontal Bar Chart - Decision Taken Proportions (Colors: Dark Salmon, Steel Blue)
plt.figure(figsize=(10, 6))
decision_counts = df['Decision Taken'].value_counts()
sns.barplot(y=decision_counts.index, x=decision_counts.values, palette=['#E9967A', '#4682B4'], orient='h')
plt.title('Decision Taken Counts')
plt.xlabel('Count')
plt.ylabel('Decision Taken')
plt.grid(False)
show_chart()

# 3. KDE Plot - Affected Subjects Distribution (Color: Dark Goldenrod)
plt.figure(figsize=(10, 6))
sns.kdeplot(data=df, x='No. Data Subjects Affected Num', color='#B8860B', fill=True)
plt.title('Density of Affected Subjects')
plt.grid(False)
show_chart()

# 4. Pie Chart - Cyber vs Non-Cyber Incident Counts (Colors: Dark Green, Light Green)
plt.figure(figsize=(5, 5))
cyber_counts = df['Incident Category'].value_counts()
plt.pie(cyber_counts, labels=cyber_counts.index, colors=['#006400', '#90EE90'], autopct='%1.1f%%', startangle=90)
plt.title('Cyber vs Non-Cyber Incident Counts')
plt.axis('equal')
show_chart()

# 5. Violin Plot - Affected Subjects by Year (Color: Dark Turquoise)
plt.figure(figsize=(10, 6))
sns.violinplot(data=df, x='Year', y='No. Data Subjects Affected Num', color='#00CED1')
plt.title('Affected Subjects Distribution by Year')
plt.xticks(rotation=0)
plt.grid(False)
show_chart()

# 6. Bar Plot - Top 5 Incident Types by Count (Color: Dark Sea Green)
plt.figure(figsize=(10, 6))
top_incidents = df['Incident Type'].value_counts().head(5)
sns.barplot(x=top_incidents.index, y=top_incidents.values, color='#8FBC8F')
plt.title('Top 5 Incident Types by Frequency')
plt.xticks(rotation=45, ha='right')
plt.grid(False)
show_chart()

# 7. Stacked Bar Chart - Incident Category by Sector (Colors: Dark Red, Light Coral)
sector_incident = pd.crosstab(df['Sector'], df['Incident Category'])
sector_incident.plot(kind='bar', stacked=True, color=['#8B0000', '#F08080'], figsize=(12, 6))
plt.title('Incident Category by Sector')
plt.xticks(rotation=45, ha='right')
plt.ylabel('Count')
plt.grid(False)
show_chart()

# 8. Line Plot - Trend of Affected Subjects Over Quarters (Color: Dark Cyan)
plt.figure(figsize=(10, 6))
df['Year-Quarter'] = df['Year'].astype(str) + ' ' + df['Quarter']
quarterly_avg = df.groupby('Year-Quarter')['No. Data Subjects Affected Num'].mean().dropna()
plt.plot(quarterly_avg.index, quarterly_avg.values, color='#008B8B', marker='o')
plt.title('Trend of Average Affected Subjects Over Quarters')
plt.xticks(rotation=45, ha='right')
if len(quarterly_avg) > 10:
    plt.xticks(ticks=range(0, len(quarterly_avg), 2), labels=quarterly_avg.index[::2])
plt.ylabel('Average No. of Affected Subjects')
plt.grid(False)
show_chart()

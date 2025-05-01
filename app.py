import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# import cleaned dataset
accident = pd.read_csv('RTA_cleaned.csv')

# ------------------------------------------------------------------------------------------------------
# 2. Preparation: define dataset, color maps, categories, etc.

# define plot color maps
from matplotlib import colors
color_map2 = colors.LinearSegmentedColormap.from_list('custom', ['#B2DFBC', '#3D3D3D'])
color_map3 = colors.LinearSegmentedColormap.from_list('custom', ['#B2DFBC', '#3D3D3D', '#441E1A'])
color_map4 = colors.ListedColormap(['#A3D0AD', '#9DB379', '#909548', '#7A6638', '#441E1A'])
color_map5 = colors.ListedColormap(['#72C083', '#ACCA75', '#C9CF6E', '#E6D367', '#B09D50', '#7a6638', '#5d2823'])
color_map6 = colors.ListedColormap(['#72C083', '#B6C185', '#B8B35C', '#958f4a', '#7a6638', '#5d2823'])

# defines group categories
road = ['Lanes_or_Medians', 'Road_allignment', 'Types_of_Junction', 'Road_surface_type']
vehicle = ['Type_of_vehicle', 'Service_year_of_vehicle', 'Defect_of_vehicle', 'Vehicle_movement']
environment = ['Day_of_week', 'Road_surface_conditions', 'Light_conditions', 'Weather_conditions', 'Area_accident_occured']
driver = ['Age_band_of_driver', 'Sex_of_driver', 'Educational_level', 'Driving_experience',  'Owner_of_vehicle', 'Cause_of_accident']

consequences = ['Type_of_collision', 'Number_of_vehicles_involved', 'Number_of_casualties', 'Casualty_class', 'Age_band_of_casualty', 'Sex_of_casualty', 'Accident_severity']

# create groupby iteration, so the visualization will be ordered descending
categories = [road, vehicle, environment, driver, consequences]

accident[['Number_of_vehicles_involved', 'Number_of_casualties']] = accident[['Number_of_vehicles_involved', 'Number_of_casualties']].astype(str)
for i in categories:
    for j in i:
        globals()['table_%s' %j] = accident.groupby([j])['Time'].count().sort_values(ascending=False).reset_index().rename(columns={'Time':'count'})

# defines groupby categories again that was created before. NOTE: must run the i j iteration first!
road_tables = [table_Lanes_or_Medians, table_Road_allignment, table_Types_of_Junction, table_Road_surface_type] # type: ignore
vehicle_tables = [table_Type_of_vehicle, table_Service_year_of_vehicle, table_Defect_of_vehicle, table_Vehicle_movement] # type: ignore
environment_tables = [table_Day_of_week, table_Road_surface_conditions, table_Light_conditions, table_Weather_conditions, table_Area_accident_occured] # type: ignore
driver_tables = [table_Age_band_of_driver, table_Sex_of_driver, table_Educational_level, table_Driving_experience,  table_Owner_of_vehicle, table_Cause_of_accident] # type: ignore

consequences_tables = [table_Type_of_collision, table_Number_of_vehicles_involved, table_Number_of_casualties, table_Casualty_class, table_Age_band_of_casualty, table_Sex_of_casualty, table_Accident_severity] # type: ignore

# define date and hours
accident['Time'] = pd.to_datetime(accident['Time'])
accident['Hour_of_day'] = accident['Time'].dt.hour
accident['Weekday-weekend'] = np.where(accident['Day_of_week'].isin(['Saturday','Sunday']), 'Weekend', 'Weekday')
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
accident_order = ['Slight Injury', 'Serious Injury', 'Fatal injury']

# ------------------------------------------------------------------------------------------------------
# 3. Plots

# distribution plots
# roads
sns.set_style('whitegrid')
road_plot = plt.figure(figsize=(16,8), dpi=150)
plt.suptitle('Road Category Distribution', y = 1, fontsize = 18)
for i in range(0, len(road_tables)):
    plt.subplot(2, 2, i+1)
    ax = sns.barplot(
        y = road_tables[i][road[i]],
        x = 100*(round(road_tables[i]['count'] / road_tables[i]['count'].sum(),4)),
        width=0.8,
        color='#6FC381'
    )
    for container in ax.containers:
        ax.bar_label(container) # type: ignore
    plt.yticks(fontsize = 14)
    plt.ylabel(ylabel = road[i], fontsize = 14)
    plt.tight_layout()
    plt.xlabel('Percentage(%)')
plt.show()
road_explain = '''
        - Straight, clean road are common for traffic accident to be happened
        - Road with improper markings (no/broken lines) supports traffic accident to be happened
    '''

# vehicle
sns.set_style('whitegrid')
vehicle_plot = plt.figure(figsize=(18,10), dpi=150)
plt.suptitle('Vehicle Category Distribution', y = 1, fontsize = 18)
for i in range(0, len(road_tables)):
    plt.subplot(2, 2, i+1)
    ax = sns.barplot(
        y = vehicle_tables[i][vehicle[i]],
        x = 100*(round(vehicle_tables[i]['count'] / vehicle_tables[i]['count'].sum(),4)),
        width=0.8,
        color='#6FC381'
    )
    for container in ax.containers:
        ax.bar_label(container, fontsize = 13) # type: ignore
    plt.yticks(fontsize = 14)
    plt.ylabel(ylabel = vehicle[i], fontsize = 14)
    plt.tight_layout()
    plt.xlabel('Percentage (%)')
plt.show()
vehicle_explain = '''
- Automobile/cars are common for traffic accidents to be happened
- Cars that went straight are the most common for traffic accidents
- Apparently, vehicles with defects didn't contribute much into traffic accidents happened
'''

# environment
sns.set_style('whitegrid')
accident['Hour_of_day'] = accident['Time'].dt.hour
environment_plot = plt.figure(figsize=(16,18), dpi=150)
plt.suptitle('Environment Category Distribution', y = 1, fontsize = 18)
for i in range(0, len(environment_tables)):
    plt.subplot(3, 2, i+1)
    ax = sns.barplot(
        y = environment_tables[i][environment[i]],
        x = 100*(round(environment_tables[i]['count'] / environment_tables[i]['count'].sum(),4)),
        width=0.8,
        color='#6FC381'
    )
    for container in ax.containers:
        ax.bar_label(container, fontsize = 13) # type: ignore
    plt.yticks(fontsize = 14)
    plt.ylabel(ylabel = environment[i], fontsize = 14)
    plt.tight_layout()
    plt.xlabel('Percentage (%)')
plt.subplot(3, 2, 6)
plt.hist(accident['Hour_of_day'],
          color= '#6FC381',
          bins=24,
          stacked=True, 
          alpha=0.9)
plt.xlabel('Time (Hours)')
plt.ylabel(ylabel = 'Hour_of_day', fontsize = 14)
plt.xticks(list(range(0,24,1)), fontsize = 12)
plt.show()
environment_explain = '''
- Apparently, normal conditions (dry roads, daylight, normal weather) are mostly when the accident happened
- Office areas are the common area that traffic accidents to be happened.
- Accidents mostly happened during rush hour (around 08:00 and 16:00 - 18:00)
'''

# driver
sns.set_style('whitegrid')
driver_plot = plt.figure(figsize=(16,18), dpi=150)
plt.suptitle('Driver Category Distribution', y = 1, fontsize = 18)
for i in range(0, len(driver_tables)):
    plt.subplot(3, 2, i+1)
    ax = sns.barplot(
        y = driver_tables[i][driver[i]],
        x = 100*(round(driver_tables[i]['count'] / driver_tables[i]['count'].sum(),4)),
        width=0.8,
        color='#6FC381'
    )
    for container in ax.containers:
        ax.bar_label(container, fontsize = 13) # type: ignore
    plt.yticks(fontsize = 14)
    plt.ylabel(ylabel = driver[i], fontsize = 14)
    plt.tight_layout()
    plt.xlabel('Percentage (%)')
plt.show()
driver_explain = '''
- The majority of drivers are males with age range around young adults to adults.
- Most cause of accidents are happened because of no distancing between vehicle and changing lanes, followed by driving carelessly
- Apparently, drivers with more experience are the most drivers that involved in accidents.
- The majority of drivers' last education are below high school.
'''

# consequence
sns.set_style('whitegrid')
consequences_plot = plt.figure(figsize=(16,22), dpi=150)
plt.suptitle('Consequences Category Distribution', y = 1, fontsize = 18)
for i in range(0, len(consequences_tables)):
    plt.subplot(4, 2, i+1)
    ax = sns.barplot(
        y = consequences_tables[i][consequences[i]],
        x = 100*(round(consequences_tables[i]['count'] / consequences_tables[i]['count'].sum(),4)),
        width=0.8,
        color='#6FC381'
    )
    for container in ax.containers:
        ax.bar_label(container, fontsize = 13) # type: ignore
    plt.yticks(fontsize = 14)
    plt.ylabel(ylabel = consequences[i], fontsize = 14)
    plt.tight_layout()
    plt.xlabel('Percentage (%)')
plt.show()
consequences_explain = '''
- Collisions between vehicles are the most common type of collision.
- 84.6% of the accidents are considered a slight accident, meaning most of the survivors are neither serious nor fatal injury (hospitalized or death), while;
- 68% of accidents are having at least casualties or injured of 1 person per accident
'''

# Time and Severity 
# Day
day_severity = accident.groupby(['Day_of_week', 'Accident_severity'])['Time'].count().reset_index().sort_values(by = 'Time', ascending=False).rename(columns={'Time':'count'})
day_severity['percent'] = 100*(round(day_severity['count'] / day_severity['count'].sum(), 4))
day_severity_pivot = day_severity.pivot_table(columns='Day_of_week', index= 'Accident_severity', values='percent', fill_value = 0)
day_severity_pivot = day_severity_pivot.reindex(accident_order)
day_severity_pivot = day_severity_pivot.reindex(day_order, axis= 1)

day_plot = plt.figure(figsize=(7,3), dpi = 120)
sns.set_style('white')
sns.heatmap(day_severity_pivot, 
            cmap= color_map2, 
            vmax = 13, 
            annot=True, 
            fmt= '.1f', 
            linewidths=0.5, 
            linecolor='#CFD1C7', 
            cbar=False)
plt.show()
day_explain = '''
Apparently, fatal accident on weekends (Saturday - Sunday) is 0.2% occurs more often than weekdays.
'''

# Hour
hour_plot = plt.figure(figsize=(7,7), dpi = 120)
sns.set_style('whitegrid')
plt.title('Time Accident Distribution and Its Severity')
plt.hist([accident[accident['Accident_severity'] == 'Fatal injury']['Hour_of_day'],
          accident[accident['Accident_severity'] == 'Serious Injury']['Hour_of_day'],
          accident[accident['Accident_severity'] == 'Slight Injury']['Hour_of_day']],
          color= ['#6A352F','#8B826F','#6FC381'],
          bins=24,
          stacked=True, 
          alpha=0.8)
plt.legend(['Fatal injury', 'Serious Injury', 'Slight Injury'], title = 'Accident Severity', loc= 2)
plt.xlabel('Time (Hours)')
plt.xticks(list(range(0,24,1)), fontsize = 11)
plt.ylabel('Count')
plt.show()
hour_explain = '''
Most accidents are happened during the rush hour (08:00 and 17:00).
'''

# week
week_plot = plt.figure(figsize=(7,7), dpi = 120)
sns.set_style('whitegrid')
plt.title('Week Accident Distribution')
sns.histplot(x = accident['Hour_of_day'],
             hue= accident['Weekday-weekend'],
             hue_order= ['Weekend', 'Weekday'],
             palette= ['#7A6638', '#9DB379'],
             kde=True,
             bins=24, 
             alpha=0.8)
plt.xlabel('Time (Hours)')
plt.xticks(list(range(0,24,1)), fontsize = 11)
plt.ylabel('Count')
plt.show()
week_explain = '''
On weekends, accidents on midnight occurs more often than weekdays.
'''

# ------------------------------------------------------------------------------------------------------
# 4. Layout

st.title('Road Traffic Accident Report and Severity Prediction')
st.markdown('Based on World Health Organization (WHO), there are factors that influences road traffic accident and the risk of it, which divided into four categories:')
st.markdown('- **Road Category**, such as the road width, markings, alignment, layout, and surface material.')
st.markdown('- **Vehicle Category**, such as vehicle type, condition, and movement.')
st.markdown('- **Environment Category**, such as time, weather, location, surface condition, and lighting.')
st.markdown('- **Driver Category**, such as age, sex, attitudes, ownership of vehicle, fatigue, and alcohol level.')
st.markdown('In this project, available columns in the dataset from kaggle can be grouped into categories above, along with ***the effect*** of the the accidents, such as type of collisions, number of vehicle and casualties involved, and the accident severity itself.')
st.subheader('Top Causes of Road Traffic Accident on each Category')

plots_key = ('Road', 'Vehicle', 'Environment', 'Driver', 'Effects')
plots = (road_plot, vehicle_plot, environment_plot, driver_plot, consequences_plot)
explain = (road_explain, vehicle_explain, environment_explain, driver_explain, consequences_explain)

cause = st.selectbox(
    'Select Category',
    plots_key,
    index=None,
    placeholder='Select category here...'
)

for i in range(0, len(plots)):
    if cause == plots_key[i]:
        st.pyplot(plots[i])
        with st.expander("Key Takeaways"):
            st.markdown(explain[i])


st.subheader('Road Traffic Accident Based on Day-of-week and Hour-of-time')

day_key = ('Hour', 'Day', 'Week')
plots_date = (hour_plot, day_plot, week_plot)
explain_date = (hour_explain, day_explain, week_explain)

day_hour_week = st.selectbox(
    'Select between Hours, Days, and Week (result in days are percentage (%))',
    day_key,
    index=None,
    placeholder='Select here...'
)

for i in range(0, len(plots_date)):
    if day_hour_week == day_key[i]:
        st.pyplot(plots_date[i])
        with st.expander("Key Takeaways"):
            st.markdown(explain_date[i])
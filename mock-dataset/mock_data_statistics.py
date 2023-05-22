from collections import OrderedDict
import category_encoders
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import re

def isDigit(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ isDigit(c) for c in re.split(r'(\d+)', text) ]

def combine_df_columns(df):
    columns = df.columns

    results = dict()

    for column in columns:
        results[column] = 0
        row_with_column = df[column]
        for row in row_with_column:
            if row is 1:
                results[column] = results[column] + 1

    return results

#for column in columns:
#    df

mock_data_file = "./mock_data.json"

all_events = []
all_sensors = []

#Open database, feature select, save events
with open(mock_data_file, 'r') as json_read:
    for row in json_read:
        data_entry = json.loads(row)
        all_events.append(data_entry['event'])
        all_sensors.append(data_entry['sensor'])

#Remove duplicates to get unique events/sensors
unique_events = list(dict.fromkeys(all_events))
unique_sensors = list(dict.fromkeys(all_sensors))

#Use humansorting on events/sensors
unique_events.sort(key=natural_keys)
unique_sensors.sort(key=natural_keys)
all_sensors.sort(key=natural_keys)
all_events.sort(key=natural_keys)

unique_sensors_dataframe = pd.DataFrame(data=unique_sensors, columns=['sensor'])
all_sensors_dataframe = pd.DataFrame(data=all_sensors, columns=['sensor'])
unique_events_dataframe = pd.DataFrame(data=unique_events, columns=['event'])
all_events_dataframe = pd.DataFrame(data=all_events, columns=['event'])

sensor_encoder = category_encoders.OneHotEncoder(cols=['sensor'])
event_encoder = category_encoders.OneHotEncoder(cols=['event'])
sensor_encoder.fit(unique_sensors_dataframe)
event_encoder.fit(unique_events_dataframe)

sensors_classes = sensor_encoder.transform(unique_sensors_dataframe)
encoded_sensors = sensor_encoder.transform(all_sensors_dataframe)

event_classes = event_encoder.transform(unique_events_dataframe)
encoded_events = event_encoder.transform(all_events_dataframe)

sensor_results = combine_df_columns(encoded_sensors)
event_results = combine_df_columns(encoded_events)
event_results2 = dict()





print(sensors_classes)
print(event_classes)

i = 1
for event in event_results:
    event_results2[i] = event_results[event]
    i = i + 1

event_results = event_results2

fig, sensor_plot = plt.subplots()
fig, event_plot = plt.subplots()
sensor_plot.bar(list(sensor_results.keys()), sensor_results.values(), color='b')
sensor_plot.set_xlabel("Sensor classes")
sensor_plot.set_ylabel("Occurency of sensor in events")

event_plot.bar(list(event_results.keys()), event_results.values(), color='b')
event_plot.set_xlabel("Event classes")
event_plot.set_ylabel("Amount of events")
plt.tight_layout()
plt.show()

import json
import numpy as np
from pprint import pprint
from pathlib import Path
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from operator import attrgetter
from sklearn.datasets import load_boston

I = 1
PATH_TO_MOCK_DATA = "../mock-dataset/mock_data.json"
WINDOW_SIZE = 30 * I

def convert_list_of_dicts(lod, keylist):
    return [[row[key] for key in keylist] for row in lod]

def reshape_events(events):
    for i in range(len(events)):
        e = events[i]
        events[i] = [e[i:i+3] for i in range(0, len(e), 3)]
    return events

""" Sort events according to timestamp so that they can be put into the neural networks """
def sort_events(data):
    data.sort(key=lambda e: e['timestamp'])
    pass

""" Transforms the labeled data using the OneHotEncoder from scikit """
def encode(data):
    X = np.stack(data)
    Y = list()
    for i in range(len(X)):
        Y.append(X[i][0])

    enc = OneHotEncoder()
    transformed_data = enc.fit_transform(Y).toarray()

    for i in range(len(X)):
        X[i][0] = transformed_data[i].tolist()

    return X

def read_into_window(data, index):
    window = list()
    
    start = index * WINDOW_SIZE
    end = start + WINDOW_SIZE

    for i in range(start, end):
        current = data[i]
        dataArray = [
            current[0],
            current[1]
        ]
        window.append(dataArray)
    return window

with open(Path(PATH_TO_MOCK_DATA)) as json_file:
    data = json.load(json_file)
    sort_events(data)

    """ Format the data so that it can be handled by the OneHotEncoder """
    events = convert_list_of_dicts(data, ['event', 'sensor', 'sensor_group', 'timestamp'])
    reshaped_events = reshape_events(events)

    """ Encode events """
    encoded_events = encode(reshaped_events)
    
    """ Data to be written to output file """ 
    output = {}

    """ Read a number of events into a window, starting at 0, that will be used as input for the neural networks """
    index = 0
    window = read_into_window(encoded_events, index)

    output['events'] = window

    with open('output.json', 'w') as outfile:
        json.dump(output, outfile)

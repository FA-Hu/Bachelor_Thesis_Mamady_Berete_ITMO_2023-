import os, sys, random, json

def fix_time_string(time_to_fix, hour):
	if time_to_fix is 24 and hour:
		time_to_fix = "00"
	elif time_to_fix >= 0 and time_to_fix <= 9:
		time_to_fix = "0" + str(time_to_fix)
	else:
		time_to_fix = str(time_to_fix)
	
	return time_to_fix

def random_timestamp():
	year_month = "1999-03-"
	day = random.randint(8,12)

	if day is 8 or day is 9:
		day = "0" + str(day)
	else:
		day = str(day)

	hour = fix_time_string(random.randint(6,24), True)
	minute = fix_time_string(random.randint(0,59), False)
	second = fix_time_string(random.randint(0,59), False)

	return year_month + day + " " + hour + ":" + minute + ":" + second

def darpa_convert_timestamp(date, time):
	split_date = date.split('/')
	return split_date[2] + "-" + split_date[1] + "-" + split_date[0] + " " + time

malware_names_file = "./MalwareTrainingSets-master/malware_names.csv"
darpa_attacks_file = "./darpa-1999/IDS_events.csv"
output_json = "./mock_data.json"

mock_data = []
event_id = 1

with open(darpa_attacks_file, mode='r') as darpa_read:				
	for row in darpa_read:
		split_row = row.split(';')

		mock_data.append(dict(event = 'E' + str(event_id),
		sensor = 'S' + str(random.randint(11,12)),
		sensor_group = 'G1',
		timestamp = darpa_convert_timestamp(split_row[1],split_row[2])
		))
		event_id = event_id + 1

with open(malware_names_file, mode='r') as malware_read:				
	for row in malware_read:
		random_event_id = random.randint(1, event_id)
		mock_data.append(dict(event = 'E' + str(random_event_id),
		sensor = 'S' + str(random.randint(1,10)),
		sensor_group = 'G2',
		timestamp = random_timestamp()
		))
		

random.shuffle(mock_data)

with open(output_json, 'w') as results_write:
	for row in mock_data:
		json.dump(row, results_write)
		results_write.write('\n')

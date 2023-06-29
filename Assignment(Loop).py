#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
from datetime import datetime
from pytz import timezone, utc
from flask import Flask, jsonify, request

app = Flask(__name__)

# Step 1: Read store status data from CSV
def read_store_status(filename):
    store_status = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            store_id = int(row[0])
            timestamp_utc = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
            status = row[2]
            store_status.append((store_id, timestamp_utc, status))
    return store_status

# Step 2: Read business hours data
def read_business_hours(filename):
    business_hours = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            store_id = int(row[0])
            day_of_week = int(row[1])
            start_time_local = datetime.strptime(row[2], '%H:%M:%S').time()
            end_time_local = datetime.strptime(row[3], '%H:%M:%S').time()
            business_hours.setdefault(store_id, {})[day_of_week] = (start_time_local, end_time_local)
    return business_hours

# Step 3: Read timezone data
def read_timezone_data(filename):
    timezone_data = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            store_id = int(row[0])
            timezone_str = row[1]
            timezone_data[store_id] = timezone_str
    return timezone_data

# Step 4: Calculate the number of times stores were inactive during business hours
def calculate_inactive_count(store_id, store_status, business_hours, timezone_data):
    timezone_str = timezone_data.get(store_id, 'America/Chicago')
    tz = timezone(timezone_str)
    inactive_count = 0
    if store_id in business_hours:
        for status in store_status:
            if status[0] == store_id:
                timestamp_utc = status[1]
                local_time = timestamp_utc.astimezone(tz)
                day_of_week = local_time.weekday()
                start_time_local, end_time_local = business_hours[store_id].get(day_of_week, (datetime.min.time(), datetime.max.time()))
                if local_time.time() >= start_time_local and local_time.time() <= end_time_local:
                    if status[2] == 'inactive':
                        inactive_count += 1
    return inactive_count

# Endpoint 1: Get the report of the number of times each store went inactive during its business hours
@app.route('/report', methods=['GET'])
def get_report():
    store_status = read_store_status('store_status.csv')
    business_hours = read_business_hours('business_hours.csv')
    timezone_data = read_timezone_data('timezone_data.csv')
    report = {}
    for store_id in business_hours.keys():
        inactive_count = calculate_inactive_count(store_id, store_status, business_hours, timezone_data)
        report[store_id] = inactive_count
    return jsonify(report)

# Endpoint 2: Get the store status for a specific store and timestamp
@app.route('/status', methods=['GET'])
def get_store_status():
    store_id = int(request.args.get('store_id'))
    timestamp_utc = datetime.strptime(request.args.get('timestamp_utc'), '%Y-%m-%d %H:%M:%S')
    store_status = read_store_status('store_status.csv')
    timezone_data = read_timezone_data('timezone_data.csv')
    timezone_str = timezone_data.get(store_id, 'America/Chicago')
    tz = timezone(timezone_str)
    utc_time = timestamp_utc.replace(tzinfo=utc)
    local_time = utc_time.astimezone(tz)
    status = 'unknown'
    for store_status_entry in store_status:
        if store_status_entry[0] == store_id and store_status_entry[1] == utc_time:
            status = store_status_entry[2]
            break
    return jsonify({
        'store_id': store_id,
        'timestamp_utc': timestamp_utc.strftime('%Y-%m-%d %H:%M:%S'),
        'status': status,
        'local_time': local_time.strftime('%Y-%m-%d %H:%M:%S'),
        'timezone': timezone_str
    })


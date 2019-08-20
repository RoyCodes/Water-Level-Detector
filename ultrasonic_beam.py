#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import required libraries, including python-requests and hcsr04.py
import csv, os, sys, time, requests, json, hcsr04, led

# Helper function for generating timestamps in ISO 8601 format
def get_utc_timestamp(seconds=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))

# Set a default interval of 5 seconds. If the script was run with an argument,
# such as "python ultrasonic_harvest.py 2", use that value instead.
interval=5 if len(sys.argv)==1 else int(sys.argv[1])

print("Starting distance measurement! Press Ctrl+C to stop this script.")
time.sleep(1)

# Cleaning up from the last time. Delete old sensor data if file exists.
if os.path.exists("sensorhistory.csv"):
    os.remove("sensorhistory.csv")

while True:
    print("***")
    # Tracking the current time so we can loop at regular intervals.
    loop_start_time = time.time()

    # Reading the distance using the read_distance function from hcsr04.py.
    distance = hcsr04.read_distance()

    # Set the HTTP request header and payload content
    headers = {"Content-Type": "application/json"}
    payload = {"timestamp": get_utc_timestamp(), "value": round(distance * 10) / 10}

    # Saving the sensor reading to a CSV file.
    csv_columns = ["timestamp", "value"]

    try:
        with open('sensorhistory.csv', 'a+') as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            # writer.writeheader()
            writer.writerow(payload)
    except IOError:
        print("I/O error") 
    f.close()

    # Printing distance reading from sensor in cm
    print("Distance: {} cm".format(distance))

    try:
        # Opening our CSV file of sensor readings.
        csvfile = open('sensorhistory.csv', 'r')

        # Turning the readings from the file into a dictionary object
        reader = csv.DictReader( csvfile, fieldnames=csv_columns)

        sensordata = list(reader)
        sensordatacount = 0
        for i in sensordata:
            sensordatacount += 1

        # Printing current length of CSV file.
        print("Current count of sensor readings: {}".format(sensordatacount))

        # Anomaly Detector API requires a minimum of 12 values. Once we have enough, POST them to Beam.
        if sensordatacount >= 12:
            beampayload = {
                "series": sensordata[-12:],
                "maxAnomalyRatio": 0.25,
                "sensitivity": 99,
                "granularity": "minutely"      
            }

            # This POST will be via HTTP to Soracom Beam.
            beamurl = "http://beam.soracom.io:8888/"

            # We do not need to include our Azure Anomaly Detector API key in this header.
            beamheaders = {
                'Content-Type': "application/json"
            }

            response = requests.request("POST", beamurl, data=json.dumps(beampayload), headers=beamheaders)

            # Beam will pass back the response from the Anomaly Detector API, and we'll save it as JSON.
            azureresponse = json.loads(response.text)

            # This will print out isAnomaly: True or False depending on the boolean value returned.
            print("isAnomaly: ", azureresponse["isAnomaly"])
            
            # If the value is True, and anomaly is detected and the LED will turn on.
            if azureresponse["isAnomaly"] == True:
                print("Anomaly detected. Turning on LED.")
                led.turn_on()
            # Otherwise, its False, and we'll keep it off. This will turn it off it was true previously as well.
            else:
                print("No anomaly detected. LED off.")
                led.turn_off()

    except Exception as e:
        print(e)

    print("***")

    # sleep until next loop
    time_to_wait = loop_start_time + interval - time.time()
    if time_to_wait > 0:
        time.sleep(time_to_wait)
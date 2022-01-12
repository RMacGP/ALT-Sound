import serial
import csv
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : "https://project-thing-8ed9d-default-rtdb.europe-west1.firebasedatabase.app"
})

DATA_SESSION_COLLECTION_NAME = input("Enter title for data collection session:\t") # data will be pushed to new child on the database with this name

ref = db.reference()
# print(ref.get())

ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/ttyACM0'
ser.open()

count = 1
while True:
    # print(count)
    count += 1
    data = str(ser.readline())

    try:  # try parsing data, otherwise string is invalid, and continue onto next second
        
        seconds, sound = [-1,-1]

        parsed_data = re.sub(r'[^0-9,]', '', data).split(",") # remove all non-(number and ',') chars and split into two numbers using the ','
        seconds, sound = [int(x) for x in parsed_data]

        # in the case of error (with int() or .split().. etc), the data is invalid and the script moves onto the except statement

        # finished parsing string, final check if seconds and sound have been given values
        if (seconds == -1 or sound == -1):
            print("invalid data / parsing")
            raise Exception

        print(seconds, sound)

        # with open("sound_data.csv", "a+") as f: # write data to csv file
        #     csv_writer = csv.writer(f)
        #     csv_writer.writerow([seconds, sound])

        record = {"time":seconds, "sound":sound} # push data to firebase
        ref.child(DATA_SESSION_COLLECTION_NAME).push(record)

    except:
        pass

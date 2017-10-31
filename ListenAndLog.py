import sys
import time
import csv
import os
import serial as ser
import numpy as np
import matplotlib as plt

def UpdateRecentData (value):
	for i in xrange(8):
		recent_data[i,:] =  recent_data[i+1,:]
	recent_data[9,:] = value
	return;

# Constants
data_log_file_path = "outputs/data_log.csv"
usb_port = "/dev/cu.usbserial-DN01IWF9"

# TODO: Answer question: do we need this? does this 
#	actually speed things up?
# Create recent data array to store past 10 values
# This will be used to help filter out bad data as well
# 	as trigger alerts
recent_data = np.zeros((10,2))

# Open the data_log.csv file for appending and reading
data_log_file = open(data_log_file_path, "a+")

# If the file is empty, write the headers
if os.stat(data_log_file_path).st_size == 0:
        data_log_file.write("Time,Read\n")

# seek to the end of the file
data_log_file.seek(0,2)
file_offset = data_log_file.tell()

# fill recent data by reading backwards
# note: each read interates file offset forward
i = 9
j = 0
while file_offset < 9 and i >= 0:
	temp = data_log_file.read(1)
	# if the byte is a delimiter, iterate back past it
	if temp == ',':
		file_offset = file_offset - 2
		recent_data[i,j] = data_buffer
		data_buffer = ' '
		j = 1;
	# if the byte is a newline stop reading
	elif temp == '\n':
		file_offset = file_offset - 2
		recent_data[i,j] = data_buffer
		data_buffer = ' '
		j = 0;
		i = i - 1;
	else: 
		data_buffer = temp + data_buffer
		file_offset = file_offset - 2

# Open serial port
Xbee = ser.Serial(usb_port, baudrate=9600, timeout = 1)

error_counter = 0
error_time = 0
while True:

	while  Xbee.in_waiting:
		temp = Xbee.readline()

		try:
   			val = float(temp)
   			print(val)
   			UpdateRecentData(val)
   			write_string = str(time.clock()) + "," + str(val) + "\n"
   			data_log_file.write(write_string)
		except ValueError:
			error_counter = error_counter + 1
			error_time = time.clock()

	# decrement error counter every 30 seconds error free
	if (time.clock() -  error_time) > 30 and error_counter > 0:
		error_counter = error_counter - 1
		error_time = time.clock()

	# spit out error if counter reaches 10, reset counter to 0
	# sleep inserted to give user time to act if necessary
	if error_counter > 10:
		print ("Error overflow!")
		error_counter = 0
		time.sleep(5)

data_log_file.close()

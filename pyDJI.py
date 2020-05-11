#!/usr/bin/env python3
import sys
import serial

import duml
import serial.tools.list_ports

active_port = None

def connect(port):
	global active_port
	baud = 115200
	timeout = 3
	active_port = serial.Serial(port, baud, timeout=timeout)

	return active_port.is_open


def disconnect():
	if active_port.is_open:
		active_port.close()

def write(packet):
	print('sending ' + bytes(packet).hex())
	active_port.write(bytes(packet))

def main():
	if len(sys.argv) == 2:
		if connect(sys.argv[1]):
			write(duml.Reboot(0x21,0x0b))
		else:
			print('Failed to connect to ' + sys.argv[1])

	else:
		print('Usage: ./djiserial.py [PORT]')

if __name__ == '__main__':
	main()
#!/usr/bin/env python3
from random import randrange
from dumlcrc import *


seqno = randrange(0,32767)


def getSeqNo():
	global seqno
	if seqno >= 32767:
		seqno = 0
	else:
		seqno += 1
	return seqno


def getVersion(src, dst):
	#return build(source=0x2a, destination=0x28, cmdType=0x40, cmdSet=0x00, cmdID=0x01, payload=None)
	return build(source=src, destination=dst, cmdType=0x40, cmdSet=0x00, cmdID=0x01, payload=None)


def Reboot(src, dst):
	#return build(source=0x2a, destination=0x0b, cmdType=0x40, cmdSet=0x00, cmdID=0x0b, payload=None)
	return build(source=src, destination=dst, cmdType=0x40, cmdSet=0x00, cmdID=0x0b, payload=None)


def build(source, destination, cmdType, cmdSet, cmdID, payload):
	packet = [chr(0x00)] * 11
	pktlen = 0

	if payload is None:
		pktlen = 11
	else:
		pktlen = 11 + len(payload)

	#Header structure
	packet[0] = 0x55 #magic
	packet[1] = (pktlen + 2) & 0xFF #length
	packet[2] = (((pktlen + 2) >> 8 & 0x03) | 0x04) #version 
	packet[3] = calc8([packet[0],packet[1],packet[2]]) #header crc8

	#Transist 0801 --> (0x08 | (0x01 << 5)) == 0x28
	packet[4] = source
	packet[5] = destination
	seqno = getSeqNo()
	packet[6] = seqno & 0xFF #Sequence number
	packet[7] = (seqno >> 8) & 0xff #Sequence number

	#Command Structure
	packet[8] = cmdType
	packet[9] = cmdSet
	packet[10] = cmdID

	if payload is not None:
		packet = packet + packet

	pktcrc = calc16(packet)
	crc = [chr(0x00)] * 2
	crc[0] = pktcrc & 0xFF
	crc[1] = (pktcrc >> 8) & 0xFF
	packet += crc
	return packet
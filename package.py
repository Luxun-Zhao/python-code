#################################################
#package the data and send through the serial
#################################################


import struct #pack unpack
import sys
import binascii

import serial
ser = serial.Serial()
ser.baudrate = 115200
ser.port = sys.argv[1]
ser.open()

ID=int(sys.argv[2]);
number_tof=1;

##############################
# get the 
##############################

data=[-1445.821988342563800,0.390660170876389,-0.264142528229135,0.000021774903234,-0.000001716020822,0.000071871845679];
out=[0xff,0x55,6 * 8 + 3,0x03,ID];
sum_check=54+ID;
datapack=struct.pack('dddddd',data[0],data[1],data[2],data[3],data[4],data[5]);
print('%s'%datapack);
for i in datapack:
	sum_check = sum_check + i;
	out.append(i);
out.append(sum_check%256);

ser.write(bytes(out));
for i in range(1,9999):
	print();
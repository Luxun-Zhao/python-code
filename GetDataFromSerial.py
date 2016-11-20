import sys

import serial
import struct
import xlwt
import time
import numpy as np
import matplotlib.pyplot as plt
plt.figure(1)
ser = serial.Serial()
ser.baudrate = 115200
ser.port = sys.argv[1]
ser.open()
fig_num = 1
last_data = [0,0,0,0,0,0,0,0,0,0,0]
book = xlwt.Workbook(encoding = 'utf-8', style_compression = 0)
sheet = book.add_sheet('dede', cell_overwrite_ok = True)
i = 0
time = time.strftime('%y-%m-%d-%H-%M-%S',time.localtime(time.time()))
f = open('%s.txt' % time,'w')
a = '%s.txt'
while 1:
	s = ser.read()
	if ord(s) == 0xaa:
			s = ser.read()
			if ord(s) == 0xaa:
				s = ser.read()
				if ord(s) == 0xf1:
					s = ser.read()
					buf = ser.read(ord(s))
					# result = struct.unpack("!4h7f",buf)
					result = struct.unpack("!11f",buf)
					if fig_num == 201:
						fig_num = 1
						plt.cla()
						plt.pause(0.0001)
						plt.plot(200,0)
					# plt.plot([fig_num - 1,fig_num],[last_data[0],result[0]],'b',linewidth = 2)
					# plt.plot([fig_num - 1,fig_num],[last_data[1],result[1]],'k',linewidth = 2)
					# plt.plot([fig_num - 1,fig_num],[last_data[2],result[2]],'g',linewidth = 2)
					plt.plot([fig_num - 1,fig_num],[last_data[8],result[8]],'r',linewidth = 2)
					plt.plot([fig_num - 1,fig_num],[last_data[9],result[9]],'c',linewidth = 2)
					# plt.plot([fig_num - 1,fig_num],[last_data[3],result[3]],'m',linewidth = 2)
					# plt.plot([fig_num - 1,fig_num],[last_data[7],result[7]],'y',linewidth = 2)
					print(i,result)
					last_data = result
					plt.pause(0.0001)
					# for data in result:
						# sheet.write(i, num_result, result[num_result])
					f.write('%f	%f	%f	%f	%f	%f	%f	%f	%f	%f	%f\n'%result)
					i += 1
					fig_num += 1
						# book.save('%s.xls' % time)
ser.close()
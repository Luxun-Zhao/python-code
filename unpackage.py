###############################################
#输出数据格式：
#    每个TOF一个txt文件
#    文件内格式：
#    相位   信噪比   实际距离   测量距离
###############################################

###############################
#创建结果存放目录
###############################
import os
import shutil
if os.path.exists('result') == False:
	os.mkdir('result');
	# shutil.rmtree('result');


import sys
# import struct #pack unpack
read_file = sys.argv[1]
data = open('%s.txt' % read_file, 'r', encoding = 'utf-8');
print('%s' % read_file);

realdistance = 0;
tofdistance = [0,0,0,0,0,0];
while 1:
	a = data.readline();#read the text data
	if len(a) == 0:
		break;
	while 1:
		#########################
		#get one frame data
		#########################
		index = a.index('FF 55 ');
		if  index >= 0:
			lenth=int(a[index + 6:index + 8],16) + 3;#start from zero
			if len(a)<(lenth * 3):
				break;
			frame=a[index:index + lenth * 3];
			a=a[index + lenth * 3:];
			print('%s'%frame);
			###########################
			#unpack the frame
			###########################
			order = int(frame[9:11],16);
			ID = int(frame[12:14],16);
			get_checksum = int(frame[-3:],16);
			get_data = [];
			if order == 2:
				data_sum = 0;
				for i in range(1,lenth - 5):
					get_data.append(int(frame[3 * i + 12:3 * i + 14],16));
					data_sum = data_sum + get_data[i - 1];
					# print('data:%d'%get_data[-1]);
			###########################
			#check the checksum
			###########################
			real_checksum = (lenth - 3 + order + ID + data_sum) % 256;
			if real_checksum != get_checksum:
				print('sum:%d,%d'%(real_checksum,get_checksum))
				continue;
			###########################
			#put the data on his drive
			###########################
			numberOfTof = int(frame[16],16) - 1;
			print('TOF:%d'%numberOfTof);
			if int(frame[15],16) == 4:#if the data is sonar's data
				realdistance = (get_data[1] + get_data[2] * 256) / 8.343;
				print('sonar:%d'%realdistance);
			if int(frame[15],16) == 1:#if the data is tof's compute distance
				tofdistance[numberOfTof] = get_data[1] * 256 + get_data[2];
				print('tof:%d'%realdistance);
			if int(frame[15],16) == 3:#if the data is celibration data
				out_data = [get_data[6] * 256 + get_data[7],get_data[2] + get_data[3] * 256,realdistance,tofdistance[numberOfTof]];
				print('calibration:%d,%d,%d,%d'%tuple(out_data));
				file_name = '%d_' % ID + '%d' % (numberOfTof + 1);
				write_file = open('result/%s_out.txt' % file_name, 'a', encoding = 'utf-8')
				write_file.writelines('%d	%d	%d	%d\r\n'%tuple(out_data));
				# write_flie.close();
		else:
			continue;

import xlrd
import xlwt

file_read_name = '0.xls'
bk = xlrd.open_workbook(file_read_name)
shxrange = range(bk.nsheets)
try:
    sh = bk.sheet_by_name("考勤记录")
except:
    print("no sheet in %s named Sheet1" % fname)
#获取行数
nrows = sh.nrows
#获取列数
ncols = sh.ncols
print("nrows %d, ncols %d" % (nrows,ncols))
#获取第一行第一列数据 
cell_value = sh.cell_value(1,1)
#print cell_value

row_list = []
#获取各行数据
for i in range(1,nrows):
    row_data = sh.row_values(i)
    row_list.append(row_data)
print(row_list[1][2])

#row_list[a][b]	a从3开始，奇数为个人信息，+1为对应考勤数据
#				b     个人信息：工号【2】 姓名【10】 部门【20】

black=[]
if (nrows % 2) == 0:
	population = int((nrows - 4) / 2)#int(row_list[-2][2])
	print("考勤人数：%d" % population)
else:
	population = int((nrows - 4) / 2 + 1)#int(row_list[-1][2])
	print("考勤人数：%d" % population)
	for i in range(0,ncols):
		black.append('')
	row_list.append(black)

# print(row_list)

salary = []

for num in range(1,(population+1)):
	name = row_list[1 + num*2][10]
	check = []
	for day in range(0, ncols):
		if len(row_list[2 + num*2][day]) != 0:
			time_num = 	int(len(row_list[2 + num*2][day]) / 5)
			time_data = []
			for i in range(0,time_num):
				time_data.append((row_list[2 + num*2][day])[0 + 5 * i : 5 + 5 * i])
			work = (row_list[2 + num*2][day])[0 : 5]
			work_state = 0
			rest = (row_list[2 + num*2][day])[-5 :]
			rest_state = 0
			h=int(rest[:2]) - int(work[:2]) - 2
			m=int(rest[-2:]) - int(work[-2:]) + 30
			if m < 0 :
				m = m + 60
				h = h - 1
			elif m > 59 :
				m = m - 60
				h = h + 1
			if work == rest :
				h = 0
				m = 0
				if int(work[:2]) < 12 :
					rest = '漏卡'
					rest_state = 1
				else :
					work = '漏卡'
					work_state = 1
			work_time = '%d:%d'%(h,m)
			if h < 8:
				work_time_state = 2
			else:
				work_time_state = 0
			# print(work,rest,work_time)
		else :
			work = None
			work_state = 3
			rest = None
			rest_state = 3
			work_time = None
			work_time_state = 3

		check.append([work, rest, work_time, work_state, rest_state, work_time_state])

	salary.append([name, check])

mark = []
# print(salary)
book = xlwt.Workbook(encoding = 'utf-8', style_compression = 0)
sheet = book.add_sheet('dede', cell_overwrite_ok = True)

for i in [1, 3, 45, 48]:
	st = xlwt.easyxf('pattern: pattern solid;')
	st.pattern.pattern_fore_colour = i
	mark.append(st)

##############################################################################
for people in salary:
	sheet.write(0, salary.index(people) * 3 + 1, people[0])
	sheet.write(1, salary.index(people) * 3 + 1, '上班')
	sheet.write(1, salary.index(people) * 3 + 2, '下班')
	sheet.write(1, salary.index(people) * 3 + 3, '工作时间')

for day in range(1, (ncols + 1)):
	sheet.write(day + 1, 0, day)
	for people in salary:
		sheet.write(day + 1, salary.index(people) * 3 + 1, people[1][day-1][0], mark[people[1][day-1][3]])
		# sheet.write(day + 1, salary.index(people) * 3 + 1, people[1][day-1][0], mark[1])
		sheet.write(day + 1, salary.index(people) * 3 + 2, people[1][day-1][1], mark[people[1][day-1][4]])
		sheet.write(day + 1, salary.index(people) * 3 + 3, people[1][day-1][2], mark[people[1][day-1][5]])

###############################################################################
book.save('%s月考勤表.xls' % row_list[1][2][5:7])
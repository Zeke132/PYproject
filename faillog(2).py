import os,sys
import re,datetime
import time

##########################################################
#OK
def show_usage():
	print("--------------------[ usage ]------------------------")
	print("python faillog.py -a filename")
	print("python faillog.py -u username filename")
	print("python faillog.py -t date time filename")
	print("python faillog.py -v filename")
	print("------------------------------------------------------")

#OK
class FailLog(object):
	def __init__(self,fname):
		self._name=fname
		self._lines=[]
		self.parse()
	def parse(self):
		if not os.path.exists(self._name):
			print("Err: [%s] not exist" % self._name)
			sys.exit(-1)
		if not os.path.isfile(self._name):
			print("Err: [%s] is not a file" % self._name)
			sys.exit(-1)
		if not os.access(self._name,os.R_OK):
			print("Err: [%s] is not readable" % self._name)
			sys.exit(-1)
		fp=open(self._name,"r")
		lines=fp.readlines()
		fp.close()
		for line in lines:
			ret=re.search("([a-zA-Z0-9_-]+)\s+(\d{2}/\d{2}/\d{4})\s+(\d{2}:\s*\d{2}:\s*\d{2})",line.strip())
			if ret:
				obj={}
				obj["raw"]=line.strip()
				obj["name"]=ret.group(1)
				obj["date"]=ret.group(2)
				obj["time"]=ret.group(3)
				self._lines.append(obj)
	def print_all_name(self):#OK
		if len(self._lines)==0:
			print("No usernames found")
			return
		print("Usernames:")
		for obj in self._lines:
			print(obj["name"])
	def print_by_name(self,name):
		events=[]
		for obj in self._lines:
			if obj["name"]==name:
				events.append(obj["raw"])
		if len(events)==0:
			print("No events found for the given %s" % name)
			return
		print("Events for user: %s" % name)
		for line in events:
			print(line)
	def calc_time(self,s_date,s_time):
		data="%s %s" % (s_date.strip(),s_time.strip())
		tm=time.strptime(data,'%d/%m/%Y %H:%M:%S')
		return tm
	def print_by_time(self,s_date,s_time):
		events=[]
		filter_tm=self.calc_time(s_date,s_time)
		for obj in self._lines:
			tmp=self.calc_time(obj["date"],obj["time"])
			if tmp>=filter_tm:
				events.append(obj["raw"])
		if len(events)==0:
			print("No events found for the given %s/%s" % (s_date,s_time))
			return
		for line in events:
			print(line)
	def print_version(self):
		#eg.Huang XiaoMing
		name="Xiao Ming"
		surname="Huang"
		student_id="2048"
		completion_date="2021/5/20"
		print("\n============Assignment Information============")
		print("%18s: %s" % ("Surname",surname))
		print("%18s: %s" % ("Name",name))
		print("%18s: %s" % ("ID",student_id))
		print("%18s: %s" % ("Completion Date",completion_date))
		print("=============================================")
##########################################################
#[1] no options found
if len(sys.argv)<2:
	show_usage()
	sys.exit(-1)

#[2] check first option
first_option=sys.argv[1]
#python faillog.py -a filename
if first_option=="-a":
	if len(sys.argv)<3:
		print("Err: missing [filename] argument")
		sys.exit(-1)
	fp=FailLog(sys.argv[2])
	fp.print_all_name()
	sys.exit(-1)

#python faillog.py -u username filename
if first_option=="-u":
	if len(sys.argv)<3:
		print("Err: missing [username] argument")
		sys.exit(-1)
	if len(sys.argv)<4:
		print("Err: missing [filename] argument")
		sys.exit(-1)
	fp=FailLog(sys.argv[3])
	fp.print_by_name(sys.argv[2])
	sys.exit(-1)

#python faillog.py -t date time filename
if first_option=="-t":
	if len(sys.argv)<3:
		print("Err: missing [date] argument ")
		sys.exit(-1)
	if len(sys.argv)<4:
		print("Err: missing [time] argument ")
		sys.exit(-1)
	if len(sys.argv)<5:
		print("Err: missing [filename] argument ")
		sys.exit(-1)
	fp=FailLog(sys.argv[4])
	fp.print_by_time(sys.argv[2],sys.argv[3])
	sys.exit(-1)

#python faillog.py -v filename
if first_option=="-v":
	if len(sys.argv)<3:
		print("Err: missing [filename] argument")
		sys.exit(-1)
	fp=FailLog(sys.argv[2])
	fp.print_version()

	sys.exit(-1)

print("wrong option")
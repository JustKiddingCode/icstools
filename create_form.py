#!/usr/bin/env python3
# vim: tabstop=4 noexpandtab
import math
import sys, argparse
from datetime import date
from calendar import monthrange

from ics import Calendar

days = [ 0 for k in range(33) ]
days[0] = -1
months = {
	'JAN' : 1,
	'FEB' : 2,
	'MAR' : 3,
	'APR' : 4,
	'MAY' : 5,
	'JUN' : 6,
	'JUL' : 7,
	'AUG' : 8,
	'SEP' : 9,
	'OCT' : 10,
	'NOV' : 11,
	'DEC' : 12,
		}

def get_first_sunday(year,month):
	for i in range(1,8):
		if date(year,month,i).isoweekday() == 7:
			return i

def disable_sunday_saturday(year,month):
	# set days to -1 where is it a saturday or sunday
	first_sunday = get_first_sunday(year,month)

	while first_sunday < 32:
		if first_sunday > 1:
			days[first_sunday - 1] = -1
			days[first_sunday] = -1
		first_sunday += 7

def disable_holidays(year,month):
	# disable public holidays ( set to - 2)
	pass


def duration_to_hours(total_seconds):
	# input: 04:30:20
	# output: 4,5
	return total_seconds / 3600.0
	


def read_ics(filename,year,month,title_starts,from_day,to_day,print_only):
	f = open(filename, "r")

	c = Calendar(f.read())
	start = "%04d-%02d-%02d" % (year,month,from_day)
	if (to_day == 32):
		end = "%04d-%02d-01" % (year,month+1)
	else:
		end = "%04d-%02d-%02d" % (year,month,to_day)

	#print(c)
	eventlist = c.events[start:end]
	#print(eventlist)

	for i in eventlist:
		entry_day = i.begin.day
#		print(i.description)
		if not i.name.startswith(title_starts):
			continue
		while days[entry_day] < 0:
			entry_day += 1
		# entry_days could be 32 (thats ok)
		if print_only:
			print("%04d-%02d-%02d\t%.2f\t%s" %(year,
				month,
				entry_day,
				duration_to_hours(i.duration.total_seconds()),
				i.name)
			)
		else:
			days[entry_day] += duration_to_hours(i.duration.total_seconds())
			
def normalize_days(MAX_HOURS_PER_DAY=6):
	to_balance = days[32]
	days[32] = 0

	for i in range(len(days)):
		if days[i] < 0:
			continue
		
		if days[i] > MAX_HOURS_PER_DAY:
			to_balance += days[i] - MAX_HOURS_PER_DAY
			days[i] = MAX_HOURS_PER_DAY
		else:
			if to_balance > 0:
				if to_balance > MAX_HOURS_PER_DAY - days[i]:
					to_balance -= MAX_HOURS_PER_DAY - days[i]
					days[i] = MAX_HOURS_PER_DAY
				else: 
					days[i] += to_balance
					to_balance = 0
		places = days[i] - math.floor(days[i])
		if places > 0.75:
			days[i] += 1-places
		elif places > 0.5:
			days[i] += 0.75-places
		elif places > 0.25:
			days[i] += 0.25-places
		elif places > 0:
			days[i] += 0.25-places



def stretch_days(factor=1.5):
	for i in range(len(days)):
		if days[i] < 0:
			continue
		days[i] *= factor

def days_sum():
	x = 0
	for y in days:
		if y > 0:
			x += y
	return x

def print_days(month,year):
	for i in range(len(days)):
		if days[i] > 0:
			print("%02d.%02d.%04d\t%s" % (i,month,year,days[i]))
		

def main(argv):
	# Parser
	parser = argparse.ArgumentParser(description='Create time documentation')
	parser.add_argument('month')
	parser.add_argument('-f',dest='icsfile',required=True,action='append')
	parser.add_argument('--max',type=int,default=6,required=False)
	parser.add_argument('--factor',type=float,default=1.5,required=False)
	parser.add_argument('--title',type=str,default="",required=False)
	parser.add_argument('--weekend',dest='weekend',action='store_true')
	parser.add_argument('--no-weekend',dest='weekend',action='store_false')
	parser.add_argument('--from',type=int,dest='from_day',default=0,required=False)
	parser.add_argument('--to',type=int,default=31,required=False)
	parser.add_argument('--printonly',action='store_true')
	parser.add_argument('--no-header',dest='header',action='store_false')
	args = parser.parse_args()
	if args.header:
		print(args.month)

	# Set month 
	today = date.today()
	year, month, day = date.today().timetuple()[:3]
	month = months[args.month]
	if not args.weekend:
		disable_sunday_saturday(year, month)

	# Read ics
	for filename in args.icsfile:
		read_ics(filename,year,month,args.title,args.from_day,args.to + 1,args.printonly)

	if not args.printonly:
		stretch_days(args.factor)
		normalize_days(args.max)
	
		print(days_sum())

		print_days(month, year)

if __name__ == "__main__":
	main(sys.argv[1:])

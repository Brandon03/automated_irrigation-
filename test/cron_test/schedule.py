from crontab import CronTab
import pdb

#pdb.set_trace()

s = "python3 /Users/tongkuisheng/Projects/Programming/irricon/config/writeDate.py"
_s = "python3 /Users/tongkuisheng/Projects/Programming/irricon/program/example1.py"

"""
system_cron = CronTab(tabfile="/usr/bin/crontab", user=False)
job = system_cron[0]
job.user != None
job = system_cron.new(command=_s, user='root')

"""
cron = CronTab(user="pi")
job = cron.new(command=s)
job.minute.every(1)

print(job)

cron.write()

'''
my_cron = CronTab(user="pi")
for job in my_cron:
	if job.comment == "dateinfo":
		job.minute.every(1)
		my_cron.write()
		print("job done")
'''

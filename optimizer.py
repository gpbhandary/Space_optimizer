##############################################################################
# story:        https://jira.oraclecorp.com/jira/browse/OCSC-10948
# Script:       space_optimizer.py
# Language:     Python 2.7
#
# Author:       Guruprasad Bhandary B
# Date:         1st April 2021
# Version:      0.1
#
##############################################################################
# Amendment History:
#########################################################################################
#JOBINFO NAME
#Automated script for zipping the old audit log files frequency basis
#########################################################################################
########################### Common Setup #################################
import fnmatch
import os
import time
import gzip
import configuration

seconds = time.time()
local_time = time.ctime(seconds)
prev_hour_sec = seconds - 3600
prev_hour = (time.ctime(prev_hour_sec)[8:13])
prev_hour_only = (time.ctime(prev_hour_sec)[11:13])
prev_day = (time.ctime(seconds - 86400)[8:10])
print prev_day
print prev_hour
print prev_hour_only
print("Local time:", local_time)
# Path1 = '/var/log/mysql_processlist' # zip one hour previous files from current time
# Path2 = '/var/log/sa' # zip the files at the end of the day(previous day file) , file zip at 00 hours for the <23:** hour time stamp file
# Path3 = '/var/log/audit.d' #zip particular file type with patter
# pattern = '*[!.gz]'
# Pattern1 = '*.log.*'

for root, dirs, files in os.walk(configuration.Path1):
    for filename in fnmatch.filter(files, configuration.pattern):
        if (time.ctime(os.path.getmtime(os.path.join(root, filename)))[8:13]) == prev_hour:
            print(time.ctime(os.path.getmtime(os.path.join(root, filename)))[8:13], filename)
            print (os.path.join(root, filename))
            f_in = open(os.path.join(root, filename))
            f_out = gzip.open((os.path.join(root, filename)) + '.gz', 'wb')
            f_out.writelines(f_in)
            f_out.close()
            f_in.close()
            os.remove(os.path.join(root, filename))

for root, dirs, files in os.walk(configuration.Path3):
    for filename in fnmatch.filter(files, configuration.Pattern1 + configuration.pattern):
        print (time.ctime(os.path.getmtime(os.path.join(root, filename)))[8:13], filename)
        print (os.path.join(root, filename))
        f_in = open(os.path.join(root, filename))
        f_out = gzip.open((os.path.join(root, filename)) + '.gz', 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove(os.path.join(root, filename))

if prev_hour_only == '23':
    for root, dirs, files in os.walk(configuration.Path2):
        for filename in fnmatch.filter(files, configuration.pattern):
            if (time.ctime(os.path.getmtime(os.path.join(root, filename)))[8:10]) == prev_day:
                print(time.ctime(os.path.getmtime(os.path.join(root, filename)))[10:13], filename)
                print (os.path.join(root, filename))
                f_in = open(os.path.join(root, filename))
                f_out = gzip.open((os.path.join(root, filename)) + '.gz', 'wb')
                f_out.writelines(f_in)
                f_out.close()
                f_in.close()
                os.remove(os.path.join(root, filename))

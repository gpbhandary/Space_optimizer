##############################################################################
# story:        https://jira.oraclecorp.com/jira/browse/OCSC-10948
# Script:       space_optimizer.py
# Language:     Python 2.7
#
# Author:       Guruprasad Bhandary B
# Date:         1st April 2021
# Version:      0.1
##############################################################################
# Amendment History:
#########################################################################################
#JOBINFO NAME
#Automated script for zipping the old audit log files frequency basis
#########################################################################################
########################### Common Setup #################################
# /usr/local/rnt/lib/python2.7/site-packages/yaml
#import sys; sys.path.append('/usr/local/rnt/lib/python2.7/site-packages/yaml/')
import fnmatch
import os
import time
import gzip
import yaml
import shutil
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
file_handler = logging.FileHandler('zipping.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.Loader)
Length_of_config = len(config)
seconds = time.time()
local_time = time.ctime(seconds)
prev_hour_sec = seconds - 3600
prev_day_sec = seconds - 86400
prev_hour = (time.ctime(prev_hour_sec)[8:13])
prev_hour_only = (time.ctime(prev_hour_sec)[11:13])
prev_day = (time.ctime(seconds - 86400)[8:10])
pattern = '*[!.gz]'
# Pattern1 = '*.log.*'
count = 0
while count < Length_of_config:
    directory = (config[count]['Directory%s' % (count + 1)]['Path'])
    zipping_frequency = (config[count]['Directory%s' % (count + 1)]['zipping_frequency'])
    logger.info("Directory: " + directory + " , " + "zipping frequency: " + zipping_frequency)
    count = count + 1
    isdir = os.path.isdir(directory)
    if not isdir:
        logger.error("PLEASE CHECK THE DIRECTORY PATH: " + directory)
        continue  # skip and continue the next while loop
    if zipping_frequency == "Hourly":
        for root, dirs, files in os.walk(directory):
            for filename in fnmatch.filter(files, pattern):
                file_time_sec = (os.path.getmtime(os.path.join(root, filename)))
                if file_time_sec <= prev_hour_sec:
                    print(time.ctime(os.path.getmtime(os.path.join(root, filename)))[8:13], filename)
                    file_name = os.path.join(root, filename)
                    logger.info("File zipped: " + file_name)
                    f_in = open(os.path.join(root, filename))
                    f_out = gzip.open((os.path.join(root, filename)) + '.gz', 'wb')
                    f_out.writelines(f_in)
                    f_out.close()
                    f_in.close()
                    shutil.copystat(file_name, file_name + '.gz')
                    os.remove(os.path.join(root, filename))
    elif zipping_frequency == "Daily":
        for root, dirs, files in os.walk(directory):
            for filename in fnmatch.filter(files, pattern):
                file_time_sec = (os.path.getmtime(os.path.join(root, filename)))
                if file_time_sec <= prev_day_sec or (time.ctime(os.path.getmtime(os.path.join(root, filename)))[8:10]) == prev_day:
                    print(time.ctime(os.path.getmtime(os.path.join(root, filename)))[8:13], filename)
                    file_name = os.path.join(root, filename)
                    logger.info("File zipped: " + file_name)
                    f_in = open(os.path.join(root, filename))
                    f_out = gzip.open((os.path.join(root, filename)) + '.gz', 'wb')
                    f_out.writelines(f_in)
                    f_out.close()
                    f_in.close()
                    shutil.copystat(file_name, file_name + '.gz')
                    os.remove(os.path.join(root, filename))
logger.info("Exiting ...")
bashCommand = "tail -n 2000 zipping.log > zipping1.log"
bashCommand1 = "mv -f zipping1.log zipping.log"
os.system(bashCommand)
os.system(bashCommand1)









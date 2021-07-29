Path1 = '/var/log/mysql_processlist'  # zip one hour previous files from current time
Path2 = '/var/log/sa'  # zip the files at the end of the day(previous day file) , file zip at 00 hours for the <23:** hour time stamp file
Path3 = '/var/log/audit.d'  # zip particular file type with patter
pattern = '*[!.gz]'
Pattern1 = '*.log.*'

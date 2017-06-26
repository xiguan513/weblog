#!/bin/bash
#Author   :  songbing
#Function :  tomcat_log_time_intercept
#Date     :  2015-9-14


#variable
log_dir=/opt/tomcat_log/
DATE=$(date +%Y%m%d%H%M%S)

#Number of rows to take a keyword
#if [ $(id -u root) -ne 0 ];then
#	echo  -e "\033[31myour must administrator user!\033[0m"
#	exit 1
#else
#	echo -e "\033[31m
#		Query log ges:
#		bash /opt/sh/$0 "start_time" "End_time" "Project_name"
#		bash tomcat_log_time.sh \"2016-01-29 00:00\"  "/usr/local/tomcat_core_biz/logs/catalina-2016-01-29.log"
#		or
#		bash tomcat_log_time.sh \"2016-01-29 00:00\" \"2016-01-29 00:33\"  "/usr/local/tomcat_core_biz/logs/catalina-2016-01-29.log"
#	\033[0m"
#fi

if [ -d ${log_dir} ];then
    echo -e "\033[31mLog dircutre ${log_dir}\033[0m"
else
    mkdir ${log_dir}
fi

if [ $# == 2 ];then
        log_file=$2
        line_head=$(cat -n  ${log_file}  | grep "$1" | head -1 |awk '{print $1}')
        #log

		#name=$(echo ${2} | awk -F"/" '{print $4}')
        #sed -n ''${line_head}',$p' $log_file > ${log_dir}${name}${DATE}.log
        sed -n ''${line_head}',$p' $log_file
        if [ $? -ne 0 ];then
                exit 10
        fi
else
		if [ $# == 3 ];then
			#echo $1 $2 $3
			#log file path
			log_file=$3
			#line number
			line_head=$(cat -n  ${log_file}  | grep "$1" | head -1 |awk '{print $1}')
			line_tail=$(cat -n  ${log_file}  | grep "$2" | tail -1|awk '{print $1}')
			#log
			#name=$(echo ${3} | awk -F"/" '{print $4}')
			#sed -n ''$line_head','$line_tail'p' $log_file > ${log_dir}${name}${DATE}.log
			sed -n ''$line_head','$line_tail'p' $log_file 
            if [ $? -ne 0 ];then
                exit 10
            fi
		fi
fi

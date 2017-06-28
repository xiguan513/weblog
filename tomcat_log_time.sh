#!/bin/bash
#Author   :  songbing
#Function :  tomcat_log_time_intercept
#Date     :  2015-9-14


#variable
log_dir=/opt/tomcat_log/
DATE=$(date +%Y%m%d%H%M%S)


if [ -d ${log_dir} ];then
    echo -e "\033[31mLog dircutre ${log_dir}\033[0m"
else
    mkdir ${log_dir}
fi

if [ $# == 2 ];then
        log_file=$2
        line_head=$(cat -n  ${log_file}  | grep "$1" | head -1 |awk '{print $1}')
        sed -n ''${line_head}',$p' $log_file
        if [ $? -ne 0 ];then
                exit 10
        fi
else
		if [ $# == 3 ];then

			log_file=$3
			line_head=$(cat -n  ${log_file}  | grep "$1" | head -1 |awk '{print $1}')
			line_tail=$(cat -n  ${log_file}  | grep "$2" | tail -1|awk '{print $1}')
			sed -n ''$line_head','$line_tail'p' $log_file 
            if [ $? -ne 0 ];then
                exit 10
            fi
		fi
fi

#!/bin/bash
DIR="/home/ubuntu/kentzu/insert_list/insert_list1025"
ERROR_TXT="/home/ubuntu/kentzu/insert_list/insert_list1025/error.txt"
for entry in  "$DIR"/*
do
  FILE=$(basename "$entry")
  echo "insert file: " 
  echo $FILE
  echo "start insert...................."
  python insert_file_one.py $FILE
  echo "restart .............."
  sudo service nova-api-ec2 restart;sudo service nova-cert restart;sudo service nova-consoleauth restart;sudo service nova-objectstore restart;sudo service nova-api-os-compute restart;sudo service nova-conductor restart;sudo service nova-novncproxy restart; sudo service nova-scheduler restart

  echo "status .............."
  sudo service nova-api-ec2 status;sudo service nova-cert status;sudo service nova-consoleauth status;sudo service nova-objectstore status;sudo service nova-api-os-compute status;sudo service nova-conductor status;sudo service nova-novncproxy status; sudo service nova-scheduler status

  #echo "status .............."
  #STATUS="$(sudo service nova-api-ec2 status;sudo service nova-cert status;sudo service nova-consoleauth status;sudo service nova-objectstore status;sudo service nova-api-os-compute status;sudo service nova-conductor status;sudo service nova-novncproxy status; sudo service nova-scheduler status)"
 
   
  #echo $STATUS
  SERVICE="nova-api-ec2 nova-api-os-compute nova-cert nova-conductor nova-consoleauth nova-novncproxy nova-objectstore nova-scheduler"

  for s in $SERVICE; do

    is_running=`ps aux | grep -v grep | grep $s | wc -l | awk '{print $1}'`
    echo $is_running
    echo $s
    sleep 2s
    if (( $is_running < 1)); then 
    
      echo "###################ERROR####################"
      echo "recover file:"
      echo $FILE
      echo "$FILE" >> $ERROR_TXT
      python recover_file_one.py $FILE
      break
    fi
  done
done

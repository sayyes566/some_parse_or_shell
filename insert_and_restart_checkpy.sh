#!/bin/bash
DIR="/home/ubuntu/kentzu/insert_list/insert_list1025"
ERROR_LIST="/home/ubuntu/kentzu/insert_list/error_list/"
ERROR_TXT="/home/ubuntu/kentzu/insert_list/error.txt"
ERROR_SOURCE_TXT="/home/ubuntu/kentzu/insert_list/error_source.txt"
for entry in  "$DIR"/*
do
  FILE=$(basename "$entry")
  echo "insert file: " 
  echo $FILE
  echo "start insert...................."
  python insert_file_one.py $FILE
  #echo "restart .............."
  #sudo service nova-api-ec2 restart;sudo service nova-cert restart;sudo service nova-consoleauth restart;sudo service nova-objectstore restart;sudo service nova-api-os-compute restart;sudo service nova-conductor restart;sudo service nova-novncproxy restart; sudo service nova-scheduler restart

  #echo "status .............."
  #sudo service nova-api-ec2 status;sudo service nova-cert status;sudo service nova-consoleauth status;sudo service nova-objectstore status;sudo service nova-api-os-compute status;sudo service nova-conductor status;sudo service nova-novncproxy status; sudo service nova-scheduler status

  #echo "status .............."
  #STATUS="$(sudo service nova-api-ec2 status;sudo service nova-cert status;sudo service nova-consoleauth status;sudo service nova-objectstore status;sudo service nova-api-os-compute status;sudo service nova-conductor status;sudo service nova-novncproxy status; sudo service nova-scheduler status)"
 
  LINE=$(head -n 1 $DIR/$FILE)

  API_PATH=${LINE:10}

  EXE_PYTHON=$(python $API_PATH  2>&1)

  sleep 1s

  ERROR_EXIST=0
  if [[ "$EXE_PYTHON" = *invalid* ]]; then
    ERROR_EXIST=1
  elif [[ "$EXE_PYTHON" = *expected* ]]; then
    ERROR_EXIST=2
  elif [[ "$EXE_PYTHON" = *Error* ]]; then
    ERROR_EXIST=3
  elif [[ "$EXE_PYTHON" = *line* ]]; then
    ERROR_EXIST=4
  fi

  echo "#end check python syntax"

    if (( $ERROR_EXIST > 0)); then 
    
      echo "###################ERROR####################"
      echo $EXE_PYTHON
      echo "==========================================="
      echo $ERROR_EXIST
      echo "recover file:"
      echo $FILE
      echo "$EXE_PYTHON" >> $API_PATH
      cp -v $API_PATH $ERROR_LIST$FILE.py
      echo "$API_PATH" >> $ERROR_SOURCE_TXT
      echo "$FILE" >> $ERROR_TXT
      python recover_file_one.py $FILE
      echo "origin file path"
      echo $API_PATH 
      echo "#########################################END"
      
    fi

done

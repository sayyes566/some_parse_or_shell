#!/bin//bash
DIR="/home/ubuntu/kentzu/insert_list/insert_list1025"
ERROR_LIST="/home/ubuntu/kentzu/insert_list/error_list2/"
ERROR_TXT="/home/ubuntu/kentzu/insert_list/error.txt"
ERROR_SOURCE_TXT="/home/ubuntu/kentzu/insert_list/error_source.txt"
for entry in  "$DIR"/*
do
  FILE=$(basename "$entry")
  #echo "insert file: " 
  #echo $FILE
  
  filename="$ERROR_TXT"

    while read -r line 
    do

      error_name="$line"

      #echo "Name  - $error_name \n"
      
      if [ `echo $FILE` = `echo $error_name` ];
        then

        echo "ok ------------- $FILE \n"
      

       echo "start insert...................."
  
       python insert_file_one.py $FILE

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

      #if (( $ERROR_EXIST > 0)); then

      echo "###################ERROR####################"
      echo $EXE_PYTHON
      echo "==========================================="
      echo $ERROR_EXIST
      echo "recover file:"
      echo $FILE
      echo "$EXE_PYTHON" >> $API_PATH
      echo "$API_PATH" >> $ERROR_SOURCE_TXT
      echo "$FILE" >> $ERROR_TXT
      cp -v $API_PATH $ERROR_LIST$FILE.py
      python recover_file_one.py $FILE
      echo "origin file path"
      echo $API_PATH
      echo "#########################################END"

     break 1  
    fi

     

    done < "$filename"

  #LINE=$(head -n 1 $DIR/$FILE)

  #API_PATH=${LINE:10}

  #EXE_PYTHON=$(python $API_PATH  2>&1)
done

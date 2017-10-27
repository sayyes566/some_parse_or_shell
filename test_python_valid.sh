
#!/bin/sh
DIR="/home/ubuntu/kentzu/insert_list/insert_list1025"

FILE="/home/ubuntu/kentzu/insert_list/insert_list1025/nova_wsgi"

value=$(head -n 1 $FILE)

echo "${value:10}"

#res=$(python /usr/lib/python2.7/dist-packages/nova/api/ec2/cloud.py 2>&1)
res=${value:10}
echo $res
#pyv=(python -V 2>&1)
cp -v $res $DIR/error_list/123
sleep 1s
echo "$pyv"

if [[ "$res" = *invalid* ]]; then 
  echo "find valid"

fi
  
echo "#end"

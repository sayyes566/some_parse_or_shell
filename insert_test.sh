#!/bin/bash
  echo "restart .............."
  sudo service nova-api-ec2 restart;sudo service nova-cert restart;sudo service nova-consoleauth restart;sudo service nova-objectstore restart;sudo service nova-api-os-compute restart;sudo service nova-conductor restart;sudo service nova-novncproxy restart; sudo service nova-scheduler restart

  echo "status .............."
  sudo service nova-api-ec2 status;sudo service nova-cert status;sudo service nova-consoleauth status;sudo service nova-objectstore status;sudo service nova-api-os-compute status;sudo service nova-conductor status;sudo service nova-novncproxy status; sudo service nova-scheduler status

  echo "status .............."
  STATUS="$(sudo service nova-api-ec2 status;sudo service nova-cert status;sudo service nova-consoleauth status;sudo service nova-objectstore status;sudo service nova-api-os-compute status;sudo service nova-conductor status;sudo service nova-novncproxy status; sudo service nova-scheduler status)"
 
  #sleep 5s 
  echo $STATUS

#echo $template
if pgrep -x "nova-api-os-compute"  > /dev/null
then
    echo "Running"
else
    echo "Stopped"
fi
SERVICE="nova-api-ec2 nova-api-os-compute nova-cert nova-conductor nova-consoleauth nova-novncproxy nova-objectstore nova-scheduler"

for s in $SERVICE; do

  is_running=`ps aux | grep -v grep | grep $s | wc -l | awk '{print $1}'`
  #echo "is running:"+$s
  echo $is_running
  sleep 2s
done

#echo "$(/etc/init.d/nova-api-os-compute status)"

#echo "$(service --status-all)"

#eval "service --status-all"

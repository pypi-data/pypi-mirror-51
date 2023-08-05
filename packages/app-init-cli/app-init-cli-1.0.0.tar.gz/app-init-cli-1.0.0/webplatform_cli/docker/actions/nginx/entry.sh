#!/bin/bash -x
# echo "$HOST_MACHINE     host-machine" >> /etc/hosts
# if [ ! -e "/home/cee-tools/logs/error.log" ]; then
#   touch /home/cee-tools/logs/error.log
# fi

# rm -rf /run/nginx.pid
# cat /home/container/config/test.conf
sh /home/container/actions/start.sh

tail -f /home/container/data/error.log
bash

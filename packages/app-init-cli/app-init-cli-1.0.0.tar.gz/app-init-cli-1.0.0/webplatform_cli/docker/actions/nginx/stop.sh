#!/bin/bash -x
if [ -e "/run/nginx.pid" ]; then
  PID=$(cat /run/nginx.pid)
  CHECK=$(ps -p $PID | tail -n +2 | awk '{ print $1 }')

  if [ "$CHECK" == "$PID" ]; then
    echo "Stopping '$CEE_TOOLS_SERVICE' on instance '$CEE_TOOLS_INSTANCE'"
    kill -s QUIT $PID

    while true; do
      if [ ! -e "/run/nginx.pid" ]; then
        break
      fi
    done
  else
    echo "Already killed '$CEE_TOOLS_SERVICE' on instance '$CEE_TOOLS_INSTANCE'"
    rm -f /run/nginx.pid
  fi
else
  echo "Already killed '$CEE_TOOLS_SERVICE' on instance '$CEE_TOOLS_INSTANCE'"
fi

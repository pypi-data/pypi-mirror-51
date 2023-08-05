#!/bin/bash -x
if [ -e '/home/cee-tools-src' ]; then
  cd /home/cee-tools-src/frontend/
  rm -rf dist/

  git fetch origin
  git merge origin/production

else
  git clone -b production git@gitlab.cee.redhat.com:mowens/cee-tools.git /home/cee-tools-src/
  sh /home/container/actions/setup.sh
fi

chown -R tmp:tmp /home/cee-tools-src

su - tmp -c "cd /home/cee-tools-src/frontend; npm install"
su - tmp -c "cd /home/cee-tools-src/frontend; npm run prod"

#!/bin/bash
# PYTHONPATH=/home/container/cli:$PYTHONPATH
# PYTHON=/home/container/cli:$PATH
export PYTHONPATH=$PYTHONPATH:/home/container/webplatform_cli
export PATH=$PATH:/home/container/webplatform_cli

. /home/container/actions/entry.sh
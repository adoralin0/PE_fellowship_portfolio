#!/bin/bash

PROJECTDIR="$HOME/PE_fellowship_portfolio"


tmux kill-server 2>/dev/null

cd "$PROJECTDIR" || exit

git fetch
git reset --hard origin/main

python3 -m venv venv
source venv/bin/activate

python3 -m pip install -r requirements.txt

tmux new -d -s flask "cd $PROJECTDIR && source venv/bin/activate && flask run --host=0.0.0.0 --port=5000"

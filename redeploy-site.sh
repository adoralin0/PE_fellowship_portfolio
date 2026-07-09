#!/bin/bash

PROJECTDIR="$HOME/PE_fellowship_portfolio"

cd "$PROJECTDIR" || exit

git fetch
git reset --hard origin/main

python3 -m venv venv
source venv/bin/activate

python3 -m pip install -r requirements.txt

sudo systemctl restart myportfolio
sudo systemctl status myportfolio --no-pager

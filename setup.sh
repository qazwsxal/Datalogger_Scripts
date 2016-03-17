#!/bin/bash
#check if pip3 (therefore python3) is installed
if hash pip3; then
  if hash virtualenv; then #check for virtualenv
    :  #do nothing
  else
    sudo pip3 install virtualenv #install if not there
  fi
  #setup virtualenv

  virtualenv .venv

  #activate .venv
  source .venv/bin/activate

  #install requirements
  echo Installing requirementls
  pip install -r requirements.txt
else
  if hash python3; then
    echo pip3 not found, is it installed?
    exit 1
  else
    echo python 3 not found, is it installed?
    exit 1
  fi
fi

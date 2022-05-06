#!/bin/bash

python3 ui.py &
sleep 5
python3 signal2.py $!
#!/bin/bash

python3 final/src/ui/ui.py &
sleep 5
python3 signal2.py $!
#!/bin/bash
pyro4-ns &
for ((i=1;i<=$1;i++))
do
    python replica.py &
done
python frontend.py &

function kill_script() {
    echo
    echo "Clean exit"
    killall -SIGKILL python
    killall -SIGKILL pyro4-ns
    exit
}

read -p "waiting"
kill_script

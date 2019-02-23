#!/bin/bash
pyro4-ns &
for ((i=1;i<=$1;i++))
do
    python3 replica.py $1 &
done
python3 frontend.py &

function kill_script() {
    echo
    echo "Clean exit"
    killall -SIGKILL python3
    killall -SIGKILL pyro4-ns
    exit
}

read -p "waiting"
kill_script

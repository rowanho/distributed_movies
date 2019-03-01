#!/bin/bash
pyro4-ns &
python3 frontend.py &
for ((i=1;i<=10;i++))
do
    python3 replica.py 10 &
done

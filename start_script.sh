#!/bin/bash
pyro4-ns &
python3 frontend.py &
for ((i=1;i<=3;i++))
do
    python3 replica.py 3 &
done

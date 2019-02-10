#!/bin/bash
pyro4-ns &
for ((i=1;i<=$1;i++))
do
    python replica.py &
done
python frontend.py &

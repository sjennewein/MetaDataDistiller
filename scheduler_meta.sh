#!/bin/bash

if [ ! -f ~/papers/RUNNING ] 
then
  for f in ~/papers/dois*.txt
  do
    touch ~/papers/RUNNING
    /usr/bin/python3 $f /home/xt3/papers/metadata
    tar -xzf /home/xt3/papers/metadata_$f.tar.gz /home/xt3/papers/metadata
    rm $f
    rm -rf /home/xt3/papers/metadata/*
    touch ~/papers/FINISHED
    rm ~/papers/RUNNING
  done
fi 

#!/bin/bash

if [ ! -f ~/papers/RUNNING ] 
then
  for f in ~/papers/dois*.txt
  do
    touch ~/papers/RUNNING
    /usr/bin/python3 $f /home/stephan/papers/metadata
    tar -xzf /home/stephan/papers/metadata.tar.gz /home/stephan/papers/metadata
    rm $f
    rm -rf /home/stephan/papers/metadata/*
    touch ~/papers/FINISHED
    rm ~/papers/RUNNING
  done
fi 

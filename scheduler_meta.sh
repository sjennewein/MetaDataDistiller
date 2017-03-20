#!/bin/bash

if [ ! -f ~/papers/RUNNING ] 
then
  for f in ~/papers/dois*.txt
  do
    echo $f
    #touch ~/papers/RUNNING
    /usr/bin/python3 /home/xt3/MetaDataDistiller/metadata_fromList.py $f /home/xt3/papers/metadata/
    #tar -xzf /home/xt3/papers/metadata_$f.tar.gz /home/xt3/papers/metadata
    #rm $f
    #rm -rf /home/xt3/papers/metadata/*
    #touch ~/papers/FINISHED
    #rm ~/papers/RUNNING
  done
fi 

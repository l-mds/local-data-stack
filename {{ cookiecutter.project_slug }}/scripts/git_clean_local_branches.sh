#!/bin/bash

git branch | grep -v "^\*" | grep -v master | grep -v main | xargs git branch -d
git fetch -p ; git branch -r | awk '{print $1}' | egrep -v -f /dev/fd/0 <(git branch -vv | grep origin) | awk '{print $1}' | xargs git branch -d
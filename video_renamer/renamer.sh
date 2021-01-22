#!/bin/bash

shopt -s nullglob

for f in *.{mkv,mp4,webm,avi}
do
  size=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$f")
  #echo "($size)|$f|"
  #echo "${f%.*} ($size).${f##*.}"
  mv "$f" "${f%.*} ($size).${f##*.}"
done

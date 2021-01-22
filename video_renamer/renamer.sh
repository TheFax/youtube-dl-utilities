#!/bin/bash

shopt -s nullglob

for f in *.{mkv,mp4,webm,avi}
do
  height=$(ffprobe -v error -show_entries stream=height -of csv=p=0 "$f")
  if [ "$height" -eq 2160 ] || [ "$height" -eq 1080 ] || [ "$height" -eq 720 ]; then

  fi
  mv "$f" "${f%.*} ($height).${f##*.}"
done

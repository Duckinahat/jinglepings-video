#!/usr/bin/env bash

for filename in $1/*.png; do
    [ -e "$filename" ] || continue
    python3 image2ipv6.py "$filename" -X 70 -Y 0 > output/${filename##*/}
done
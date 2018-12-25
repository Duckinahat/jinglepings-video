#!/usr/bin/env bash

mkdir output
avconv -i "$1" -r "$2" -f image2 output/%04d.png

#!/bin/bash
for i in $( ls ); do
    tesseract $i out/"$i out"
done
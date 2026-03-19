#!/bin/sh

BASE="/Users/jaehyeokchoi/Desktop/models"

for dir in "$BASE"/*/; do
	outdir=$(basename "$dir")
	mkdir -p /Users/jaehyeokchoi/Desktop/pns/"$outdir"

	for file in "$dir"/PT/*; do
		python main.py $file $outdir
	done
done

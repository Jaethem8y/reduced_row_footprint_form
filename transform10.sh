#!/bin/sh

BASE="/Users/jaehyeokchoi/Desktop/models"
JOBS=10

for dir in "$BASE"/*/; do
	outdir=$(basename "$dir")
	mkdir -p /Users/jaehyeokchoi/Desktop/pns/"$outdir"

	for file in "$dir"/PT/*; do
		echo "Running $file"

		python main.py "$file" "$outdir" &

		# limit to 10 concurrent jobs
		while [ "$(jobs -r | wc -l)" -ge "$JOBS" ]; do
			sleep 1
		done
	done
done

# wait for all remaining jobs to finish
wait

#!/bin/bash
# Runs the whole simulation campaign in two parallel lanes (about half an hour on two cores), merges the
# results, and validates the memory-depth estimator.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
( python3 campaign.py main ising && python3 campaign.py cold ising && python3 campaign.py noise ising \
  && python3 campaign.py tau ) > log_lane1.txt 2>&1 &
( python3 campaign.py main haar && python3 campaign.py cold haar && python3 campaign.py noise haar \
  && python3 validate_pairs.py ) > log_lane2.txt 2>&1 &
wait
python3 merge.py

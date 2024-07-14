#!/bin/bash

SRC_DIR="by-contestant"
DEST_DIR="by-problem"

mkdir -p "$DEST_DIR"

for contestant_dir in "$SRC_DIR"/*; do
    contestant_name=$(basename "$contestant_dir")
    
    for problem_dir in "$contestant_dir"/*; do
        problem_name=$(basename "$problem_dir")
        
        mkdir -p "$DEST_DIR/$problem_name/$contestant_name"
        cp "$problem_dir"/* "$DEST_DIR/$problem_name/$contestant_name/"
    done
done

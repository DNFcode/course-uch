#!/bin/sh
cd $1
timeout 5s cargo run -q | tail -n +1 | head -c 5k > output
cat output

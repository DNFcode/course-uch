#!/bin/sh
cd $1
cargo new $3
cp -r "$2/$3/." "./$3/src/"
cd "./$3"
cargo run -q < ./src/input | tail -n +1 | head -c 5k > output&
pid=$!
sleep 5

( kill -TERM $pid ) 2>&1

cat output

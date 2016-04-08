#!/bin/sh
cd $1
cargo new $3
cp -r "$2/$3/." "./$3/src/"
cd "./$3"
cargo run -q

#!/bin/sh
cd ../../rs_cargo
cargo new $1
cp -r "../files/$1/." "./$1/src/"
cd "./$1"
cargo run -q

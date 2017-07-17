#!/bin/sh

cat "$1" | pv -b | nc 192.168.0.10 1234

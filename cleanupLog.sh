#!/bin/bash

if [ ! -f "accessc.log1" ]; then
    cp "accessc.log" "accessc.log1"
else
    for i in {6..2}; do
        if [ -f "accessc.log$i" ]; then
            cp "accessc.log$((i-1))" "accessc.log$i"
        fi
    done
    cp "accessc.log" "accessc.log1"
fi

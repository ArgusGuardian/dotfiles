#!/bin/bash

while true; do
	xsetroot -name "$(date +"%a, %B %d %l:%M%p" | sed 's/  / /g')"
	sleep 1m
done &

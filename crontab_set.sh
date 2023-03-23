#!/bin/bash

# Use crontab to schedule the command to run every Friday at 11pm
(crontab -l 2>/dev/null; echo "0 23 * * 5 /path/to/command") | crontab -

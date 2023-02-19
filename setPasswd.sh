#!/bin/bash

# Use the mysql password for the user accessc
echo "Enter the mysql password that was just set:"
read password

# Replace the word PASSWORD with the new mysql password
sed -i "s/PASSWORD/$password/g" accessc.py
sed -i "s/PASSWORD/$password/g" scanIn.py

echo "Script passwords updated."

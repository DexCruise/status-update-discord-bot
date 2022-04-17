#!/bin/sh

echo "enter discord bot token: "
python -c "print(input())" > token
pip install -U discord json icmplib time requests

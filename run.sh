#!/bin/bash

cd "$(dirname "$0")"
source venv/bin/activate
python3 src/main.py --inbox inbox "$@" 2>>run.log
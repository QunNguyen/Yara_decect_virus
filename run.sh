#!/bin/bash
#venv
# python3 -m venv mmh
# source mmh/bin/activate
#conda
conda create -n mmh python=3.6
conda activate mmh
pip install -r requirements.txt
python3 main_v3.py

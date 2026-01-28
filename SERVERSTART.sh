#!/bin/bash

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload --port 9000
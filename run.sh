#!/bin/bash
# Activate the virtual environment
source .venv/bin/activate

# Run the server
uvicorn app.main:app --reload


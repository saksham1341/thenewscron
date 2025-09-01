#!/bin/bash

source .venv/bin/activate
dotenv run -- python -m executor
deactivate
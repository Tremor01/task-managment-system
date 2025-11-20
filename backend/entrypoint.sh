#!/bin/bash
sleep 3

# shellcheck disable=SC2164
cd /libs/shared

alembic upgrade head

# shellcheck disable=SC2164
cd /project/source

python3 main.py

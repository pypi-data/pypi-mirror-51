#!/usr/bin/env bash

set -ex

bash scripts/clean.sh
python setup.py sdist bdist_wheel

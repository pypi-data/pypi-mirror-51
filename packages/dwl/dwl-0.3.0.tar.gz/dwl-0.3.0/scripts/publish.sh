#!/usr/bin/env bash

set -ex

bash scripts/build.sh
twine upload dist/*

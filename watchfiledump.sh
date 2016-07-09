#!/bin/sh
watchmedo shell-command -c "clear; mv $1.dump $1.dump.orig; python -m rv.tools.filedump $1 2>&1 | tee $1.dump; echo; diff -Naur $1.dump.orig $1.dump" -p '*.sunvox;*.sunsynth;*.py' -R -W .

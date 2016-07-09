#!/bin/sh
watchmedo shell-command -c "clear; sleep 1; diff -Naur $1.dump.orig $1.dump" -p '*.sunvox;*.sunsynth' -R -W .

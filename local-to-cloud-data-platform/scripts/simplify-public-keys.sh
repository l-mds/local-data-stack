#!/bin/bash
grep -v '^\#' public-age-keys.txt | tr -d '[:space:]' | tr '\n' ',' | sed 's/,$//'
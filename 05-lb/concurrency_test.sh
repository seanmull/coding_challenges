#!/bin/bash
curl --parallel --parallel-immediate --parallel-max "$1" --config urls.txt

#!/bin/bash
python grep.py text.txt "\d+" | diff - text.txt

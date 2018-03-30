#!/usr/bin/env python3
#   interface.py
#   Interacts with scene7's backend to automate the process of finding assets, getting their size, ading them to a job queue
#   where the size < 1GB total and sending the jobs out for downloading.

import requests, csv

#   readCSV should accept a CSV file with multiple rows and one column, no headers

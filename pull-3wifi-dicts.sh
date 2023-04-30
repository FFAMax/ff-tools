#!/bin/bash

start_year=2020
current_year=$(date +%Y)
current_month=$(date +%m)
current_day=$(date +%d)

for year in $(seq $start_year $current_year); do
  for month in $(seq -w 1 12); do
    if [ $year -eq $current_year ] && [ $month -gt $current_month ]; then
      break
    fi
    last_day_of_month=$(cal $month $year | awk 'NF {DAYS = $NF}; END {print DAYS}')
    for day in $(seq -w 1 $last_day_of_month); do
      if [ $year -eq $current_year ] && [ $month -eq $current_month ] && [ $day -gt $current_day ]; then
        break
      fi
      file_url="http://3wifi.stascorp.com/3wifi-dic-$year-$month-$day.7z"
      wget $file_url
      sleep 1
    done
  done
done

#!/bin/bash

source define_colors.sh
echo -e "${Z}"

FILE="$1"
if [ -z "$1" ]; then
  echo "Usage <file><edit>"
  exit 1
fi


PIPELINE="$2"
if [ -z "$2" ]; then
  echo "Usage <file><edit>"
  exit 2
fi

function wait_for_kate_async() {
  kate "$@" &
  pid=$! # or $(jobs -p)
  wait ${pid}
}

function wait_for_kate_sync() {
  kate "$@"
  while pgrep -x "kate" > /dev/null; do
    sleep 1
  done
}


count=0
while read line; do
  #echo "$line"
  id=$(echo "${line}" | awk 'BEGIN{OFS="\t"} {print $1,$2,$3}')
  if [ -z "${id}" ]; then
    continue
  fi
  echo -e "${B}${id}${Z}"
  r=$(grep -Hn "^${id}" "${PIPELINE}")
  l=$(echo "${r}" | awk -F  ':' '{print $2}')
  echo "${PIPELINE} @ ${l}"
  
  wait_for_kate_sync --line ${l} "${PIPELINE}"

  count=$(($count + 1))
done < "${FILE}"
echo "Count ${count}"


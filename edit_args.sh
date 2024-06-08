#!/bin/bash

source define_colors.sh
echo -e "${Z}"


DIR=.
if [[ ! $1 =~ [0-9]{8}-[nvars] ]]; then
  DIR="$1"
  shift
fi
echo "Target directory: $DIR"

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

for id in "$@"; do
  echo "${id}"
  r=$(grep -Hn "^${id}" "${DIR}"/*)
  f=$(echo "${r}" | awk -F  ':' '{print $1}')
  l=$(echo "${r}" | awk -F  ':' '{print $2}')
  echo "${f} @ ${l}"
  
  wait_for_kate_sync --line ${l} "${f}" 
  
done


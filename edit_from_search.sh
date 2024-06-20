#!/bin/bash

source define_colors.sh
source define_kate.sh
echo -e "${Z}"

REGEX='`'
if [ ! -z "$1" ]; then
  REGEX="$1"
fi
echo -e "Regex: ${G}${REGEX}${Z}"

DIR=.
if [ ! -z "$2" ]; then
  DIR="$2"
fi
echo -e "Target directory: ${Y}${DIR}${Z}"

grep -Hn "${REGEX}" "${DIR}"/* | awk -F ':' '{print $2,$1}' | while read -r line; do
  echo -e "${C}${line}${Z}"
  wait_for_kate --line ${line}
done

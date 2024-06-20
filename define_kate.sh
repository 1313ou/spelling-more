#!/bin/bash

function wait_for_kate_back() {
  kate "$@" &
  pid=$! # or $(jobs -p)
  wait ${pid}
}

function wait_for_kate_poll() {
  kate "$@"
  while pgrep -x "kate" > /dev/null; do
    sleep 1
  done
}

function wait_for_kate() {
  kate --block "$@"
  wait
}

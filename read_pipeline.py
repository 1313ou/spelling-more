#!/usr/bin/python3

import argparse
import sys

import process
from process import *


def process_line(line, checkf):
    fields = line.split('\t')
    last = len(fields) - 1
    input_text = fields[last]
    rowid = "\t".join(fields[0:last])
    r = checkf(input_text)
    if r:
        #print(f"{rowid}\t{r}\t{input_text}")
        print(f"{rowid}\t{r}")
        return 1
    return 0


def read_file(file, resume, checkf):
    count = 0
    with open(file) as fp:
        for line in fp:
            count += process_line(line.strip(), checkf)
    print(f"{count} processed")


def get_processing(name):
    return globals()[name] if name else process.default_process


def main():
    parser = argparse.ArgumentParser(description="scans the pipeline")
    parser.add_argument('text', type=str, help='text')
    parser.add_argument('--resume', type=int, help='line to resume from')
    parser.add_argument('--processing', type=str, help='processing function to apply')
    args = parser.parse_args()
    processing = get_processing(args.processing)
    if processing:
        print(processing, file=sys.stderr)
    read_file(args.text, args.resume, processing)


if __name__ == '__main__':
    main()

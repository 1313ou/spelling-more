#!/usr/bin/python3

import argparse
import sys
import wordnet_yaml
import wordnet
import process
from process import *


def process_text(input_text, rowid, checkf):
    r = checkf(input_text)
    if r:
        print(f"{rowid}\t{input_text}\t{r}")
        return 1
    return 0


def get_processing(name):
    return globals()[name] if name else process.default_process


def load():
    return wordnet_yaml.load()


def main():
    parser = argparse.ArgumentParser(description="load from yaml")
    parser.add_argument('yaml', type=str, help='database')
    parser.add_argument('--processing', type=str, help='processing function to apply')
    args = parser.parse_args()
    processing = get_processing(args.processing)
    print(processing, file=sys.stderr)
    wn = load()
    print('loaded', file=sys.stderr)
    for synset in wn.synsets:
        for definition in synset.definitions:
            process_text(definition.text, synset.id, processing)
        for example in synset.examples:
            process_text(example.text, synset.id, processing)
    print('processed', file=sys.stderr)


if __name__ == '__main__':
    main()

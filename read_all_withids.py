#!/usr/bin/python3

import argparse
import sys
import sqlite3
from tqdm.auto import tqdm
import process
from process import *

sql_union = """
SELECT 'sam' AS type, sampleid AS tablerowid, sample AS `text`, oewnsynsetid FROM samples INNER JOIN synsets USING(synsetid)
UNION
SELECT 'def' AS type, synsetid AS tablerowid, definition AS `text`, oewnsynsetid FROM synsets
"""
sql = f"SELECT oewnsynsetid, tablerowid, type, `text` FROM ({sql_union}) ORDER BY oewnsynsetid, tablerowid;"
sql_count = f"SELECT COUNT(*) FROM ({sql_union});"
print(sql, file=sys.stderr)

progress = False


def process_text(input_text, rowid, checkf):
    r = checkf(input_text)
    if r:
        print(f"{rowid}\t{input_text}\t{r}")
        return 1
    return 0


def count(conn, resume):
    cursor = conn.cursor()
    sql2 = build_sql(sql_count, resume)
    cursor.execute(sql2)
    return cursor.fetchone()[0]


def build_sql(sql, resume):
    return sql + f" WHERE oewnsynsetid >= {resume}" if resume else sql


def read(file, resume, checkf):
    conn = sqlite3.connect(file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql2 = build_sql(sql, resume)
    cursor.execute(sql2)
    n = count(conn, resume)
    pb = tqdm(total=n, disable=not progress)
    process_count = 0
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        rowid = row["tablerowid"]
        type = row["type"]
        text = row["text"]
        oewnsynsetid = row["oewnsynsetid"]
        if process_text(text, oewnsynsetid, checkf):
            process_count += 1
        pb.update(1)
    conn.close()
    print(f"{process_count} processed")


def get_processing(name):
    return globals()[name] if name else process.default_process


def main():
    parser = argparse.ArgumentParser(description="scans the examples and definitions from sqlite file")
    parser.add_argument('database', type=str, help='database')
    parser.add_argument('--resume', type=int, help='row to resume from')
    parser.add_argument('--processing', type=str, help='processing function to apply')
    args = parser.parse_args()
    processing = get_processing(args.processing)
    if processing:
        print(processing, file=sys.stderr)
    read(args.database, args.resume, processing)


if __name__ == '__main__':
    main()

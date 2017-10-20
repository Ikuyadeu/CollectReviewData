#!/usr/bin/env python3
"""
Get file revised from csv
"""
from csv import DictReader
from sys import argv, stdout
from os import mkdir, path
from time import sleep
from requests import get, exceptions

USAGE = "Usage: python3 src/RequestFileDiff.py current_db requests_header start end\
[--from-ini] [--from-prev]"

FROM_BASE = 0
FROM_INI = 1
FROM_PREV = 2

def main():
    """
    Main
    """
    base_mode = FROM_BASE
    if "--from-ini" in argv:
        base_mode = FROM_INI
        argv.remove("--from-ini")
    elif "--from-prev" in argv:
        base_mode = FROM_PREV
        argv.remove("--from-prev")

    if len(argv) != 5 or "-h" in argv or "--help" in argv:
        print(USAGE)
        return

    # Set argument
    current_db = argv[1]
    requests_header = argv[2] # exp) https://review.openstack.org
    start = int(argv[3])
    end = int(argv[4])

    # Make project's directory
    projects_path = "./revision_files/" + current_db
    if not path.exists(projects_path):
        mkdir(projects_path)

    with open(current_db + ".csv", 'r') as csvfile:
        reader = DictReader(csvfile, lineterminator='\n')
        for i, rev_file in enumerate(reader, start=1):
            if i >= start:
                break

        for i, rev_file in enumerate(reader, start=start):
            if i > end:
                break
            f_file_name = rev_file["f_file_name"]
            rev_patch_set_num = rev_file["rev_patchSetNum"]

            requests_url = "/".join([requests_header,
                                     "changes", rev_file["ch_id"],
                                     "revisions", rev_patch_set_num,
                                     "files", f_file_name,
                                     "diff"])
            params = make_param_from(int(rev_patch_set_num), base_mode)

            for _ in range(1, 5):
                try:
                    response = get(requests_url, params=params)
                    if response.status_code != 200:
                        print("\n" + str(i) + ": " + str(response.status_code))
                        sleep(30)
                        continue
                except exceptions.RequestException as err:
                    print("\n" + str(i) + ": " + str(err))
                    sleep(30)
                else:
                    break
            response.encoding = 'utf-8'

            # Output
            revisions_path = "/".join([projects_path, rev_file["rev_id"]])
            if not path.exists(revisions_path):
                mkdir(revisions_path)
            with open("/".join([revisions_path, f_file_name + ".json"]), 'w') as rev_file:
                rev_file.write(response.text)
            stdout.write("\rFile: %d / %d" % (i, end))

def make_param_from(rev_patch_set_num, base_mode):
    """
    Return requests parameter
    """
    if rev_patch_set_num == 1 or base_mode == FROM_BASE:
        return None
    elif base_mode == FROM_INI:
        return {"base": "1"}
    elif base_mode == FROM_PREV:
        return {"base": str(rev_patch_set_num-1)}


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Get file revised from csv
"""
import csv
import sys
import os
from time import sleep
import requests

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
    if "--from-ini" in sys.argv:
        base_mode = FROM_INI
        sys.argv.remove("--from-ini")
    elif "--from-prev" in sys.argv:
        base_mode = FROM_PREV
        sys.argv.remove("--from-prev")

    if len(sys.argv) != 5 or "-h" in sys.argv or "--help" in sys.argv:
        print(USAGE)
        return

    # Set argument
    current_db = sys.argv[1]
    requests_header = sys.argv[2] # exp) https://review.openstack.org
    start = int(sys.argv[3])
    end = int(sys.argv[4])

    # Make project's directory
    projects_path = "./revision_files/" + current_db
    if not os.path.exists(projects_path):
        os.mkdir(projects_path)

    with open(current_db + ".csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile, lineterminator='\n')

        for i, rev_file in enumerate(reader, start=1):
            if i < start:
                continue
            if i > end:
                break
            f_file_name = rev_file["f_file_name"]
<<<<<<< HEAD
            rev_id = rev_file["rev_id"]
=======
>>>>>>> 64c9aaa3b30084f86221bdde53ad922a694c31ff
            rev_patch_set_num = int(rev_file["rev_patchSetNum"])

            requests_url = "/".join([requests_header,
                                     "changes", rev_file["ch_id"],
                                     "revisions", str(rev_patch_set_num),
                                     "files", f_file_name,
                                     "diff"])
            params = make_param_from(rev_patch_set_num, base_mode)

<<<<<<< HEAD
            try:
                response = requests.get(requests_url, params=params)
            except requests.ConnectionError as err:
                print(" " + str(i) + ": " + str(err))
                sleep(5)
                response = requests.get(requests_url, params=params)
            response.encoding = 'utf-8'

            # Output
            revisions_path = "/".join([projects_path, rev_id])
=======

            for _ in range(1, 3):
                try:
                    response = requests.get(requests_url, params=params)
                except requests.ConnectionError as err:
                    print("\n" + str(i) + ": " + str(err))
                    sleep(10)
                else:
                    break
            response.encoding = 'utf-8'

            # Output
            revisions_path = "/".join([projects_path, rev_file["rev_id"]])
>>>>>>> 64c9aaa3b30084f86221bdde53ad922a694c31ff
            if not os.path.exists(revisions_path):
                os.mkdir(revisions_path)
            with open("/".join([revisions_path, f_file_name + ".json"]), 'w') as rev_file:
                rev_file.write(response.text)
            sys.stdout.write("\rFile: %d / %d" % (i, end))

def make_param_from(rev_patch_set_num, base_mode):
    """
    Return requests parameter
    """
    if base_mode == FROM_BASE or rev_patch_set_num == 1:
        return None
    elif base_mode == FROM_INI:
        return {"base": "1"}
    elif base_mode == FROM_PREV:
        return {"base": str(rev_patch_set_num-1)}


if __name__ == '__main__':
    main()

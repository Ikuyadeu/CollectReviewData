#!/usr/bin/env python3
"""
Get file revised from csv
Usage:
$ python3 src/RequestFileDiff.py gm_openstack https://review.openstack.org
"""

import csv
import sys
import os
from time import sleep
import requests

def main():
    """
    Main 41001
    """
    # Set argument
    assert(len(sys.argv) == 5)
    current_db = sys.argv[1]
    requests_header = sys.argv[2] # exp) https://review.openstack.org
    start = int(sys.argv[3])
    end = int(sys.argv[4])

    # Make project's directory
    projects_path = "./revision_files/" + current_db
    if not os.path.exists(projects_path):
        os.mkdir(projects_path)

    csv_len = sum(1 for line in open(current_db + ".csv", 'r'))

    with open(current_db + ".csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile, lineterminator='\n')

        for i, rev_file in enumerate(reader, start=1):
            if i < start:
                continue
            if i >= end:
                break
            f_file_name = rev_file["f_file_name"]
            rev_id = rev_file["rev_id"]
            rev_patchSetNum = int(rev_file["rev_patchSetNum"])
            if rev_patchSetNum == 1:
                requests_url = "/".join([requests_header,
                                        "changes", rev_file["ch_id"],
                                        "revisions", str(rev_patchSetNum),
                                        "files", f_file_name,
                                        "diff"])
                print("\n"+requests_url)
            else:
                requests_url = "/".join([requests_header,
                                        "changes", rev_file["ch_id"],
                                        "revisions", str(rev_patchSetNum),
                                        "files", f_file_name,
                                        "diff?base="+str(rev_patchSetNum-1)])
                print("\n"+requests_url)

            try:
                response = requests.get(requests_url)
            except requests.ConnectionError as err:
                print(str(i) + ": " + str(err))
                sleep(5)
                response = requests.get(requests_url)

            # Output
            revisions_path = "/".join([projects_path, rev_id])
            if not os.path.exists(revisions_path):
                os.mkdir(revisions_path)
            with open("/".join([revisions_path, f_file_name + ".json"]), 'w') as rev_file:
                rev_file.write(response.text)
            sys.stdout.write("\rFile: %d / %d" % (i, end))

if __name__ == '__main__':
    main()

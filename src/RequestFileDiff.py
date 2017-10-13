#!/usr/bin/env python3
"""
Get file revised from csv
Usage:
$ python3 src/RequestFileDiff.py gm_openstack https://review.openstack.org
"""

import csv
import sys
import os
import requests
from time import sleep

def main():
    """
    Main
    """
    # Set argument
    argv = sys.argv
    argc = len(argv)
    if argc == 3:
        current_db = argv[1]
        requests_header = argv[2]
    else:
        current_db = "gm_openstack"
        requests_header = "https://review.openstack.org"

    # Make project's directory
    projects_path = "./revision_files/" + current_db
    if not os.path.exists(projects_path):
        os.mkdir(projects_path)

    csv_len = 0
    with open(current_db + ".csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile, lineterminator='\n')
        csv_len = len(list(reader))

    with open(current_db + ".csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile, lineterminator='\n')

        for i, rev_file in enumerate(reader, start=1):
            rev_id = rev_file["rev_id"]
            f_file_name = rev_file["f_file_name"]

            #try:
            # Get json data
            requests_url = "/".join([requests_header,
                                    "changes", rev_file["ch_id"],
                                    "revisions", rev_id,
                                    "files", f_file_name,
                                    "diff"])
            response = requests.get(requests_url)

            # Output
            revisions_path = "/".join([projects_path, rev_id])
            if not os.path.exists(revisions_path):
                os.mkdir(revisions_path)
            with open("/".join([revisions_path, f_file_name + ".json"]), 'w') as rev_file:
                rev_file.write(response.text)
            sys.stdout.write("\rFile: %d / %d" % (i, 4528235))
            if i % 100 == 0:
                sleep(30)
                print()
            #except connectionError:
            #    sleep(30)
            #    print("%d" % (rev_file["rev_id"]))

if __name__ == '__main__':
    main()

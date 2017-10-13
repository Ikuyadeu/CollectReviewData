#!/usr/bin/env python3
"""
Get file list from mysql
Usage:
$ python3 src/GetFileList.py gm_openstack user passwd
Output:
./gm_openstack.csv
    - "ch_id": Change id
    - "rev_id": Revision id
    - "f_file_name": Encoded file path
"""

import sys
import csv
from urllib.parse import quote_plus
from collections import defaultdict
import MySQLdb

def main():
    """
    Main
    """
    # set argument
    argv = sys.argv
    argc = len(argv)
    if argc == 4:
        current_db = argv[1]
        user = argv[2]
        passwd = argv[3]
    else:
        current_db = "gm_openstack"
        user = "root"
        passwd = ""

    # Define dictionary
    t_revision_dic = defaultdict(lambda: [])
    t_file_dic = defaultdict(lambda: [])

    # Connect DB
    connection = MySQLdb.connect(db=current_db, user=user, passwd=passwd)
    cursor = connection.cursor()

    # Get changes
    sys.stdout.write("\rCollecting changes...")
    sql = "SELECT id, ch_Id, ch_changeId, ch_changeIdNum \
           FROM t_change"
    cursor.execute(sql)
    changes = cursor.fetchall()

    # Get revisions
    sys.stdout.write("\rCollecting revisions...")
    sql = "SELECT id, rev_Id, rev_changeId \
           FROM t_revision"
    cursor.execute(sql)
    revisions = cursor.fetchall()

    # Get files
    sys.stdout.write("\rCollecting files...")
    sql = "SELECT f_fileName, f_revisionId \
           FROM t_file"
    cursor.execute(sql)
    files = cursor.fetchall()

    # Close DB connection
    connection.close()

    # Store data into t_revisionDic
    for revision in revisions:
        t_revision_dic[revision[2]].append(revision)
    for rev_file in files:
        t_file_dic[int(rev_file[1])].append(rev_file)

    # File list for output
    output_files = []

    # Search from changes
    changes_len = len(changes)
    for i, change in enumerate(changes):
        ch_revisions = t_revision_dic[change[0]]
        ch_id = change[1]
        ch_change_id = change[2]
        ch_change_id_num = change[3]
        revisions_len = len(ch_revisions)
        # Search from revisions
        for j, revision in enumerate(ch_revisions):
            rev_files = t_file_dic[revision[0]]
            rev_id = revision[1]
            rev_change_id = revision[2]
            output_files += [[ch_id, ch_change_id, ch_change_id_num,
                              rev_id, rev_change_id, quote_plus(rev_file[0])]
                             for rev_file in rev_files]
            sys.stdout.write("\rChange: %d / %d, Revision: %d / %d" %
                             (i, changes_len, j, revisions_len))

    # Output
    with open(current_db + ".csv", 'w') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        sys.stdout.write("\rOutputting files...")
        writer.writerow(["ch_id", "ch_change_id", "ch_change_id_num",
                         "rev_id", "rev_change_id", "f_file_name"])
        writer.writerows(output_files)

if __name__ == '__main__':
    main()

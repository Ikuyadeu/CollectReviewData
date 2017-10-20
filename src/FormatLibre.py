#!/usr/bin/env python3
"""
Format libreoffice csv
"""
from csv import DictReader, DictWriter
from sys import stdout

OD_EXTENSION = [
    ".odt",
    ".ott",
    ".odm",
    ".ods",
    ".ots",
    ".odg",
    ".otg",
    ".odp",
    ".otp",
    ".odf",
    ".odb",
    ".oxt"
]

def main():
    """
    Main
    """
    file_list = []

    with open("./gm_libreoffice.csv", 'r') as csvfile:
        reader = DictReader(csvfile, lineterminator='\n')

        for rev_file in reader:
            f_file_name = str(rev_file["f_file_name"])
            if not any([f_file_name.endswith(x) for x in OD_EXTENSION]):
                file_list.append(rev_file)

    with open("./gm_libreoffice2.csv", 'w') as csvfile:
        writer = DictWriter(csvfile,
                            ["ch_id", "ch_change_id",
                             "rev_id", "rev_change_id",
                             "f_file_name", "rev_patchSetNum"],
                            lineterminator='\n')
        stdout.write("\rOutputting files...")
        writer.writeheader()
        writer.writerows(file_list)

if __name__ == '__main__':
    main()

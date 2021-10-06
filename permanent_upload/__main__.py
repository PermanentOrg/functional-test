#!/usr/bin/env python3

import argparse
import logging
import sys
import os
import time
import string
import random
from tabulate import tabulate

from .permanent import PermanentAPI


def get_file_list(path):
    file_list = []
    for root, _, files in os.walk(path):
        for name in files:
            file_list.append(os.path.join(root, name))
    logging.debug(file_list)
    return file_list


def parse_args():
    parser = argparse.ArgumentParser(
        description="Test that uploading to Permanent.org works correctly",
    )
    parser.add_argument(
        "environment",
        choices=["local", "dev", "staging", "www"],
        help="environment that the script should run on",
    )
    parser.add_argument(
        "path",
        help="directory containing files for upload",
    )

    return parser.parse_args()


def main(environment, path):
    if not os.path.isdir(path):
        logging.critical("The path argument is not a directory")
        return
    unix_timestamp = int(time.time())
    email = f"engineers+prmnttstr{unix_timestamp}@permanent.org"
    print("User account email:", email)
    password = "".join(random.choice(string.ascii_letters) for i in range(12))
    timeout = 60
    print(f"Current timeout is {timeout} seconds")

    api = PermanentAPI(f"https://{environment}.permanent.org")
    createaccount_result = api.create_account(email, password)
    login_result = api.login(email, password)
    archive = login_result.response["ArchiveVO"]
    api.get_archive(archive["archiveId"], archive["archiveNbr"])
    api.get_account(createaccount_result.response["AccountVO"]["accountId"])
    api.logged_in()
    parent_folder_id, parent_folder_link_id = api.get_folder_info()

    files = get_file_list(path)
    results = []
    headers = ["File Name", "Type", "Status", "File Formats", "Time"]
    for f in files:
        logging.info("Processing %s", f)
        results.append(
            api.file_upload(f, parent_folder_id, parent_folder_link_id, timeout)
        )

    print(tabulate(results, headers, tablefmt="github"))


if __name__ == "__main__":
    args = parse_args()
    main(args.environment, args.path)

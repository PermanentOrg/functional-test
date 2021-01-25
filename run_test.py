#!/usr/bin/env python3

import logging
import sys
import os
import time
import string
import random
from tabulate import tabulate
import requests


BASE_URL = ""
API_KEY = ""

class PermanentRequest():
    csrf = ""
    session = requests.Session()

    def __init__(self, path, data=[]):
        '''
        Craft the fields required to make a request.
        '''
        self.body = {
            "RequestVO": {
                "data": data,
                "apiKey": API_KEY,
                "csrf": PermanentRequest.csrf
             },
        }
        self.url = f"{BASE_URL}{path}"
        self.make_request()

    def make_request(self):
        '''
        Make a JSON post request to the API backend.
        '''
        logging.debug("Request url: %s", self.url)
        logging.debug("Request json: %s", self.body)
        response = PermanentRequest.session.post(self.url, json=self.body)
        if not response.ok:
            raise_for_status(response)
        json_resp = response.json()
        logging.debug("Response body: %s", json_resp)
        assert json_resp["isSuccessful"]
        self.response = json_resp["Results"][0]["data"][0]
        PermanentRequest.csrf = json_resp["csrf"]


def get_presigned_url(record_vo):
    body = [{
        'RecordVO': record_vo,
        'SimpleVO': {
            'key': 'type',
            'value': 'application/octet-stream',
        },
    }]
    request = PermanentRequest('/api/record/getPresignedUrl', data=body)
    return request.response['SimpleVO']['value']


def upload_to_s3(s3_url, file_path, presigned_post):
    fields = presigned_post['fields']
    with open(file_path, 'rb') as f:
        fields['Content-Type'] = 'application/octet-stream'
        logging.debug('Data to be form encoded for S3:')
        logging.debug(fields)
        r = requests.post(
            presigned_post['url'],
            data=fields,
            files={'file': f}
        )
        r.raise_for_status()


def register_record(record_vo, s3_url):
    body = {
        'RecordVO': record_vo,
        'SimpleVO': {
            'key': 's3url',
            'value': s3_url,
        },
    }
    request = PermanentRequest('/api/record/registerRecord', data=body)
    return request.response['RecordVO']


def test_file_upload(file_path, parent_folder_id, parent_folder_link_id, timeout):
    '''
    Perform the file upload requests, and then poll for status until the timeout.
    '''
    filename = os.path.basename(file_path)

    record_vo = {
        "parentFolderId": parent_folder_id,
        "parentFolder_linkId": parent_folder_link_id,
        "displayName": filename,
        "uploadFileName": filename,
        "size": os.path.getsize(file_path),
        "derivedCreatedDT": int(time.time()),
    }

    s3_info = get_presigned_url(record_vo)

    logging.debug('S3 info:')
    logging.debug(s3_info)

    upload_to_s3(s3_info['destinationUrl'], file_path, s3_info['presignedPost'])
    created_record_vo  = register_record(record_vo, s3_info['destinationUrl'])

    attempts, processed_record = measure_post_upload_processing(created_record_vo, timeout)
    result = [
        filename,
        processed_record["type"].split(".")[-1],
        processed_record["status"].split(".")[-1],
        ",".join([
            vo["type"].split(".")[-1]
            for vo
            in processed_record["FileVOs"]
        ]),
        attempts,
    ]
    return result


def measure_post_upload_processing(record_vo, timeout):
    record_id = record_vo['recordId']
    archive_number = record_vo['archiveNbr']

    i = 0
    status = ""
    record = ""

    while (i < timeout and status != "status.generic.ok"):
        record = get_record(record_id, archive_number)
        status = record["status"]
        time.sleep(1)
        i += 1
    return i, record


def get_record(record_id, archive_nbr):
    logging.info("Get record %s", record_id)
    body = [{
        "RecordVO": {
            "recordId": record_id,
            "archiveNbr": archive_nbr,
         }
    }]
    request = PermanentRequest("/api/record/get", data=body)
    return request.response["RecordVO"]


def get_folder_info():
    logging.info("Get root folder")
    folder_request = PermanentRequest("/api/folder/getRoot")
    folder = folder_request.response["FolderVO"]["ChildItemVOs"][1]
    return folder["folderId"], folder["FolderLinkVOs"][0]["folder_linkId"]


def create_account(email, password):
    logging.info("Create account  %s : %s", email, password)
    body = [{
        "AccountVO":{
            "primaryEmail": email,
            "primaryPhone": None,
            "fullName": "Functional Filetype Test",
            "agreed": True,
            "optIn": False,
            "inviteCode": ""
        },
        "AccountPasswordVO":{
            "password": password,
            "passwordVerify": password,
        }
    }]
    return PermanentRequest("/api/account/post", data=body)

def login(email, password):
    logging.info("Login as %s", email)
    body = [{
        "AccountVO": {
            "primaryEmail": email,
            "rememberMe": False,
            "keepLoggedIn": False
        },
        "AccountPasswordVO":{
            "password": password
        }
    }]
    return PermanentRequest("/api/auth/login", data=body)

def get_archive(archive_id, archive_nbr):
    logging.info("Get archive")
    body = [{
        "ArchiveVO": {
            "archiveNbr": archive_nbr,
            "archiveId": archive_id
        }
    }]
    return PermanentRequest("/api/archive/get", data=body)


def get_account(account_id):
    logging.info("Get account")
    body = [{ "accountId": account_id }]
    return PermanentRequest("/api/account/get", data=body)

def logged_in():
    return PermanentRequest("/api/auth/loggedIn")

def raise_for_status(response):
    """
    Custom exceptions with more appropriate error message.
    """
    http_error_msg = str(response.status_code)

    if 400 <= response.status_code < 500:
        http_error_msg += " Client Error: "

    elif 500 <= response.status_code < 600:
        http_error_msg += " Server Error: "

    http_error_msg += response.reason

    raise requests.exceptions.HTTPError(http_error_msg, response=response)


def get_file_list(path):
    file_list = []
    for root, _, files in os.walk(path):
        for name in files:
            file_list.append(os.path.join(root, name))
    logging.debug(file_list)
    return file_list


def main():
    logging.getLogger().setLevel('INFO')
    global BASE_URL, API_KEY
    if len(sys.argv) != 4:
        logging.critical("This script requires 3 arguments: environment, api key, and "
                         " a path to files to upload.")
        return
    if not os.path.isdir(sys.argv[3]):
        logging.critical("The 3rd argument is not a directory path")
        return
    BASE_URL = f"https://{sys.argv[1]}.permanent.org"
    API_KEY = sys.argv[2]
    email = "engineers+prmnttstr{}@permanent.org".format(int(time.time()))
    print("User account email:", email)
    password = "".join(random.choice(string.ascii_letters) for i in range(12))
    timeout = 60
    print(f"Current timeout is {timeout} seconds")

    createaccount_result = create_account(email, password)
    login_result = login(email, password)
    archive = login_result.response["ArchiveVO"]
    get_archive(archive["archiveId"], archive["archiveNbr"])
    get_account(createaccount_result.response["AccountVO"]["accountId"])
    logged_in()
    parent_folder_id, parent_folder_link_id = get_folder_info()

    files = get_file_list(sys.argv[3])
    results = []
    headers = ["File Name", "Type", "Status", "File Formats", "Time"]
    for f in files:
        logging.info("Processing %s", f)
        results.append(test_file_upload(f, parent_folder_id, parent_folder_link_id, timeout))

    print(tabulate(results, headers, tablefmt="github"))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import logging
import sys
import os
import time
import string
import random
import requests

from . import utils


class PermanentRequest:
    csrf = ""
    session = requests.Session()

    def __init__(self, base_url, path, data=[]):
        """
        Craft the fields required to make a request.
        """
        self.body = {
            "RequestVO": {"data": data, "csrf": PermanentRequest.csrf},
        }
        self.url = f"{base_url}{path}"
        self.make_request()

    def make_request(self):
        """
        Make a JSON post request to the API backend.
        """
        logging.debug("Request url: %s", self.url)
        logging.debug("Request json: %s", self.body)
        response = PermanentRequest.session.post(self.url, json=self.body)
        if not response.ok:
            utils.raise_for_status(response)
        json_resp = response.json()
        logging.debug("Response body: %s", json_resp)
        assert json_resp["isSuccessful"]
        self.response = json_resp["Results"][0]["data"][0]
        PermanentRequest.csrf = json_resp["csrf"]


class PermanentAPI:
    def __init__(self, base_url=None):
        if not base_url:
            raise Exception("Need `base_url` upon object creation")
        self.base_url = base_url

    def _measure_post_upload_processing(self, record_vo, timeout):
        record_id = record_vo["recordId"]
        archive_number = record_vo["archiveNbr"]

        i = 0
        status = ""
        record = ""

        while i < timeout and status != "status.generic.ok":
            record = self._get_record(record_id, archive_number)
            status = record["status"]
            time.sleep(1)
            i += 1
        return i, record

    def _register_record(self, record_vo, s3_url):
        logging.info("Register record for file %s", record_vo["displayName"])
        body = {
            "RecordVO": record_vo,
            "SimpleVO": {
                "key": "s3url",
                "value": s3_url,
            },
        }
        request = PermanentRequest(
            self.base_url, "/api/record/registerRecord", data=body
        )
        return request.response["RecordVO"]

    def _get_presigned_url(self, record_vo):
        logging.info("Get pre-signed URL for %s", record_vo["displayName"])
        body = [
            {
                "RecordVO": record_vo,
                "SimpleVO": {
                    "key": "type",
                    "value": "application/octet-stream",
                },
            }
        ]
        request = PermanentRequest(
            self.base_url, "/api/record/getPresignedUrl", data=body
        )
        return request.response["SimpleVO"]["value"]

    def _get_record(self, record_id, archive_nbr):
        logging.info("Get record %s", record_id)
        body = [
            {
                "RecordVO": {
                    "recordId": record_id,
                    "archiveNbr": archive_nbr,
                }
            }
        ]
        request = PermanentRequest(self.base_url, "/api/record/get", data=body)
        return request.response["RecordVO"]

    def file_upload(self, file_path, parent_folder_id, parent_folder_link_id, timeout):
        """
        Perform the file upload requests, and then poll for status until the timeout.
        """
        filename = os.path.basename(file_path)

        record_vo = {
            "parentFolderId": parent_folder_id,
            "parentFolder_linkId": parent_folder_link_id,
            "displayName": filename,
            "uploadFileName": filename,
            "size": os.path.getsize(file_path),
            "derivedCreatedDT": int(time.time()),
        }

        s3_info = self._get_presigned_url(record_vo)
        utils.upload_to_s3(
            s3_info["destinationUrl"], file_path, s3_info["presignedPost"]
        )
        created_record_vo = self.register_record(record_vo, s3_info["destinationUrl"])

        attempts, processed_record = self._measure_post_upload_processing(
            created_record_vo, timeout
        )
        result = [
            filename,
            processed_record["type"].split(".")[-1],
            processed_record["status"].split(".")[-1],
            ",".join([vo["type"].split(".")[-1] for vo in processed_record["FileVOs"]]),
            attempts,
        ]
        logging.info(result)
        return result

    def get_folder_info(self):
        logging.info("Get root folder")
        folder_request = PermanentRequest(self.base_url, "/api/folder/getRoot")
        folder = folder_request.response["FolderVO"]["ChildItemVOs"][1]
        return folder["folderId"], folder["FolderLinkVOs"][0]["folder_linkId"]

    def create_account(self, email, password):
        logging.info("Create account  %s : %s", email, password)
        body = [
            {
                "AccountVO": {
                    "primaryEmail": email,
                    "primaryPhone": None,
                    "fullName": "Functional Filetype Test",
                    "agreed": True,
                    "optIn": False,
                    "inviteCode": "",
                },
                "AccountPasswordVO": {
                    "password": password,
                    "passwordVerify": password,
                },
            }
        ]
        return PermanentRequest(self.base_url, "/api/account/post", data=body)

    def login(self, email, password):
        logging.info("Login as %s", email)
        body = [
            {
                "AccountVO": {
                    "primaryEmail": email,
                    "rememberMe": False,
                    "keepLoggedIn": False,
                },
                "AccountPasswordVO": {"password": password},
            }
        ]
        return PermanentRequest(self.base_url, "/api/auth/login", data=body)

    def get_archive(self, archive_id, archive_nbr):
        logging.info("Get archive")
        body = [{"ArchiveVO": {"archiveNbr": archive_nbr, "archiveId": archive_id}}]
        return PermanentRequest(self.base_url, "/api/archive/get", data=body)

    def get_account(self, account_id):
        logging.info("Get account")
        body = [{"accountId": account_id}]
        return PermanentRequest(self.base_url, "/api/account/get", data=body)

    def logged_in(self):
        return PermanentRequest(self.base_url, "/api/auth/loggedIn")

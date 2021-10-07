import logging
import requests


def upload_to_s3(file_path, presigned_post):
    logging.info("Upload file %s", file_path)

    fields = presigned_post["fields"]
    fields["Content-Type"] = "application/octet-stream"
    logging.debug("Upload form data: %s", fields)

    with open(file_path, "rb") as f:
        r = requests.post(presigned_post["url"], data=fields, files={"file": f})
        r.raise_for_status()


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

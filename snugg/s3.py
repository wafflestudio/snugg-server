import logging

import boto3
from botocore.exceptions import ClientError

from snugg.settings import AWS_STORAGE_BUCKET_NAME, MEDIA_ROOT


def create_presigned_url(
    client_method_name, method_parameters=None, expiration=3600, http_method=None
):
    """Generate a presigned URL to invoke an S3.Client method

    Not all the client methods provided in the AWS Python SDK are supported.

    :param client_method_name: Name of the S3.Client method, e.g., 'list_buckets'
    :param method_parameters: Dictionary of parameters to send to the method
    :param expiration: Time in seconds for the presigned URL to remain valid
    :param http_method: HTTP method to use (GET, etc.)
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 client method
    s3_client = boto3.client("s3")
    try:
        response = s3_client.generate_presigned_url(
            ClientMethod=client_method_name,
            Params=method_parameters
            if "Bucket" in method_parameters
            else {"Bucket": AWS_STORAGE_BUCKET_NAME, **method_parameters},
            ExpiresIn=expiration,
            HttpMethod=http_method,
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def create_presigned_get(key, expiration=3600):
    key = "/".join((MEDIA_ROOT, key))
    return create_presigned_url(
        "get_object",
        method_parameters={"Bucket": AWS_STORAGE_BUCKET_NAME, "Key": key},
        expiration=expiration,
    )


def create_presigned_post(key, fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param key: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client("s3")
    key = "/".join((MEDIA_ROOT, key))
    try:
        response = s3_client.generate_presigned_post(
            AWS_STORAGE_BUCKET_NAME,
            key,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response


# def create_presigned_post_folder(folder_name, fields=None, conditions=None, expiration=3600):
#     s3_client = boto3.client('s3')
#     if not folder_name.endswith('/'):
#         folder_name = folder_name + '/'
#     if not conditions:
#         conditions = [["starts-with", "$key", folder_name]]
#     try:
#         response = s3_client.generate_presigned_post(AWS_STORAGE_BUCKET_NAME,
#                                                      folder_name+'${filename}',
#                                                      Fields=fields,
#                                                      Conditions=conditions,
#                                                      ExpiresIn=expiration)
#     except ClientError as e:
#         logging.error(e)
#         return None
#
#     # The response contains the presigned URL and required fields
#     return response


def delete_object(key=None, prefix=None):
    print(1, prefix)
    print(2, key)
    if prefix is None:
        if key is None:
            raise ValueError("At least one argument should be provided")
        key = "/".join((MEDIA_ROOT, key))
        s3 = boto3.client("s3")

        if isinstance(key, str):
            try:
                response = s3.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=key)
            except ClientError as e:
                logging.error(e)
                return None

        elif isinstance(key, (list, tuple)):
            try:
                response = s3.delete_objects(
                    Bucket=AWS_STORAGE_BUCKET_NAME,
                    Delete={"Objects": [{"Key": o} for o in key]},
                )
            except ClientError as e:
                logging.error(e)
                return None

        else:
            raise TypeError("object_key should be string or list type")
    else:
        prefix = "/".join((MEDIA_ROOT, prefix))
        print(prefix)
        if not prefix.endswith("/"):
            raise ValueError('prefix should end with "/"')

        s3 = boto3.resource("s3")
        bucket = s3.Bucket(AWS_STORAGE_BUCKET_NAME)
        response = bucket.objects.filter(Prefix=prefix).delete()

    return response

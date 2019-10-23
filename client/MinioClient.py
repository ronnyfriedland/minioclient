from config.Configuration import Configuration
from minio import Minio, ResponseError
import urllib3
import sys
import tempfile


class MinioClient:

    def __init__(self, url, access_key, secret_key):
        http_client = urllib3.PoolManager(cert_reqs='NONE')

        self.configuration = Configuration()

        self.minio_client = Minio(url,
                                  access_key=access_key,
                                  secret_key=secret_key,
                                  secure=self.configuration.read_config("minio", "ssl") == 'True',
                                  http_client=http_client)

        if self.configuration.read_config("minio", "debug") == 'True':
            self.minio_client.trace_on(sys.stderr)

    def list_buckets(self):
        try:
            return self.minio_client.list_buckets()
        except ResponseError:
            return None

    def list_objects(self, bucket_name, directory):
        try:
            return self.minio_client.list_objects(bucket_name, prefix=directory, recursive=False)
        except ResponseError:
            return None

    def get_object(self, bucket_name, object_name, target_name):
        self.minio_client.fget_object(bucket_name, object_name, target_name)

    def delete_object(self, bucket_name, object_name):
        self.minio_client.remove_object(bucket_name, object_name)
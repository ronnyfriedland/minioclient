from config.Configuration import Configuration
from minio import Minio, ResponseError
import urllib3
import sys
import threading



class MinioClient:

    """
    Author: Ronny Friedland

    Provides methods to access S3 storage. Hides implementation details of used framework
    """

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
        """
        List buckets
        :return: all available buckets
        """
        try:
            return self.minio_client.list_buckets()
        except ResponseError:
            return None

    def list_objects(self, bucket_name, directory):
        """
        List objects
        :param bucket_name: the bucket
        :param directory: the (optional) directory
        :return: all available objects
        """
        try:
            return self.minio_client.list_objects(bucket_name, prefix=directory, recursive=False)
        except ResponseError:
            return None

    def get_object(self, bucket_name, object_name, target_name):
        """
        Returns the object
        :param bucket_name: the bucket
        :param object_name: the (unique) name of the object
        :param target_name: the name of the file to store the content to
        """
        t = threading.Thread(target=self.minio_client.fget_object, args=(bucket_name, object_name, target_name))
        t.start()

    def put_object(self, bucket_name, object_name, file_name):
        """
        Saves data to storage
        :param bucket_name: the bucket
        :param object_name: the object name
        :param file_name: the file to store
        """
        t = threading.Thread(target=self.minio_client.fput_object, args=(bucket_name, object_name, file_name))
        t.start()

    def delete_object(self, bucket_name, object_name):
        """
        Deletes an object
        :param bucket_name: the bucket
        :param object_name: the object name
        """
        self.minio_client.remove_object(bucket_name, object_name)
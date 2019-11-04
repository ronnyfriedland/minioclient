import unittest as ut

from minio import Minio, ResponseError
from client.MinioClient import MinioClient
from unittest.mock import patch, MagicMock, PropertyMock


class TestMinioClient(ut.TestCase):

    @patch.object(Minio, 'list_buckets', MagicMock(side_effect=ResponseError(PropertyMock(data= ""), "foo")))
    def test_list_buckets_error(self):
        result = MinioClient(url="localhost:9000", access_key="foo", secret_key="bar").list_buckets()
        assert None == result

    @patch.object(Minio, 'list_buckets', MagicMock(return_value={}))
    def test_list_buckets(self):
        result = MinioClient(url="localhost:9000", access_key="foo", secret_key="bar").list_buckets()
        assert {} == result


if __name__ == '__main__':
    ut.main()
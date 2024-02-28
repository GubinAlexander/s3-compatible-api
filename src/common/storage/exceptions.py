class StorageException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class AzureStorageException(StorageException):
    pass


class GcStorageException(StorageException):
    pass


class S3StorageException(StorageException):
    pass


class FsStorageException(StorageException):
    pass


class HttpStorageException(StorageException):
    pass

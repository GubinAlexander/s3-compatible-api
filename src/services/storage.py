import os
from src.common.storage import StorageRepository

STORAGE_ROOT_DIR = "fs:///Users/alexander/Desktop/"
ROOT_DIR = "/Users/alexander/Desktop/"


class StorageService:
    def __init__(self, storage_repo: StorageRepository):
        self.storage_repo = storage_repo

    def list_objects(self, bucket_name: str):
        return self.storage_repo.list_objects(f"{STORAGE_ROOT_DIR}/{bucket_name}/files")

    def list_buckets(self) -> list:
        result = []
        files = self.storage_repo.list_objects(f"{STORAGE_ROOT_DIR}/buckets")
        for file in files:
            if os.path.isdir(f"{file.local_path}/{file.key}") and not file.key.startswith("$"):
                result.append(file)
        return result

    def upload_file(self, bucket_name: str, file_name: str, data: bytes):
        with open(f"{ROOT_DIR}/{bucket_name}/{file_name}", "wb") as file:
            file.write(data)

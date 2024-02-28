"""Definition of File system storage Repository."""
import json
import os
import shutil
from itertools import groupby
from typing import Union, Optional, Dict, List

from src.common.storage import StorageRepository
from src.common.storage.exceptions import FsStorageException
from src.common.storage.models import StoragePath, StorageObject, StorageType

SERVICE = "FS"


class FsStorageRepository(StorageRepository):
    def create_folder(self, name: str):
        if not self.folder_exists(name):
            os.makedirs(name)

    def folder_exists(self, name: str):
        return os.path.exists(name)

    def put_object(
        self,
        path: Union[StoragePath, str],
        data: bytes,
        content_type: str = "",
        metadata: Optional[Dict[str, str]] = None,
    ):
        if isinstance(path, str):
            path = StoragePath.parse(path)
        if metadata is None:
            metadata = {}

        try:
            file_path = os.path.join(path.local_path, path.key)
            self.create_folder(os.path.dirname(file_path))
            with open(file_path, "wb") as file:
                file.write(data)
            try:
                os.setxattr(  # type: ignore # pylint: disable=no-member
                    file_path, "user.metadata", json.dumps(metadata).encode("utf-8")
                )
                os.setxattr(  # type: ignore # pylint: disable=no-member
                    file_path, "user.content_type", content_type.encode("utf-8")
                )
            except:
                pass

        except Exception as e:
            raise FsStorageException(f"FS cannot put object. Key {path.key}. | {e}")

    def delete_object(self, path: Union[StoragePath, str]) -> None:
        if isinstance(path, str):
            path = StoragePath.parse(path)

        try:
            file_path = os.path.join(path.local_path, path.key)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            raise FsStorageException(f"Cannot delete object {path}. | {e}")

    def delete_objects(self, paths: List[Union[StoragePath, str]]):
        storage_paths = list(
            map(lambda x: StoragePath.parse(x) if isinstance(x, str) else x, paths)
        )
        storage_paths.sort(key=lambda x: x.local_path)
        grouped_paths = groupby(storage_paths, key=lambda x: x.local_path)

        for folder_group in grouped_paths:
            temp_paths = list(folder_group[1])
            try:
                for path in temp_paths:
                    file_path = os.path.join(path.local_path, path.key)
                    if os.path.exists(file_path):
                        os.remove(file_path)
            except Exception as e:
                raise FsStorageException(f"Cannot delete object {paths}. | {e}")

    def get_object(self, path: Union[StoragePath, str]) -> StorageObject:
        if isinstance(path, str):
            path = StoragePath.parse(path)
        try:
            file_name = os.path.join(path.local_path, path.key)
            with open(file_name, "rb") as file:
                data = file.read()
            return StorageObject(data=data)
        except Exception as e:
            raise FsStorageException(f"Cannot get object {path}. | {e}")

    def object_exists(self, path: Union[StoragePath, str]) -> bool:
        if isinstance(path, str):
            path = StoragePath.parse(path)
        return os.path.exists(os.path.join(path.local_path, path.key))

    def upload_file(self, local_path: str, path: Union[StoragePath, str]):
        if isinstance(path, str):
            path = StoragePath.parse(path)

        try:
            dst_path = os.path.join(path.local_path, path.key)
            self.create_folder(os.path.dirname(dst_path))
            shutil.copy2(local_path, dst_path)
        except Exception as e:
            raise FsStorageException(f"FS cannot upload file. Key {path.key}. | {e}")

    def download_file(self, local_path: str, path: Union[StoragePath, str]):
        if isinstance(path, str):
            path = StoragePath.parse(path)

        try:
            dst_path = os.path.join(path.local_path, path.key)
            shutil.copy2(local_path, dst_path)
        except Exception as e:
            raise FsStorageException(f"FS cannot download file. Key {path.key}. | {e}")

    def ensure_access(self, name: str) -> bool:
        self.create_folder(name)
        return self.ensure_available(name)

    def list_objects(self, path: Union[StoragePath, str]) -> List[StoragePath]:
        if isinstance(path, str):
            path = StoragePath.parse(path)

        return [
            StoragePath(
                key=file, storage_type=StorageType.FS, local_path=path.local_path
            )
            for file in os.listdir(path.local_path)
        ]

    def delete_path(self, path: Union[StoragePath, str]):
        if isinstance(path, str):
            path = StoragePath.parse(path)

        if os.path.exists(os.path.join(path.local_path, path.key)):
            shutil.rmtree(os.path.join(path.local_path, path.key))

        if os.path.exists(path.local_path) and not os.listdir(path.local_path):
            os.rmdir(path.local_path)

import uuid
from abc import ABC, abstractmethod
from typing import List, Union, Optional, Dict

from src.common.storage.models import StoragePath, StorageObject


class StorageRepository(ABC):
    @abstractmethod
    def put_object(
        self,
        path: Union[StoragePath, str],
        data: bytes,
        content_type: str = "",
        metadata: Optional[Dict[str, str]] = None,
    ) -> None:
        pass

    @abstractmethod
    def delete_object(self, path: Union[StoragePath, str]) -> None:
        pass

    @abstractmethod
    def delete_objects(self, paths: List[Union[StoragePath, str]]):
        pass

    @abstractmethod
    def get_object(self, path: Union[StoragePath, str]) -> StorageObject:
        pass

    @abstractmethod
    def object_exists(self, path: Union[StoragePath, str]) -> bool:
        pass

    @abstractmethod
    def ensure_access(self, name: str):
        pass

    @abstractmethod
    def upload_file(self, local_path: str, path: Union[StoragePath, str]):
        pass

    @abstractmethod
    def download_file(self, local_path: str, path: Union[StoragePath, str]):
        pass

    def ensure_available(self, name: str):
        path = StoragePath(
            bucket_name=name,
            container_name=name,
            local_path=name,
            key=f"tmp/{uuid.uuid4()}.txt",
        )
        self.put_object(path, data=b"test")
        self.get_object(path)
        self.delete_object(path)
        return True

    @abstractmethod
    def list_objects(self, path: Union[StoragePath, str]) -> List[StoragePath]:
        pass

    def delete_path(self, path: Union[StoragePath, str]):
        paths = self.list_objects(path)
        self.delete_objects(paths)  # type: ignore

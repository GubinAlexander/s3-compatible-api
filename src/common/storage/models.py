from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Dict


class StorageType(Enum):
    S3 = "s3"
    GCS = "gcs"
    FS = "fs"
    AZ = "az"
    HTTP = "http"


class StoragePath:
    storage_separators = {
        StorageType.S3.value: "s3",
        StorageType.GCS.value: "gs",
        StorageType.FS.value: "fs",
        StorageType.AZ.value: "az",
        StorageType.HTTP.value: "http",
    }

    def __init__(
        self,
        bucket_name: str = "",
        container_name: str = "",
        key: str = "",
        local_path: str = "",
        storage_account: str = "",
        storage_type: StorageType = None,
        prefix: Optional[str] = "",
    ):
        self.bucket_name = bucket_name
        self.container_name = container_name
        self.local_path = local_path
        self.storage_type = storage_type
        self.storage_account = storage_account
        prefix = prefix[1:] if prefix.startswith("/") else prefix  # type: ignore
        self.key = (
            os.path.join(prefix, key)
            if prefix and storage_type != StorageType.FS
            else key
        )
        self.key = (
            self.key.replace("\\", "/")
            if storage_type != StorageType.FS
            else self.key.lstrip("/")
        )
        if os.name == "nt" and storage_type == StorageType.FS:
            self.key = self.key.replace("/", "\\")

    @staticmethod
    def parse(link: str) -> StoragePath:
        link = (
            link.replace("\\", "/")
            if not link.startswith(StoragePath.storage_separators[StorageType.FS.value])
            else link
        )
        if link.startswith(StoragePath.storage_separators[StorageType.S3.value]):
            link_items = link.split("://")[1].replace("//", "/").split("/", 1)
            return StoragePath(
                bucket_name=link_items[0],
                key=link_items[1],
                storage_type=StorageType.S3,
            )
        elif link.startswith(StoragePath.storage_separators[StorageType.GCS.value]):
            link_items = link.split("://")[1].replace("//", "/").split("/", 1)
            return StoragePath(
                bucket_name=link_items[0],
                key=link_items[1],
                storage_type=StorageType.GCS,
            )
        elif link.startswith(StoragePath.storage_separators[StorageType.FS.value]):
            link = link.split("://")[1].replace("//", "/")
            local_path = Path(link)
            return StoragePath(
                local_path=str(local_path.parent),
                key=os.path.basename(local_path.name).lstrip("/"),
                storage_type=StorageType.FS,
            )
        elif link.startswith(StoragePath.storage_separators[StorageType.AZ.value]):
            link_items = link.replace(f"{StorageType.AZ.value}:", "").split("://")
            path_items = link_items[1].replace("//", "/").split("/", 1)
            return StoragePath(
                storage_account=link_items[0],
                container_name=path_items[0],
                key=path_items[1],
                storage_type=StorageType.AZ,
            )
        elif link.startswith(StoragePath.storage_separators[StorageType.HTTP.value]):
            return StoragePath(key=link, storage_type=StorageType.HTTP)
        raise ValueError(f"Invalid link format: {link}")

    def __str__(self) -> str:
        if self.storage_type == StorageType.AZ:
            return (
                f"{StoragePath.storage_separators[self.storage_type.value]}:"
                f"{self.storage_account}://{self.container_name}/{self.key}"
            )
        elif self.storage_type == StorageType.HTTP:
            return self.key
        elif self.storage_type == StorageType.FS:
            return "".join(
                [
                    f"{StoragePath.storage_separators[self.storage_type.value]}://",
                    os.path.join(self.local_path, self.key),
                ]
            )
        return (
            f"{StoragePath.storage_separators[self.storage_type.value]}://"  # type: ignore
            f"{self.bucket_name or self.local_path}/{self.key}"
        )


@dataclass(frozen=True)
class StorageObject:
    data: bytes
    content_type: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None
    path: Optional[StoragePath] = None

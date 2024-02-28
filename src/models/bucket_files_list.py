from pydantic_xml import BaseXmlModel, element
import datetime as dt
from typing import List


BUCKET_FILES = {
    "bucket_1": ["file1.jpg", "file2.jpg"],
    "bucket_2": ["file3.jpg", "file4.jpg", "file5.jpg"],
    "bucket_3": ["file6.jpg", "file7.jpg"]
}


class ContentOwner(BaseXmlModel, tag="Owner"):
    idf: str = element(tag="ID")
    display_name: str = element(tag="DisplayName")


class RestoreStatus(BaseXmlModel, tag="RestoreStatus"):
    is_restore_in_progress: bool = element(tag="IsRestoreInProgress")
    restore_expiry_date: dt.datetime = element(tag="RestoreExpiryDate")


class Contents(BaseXmlModel, tag="Contents"):
    checksum_algorithm: str = element(tag="ChecksumAlgorithm", default=None)
    e_tag: str = element(tag="ETag")
    key: str = element(tag="Key")
    last_modified: dt.datetime = element(tag="LastModified")
    owner: ContentOwner
    restore_status: RestoreStatus
    size: int = element(tag="Size")
    storage_class: str = element(tag="StorageClass")


class CommonPrefixes(BaseXmlModel, tag="CommonPrefixes"):
    prefix: str = element(tag="Prefix")


class ListBucketResult(BaseXmlModel):
    is_truncated: bool = element(tag="IsTruncated")
    contents: List[Contents] = element(tag="Contents")
    name: str = element(tag="Name")
    prefix: str = element(tag="Prefix")
    delimiter: str = element(tag="Delimiter")
    max_keys: int = element(tag="MaxKeys")
    common_prefixes: CommonPrefixes = element(default=None)
    encoding_type: str = element(tag="EncodingType")
    key_count: int = element(tag="KeyCount")
    continuation_token: str = element(tag="ContinuationToken")
    next_continuation_token: str = element(tag="NextContinuationToken")
    start_after: str = element(tag="StartAfter")

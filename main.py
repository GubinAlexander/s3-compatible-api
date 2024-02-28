import datetime
from src.decorators import log_request
from src.common.storage.fs import FsStorageRepository
from src.models.bucket_list import ListAllMyBucketsResult, Buckets, Owner, Bucket
from src.models.bucket_files_list import ListBucketResult, Contents, ContentOwner, RestoreStatus
from fastapi import FastAPI, Response, Request
from src.services.storage import StorageService, ROOT_DIR
from fastapi import Body
from fastapi.responses import FileResponse
app = FastAPI()


fs_storage_service = StorageService(FsStorageRepository())


@app.get("/")
@log_request
def bucket_list(request: Request):
    buckets = []
    for bucket in fs_storage_service.list_buckets():
        buckets.append(Bucket(creation_date=datetime.datetime.now().timestamp(), name=bucket.key))
    return Response(
        content=ListAllMyBucketsResult(
            buckets=Buckets(bucket=buckets),
            owner=Owner(display_name="Alex", idf="uuid")
        ).to_xml(),
        media_type="application/xml"
    )


@app.get("/{bucket_name}")
@log_request
def bucket_files_list(bucket_name: str, request: Request, list_type: int = 2, continuation_token: str = "", delimiter: str = "", encoding_type: str = "", fetch_owner: bool = False, max_keys: int = 1000000, prefix: str = "", start_after: str = ""):
    files = fs_storage_service.list_objects(bucket_name)
    ct = []
    for file in files:
        ct.append(Contents(
            key=file.key,
            last_modified=datetime.datetime.now().timestamp(),
            e_tag="uuid",
            size=323323,
            ass="STANDART",
            owner=ContentOwner(display_name="Alex", idf="uuid"),
            storage_class="qe",
            restore_status=RestoreStatus(
                is_restore_in_progress=False, restore_expiry_date=datetime.datetime.now().timestamp()
            ),
        ))
    return Response(
        content=ListBucketResult(
            continuation_token=continuation_token,
            delimiter=delimiter,
            encoding_type=encoding_type,
            max_keys=max_keys,
            prefix=prefix,
            start_after=start_after,
            contents=ct,
            key_count=260,
            next_continuation_token="",
            name="name",
            is_truncated=False,
        ).to_xml(),
        media_type="application/xml"
    )


@app.put("/{bucket_name}/{image_name}")
@log_request
def upload_file(bucket_name: str, image_name: str, request: Request, payload: bytes = Body(...)):
    fs_storage_service.upload_file(bucket_name, image_name, payload)
    return Response(status_code=200)


@app.get("/{bucket}/{key}")
@log_request
def download_file(bucket: str, key: str, request: Request):
    return FileResponse(f"{ROOT_DIR}/{bucket}/{key}")

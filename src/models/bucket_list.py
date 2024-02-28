from pydantic_xml import BaseXmlModel, element
import datetime as dt
from typing import List


BUCKET_NAMES = ["Desktop", "bucket_2", "bucket_3"]


class Bucket(BaseXmlModel):
    name: str = element(tag="Name")
    creation_date: dt.datetime = element(tag="CreationDate")


class Buckets(BaseXmlModel, tag='Buckets'):
    bucket: List[Bucket] = element(tag="Bucket")


class Owner(BaseXmlModel, tag="Owner"):
    idf: str = element(tag="ID")
    display_name: str = element(tag="DisplayName")


class ListAllMyBucketsResult(BaseXmlModel):
    owner: Owner
    buckets: Buckets

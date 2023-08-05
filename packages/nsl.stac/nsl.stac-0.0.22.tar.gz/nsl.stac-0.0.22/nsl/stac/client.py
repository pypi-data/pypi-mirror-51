import os

# https://stackoverflow.com/a/16151611/445372
import datetime

from typing import Iterator

from google.protobuf import timestamp_pb2, duration_pb2
from epl.protobuf import stac_pb2

from nsl.stac import stac_service


def insert_one(stac_item: stac_pb2.StacItem) -> stac_pb2.StacDbResponse:
    """
    Insert on item into the service
    :param stac_item: item to insert
    :return: StacDbResponse, the response of the success of the insert
    """
    auth = os.getenv('AUTH')
    bearer = os.getenv('BEARER')
    return stac_service.stub.InsertOne(stac_item, metadata=(
        ('authorization', auth),
        ('bearer', bearer),
    ))


def search_one(stac_request: stac_pb2.StacRequest) -> stac_pb2.StacItem:
    """
    search for one item from the db that matches the stac request
    :param stac_request: StacRequest of query parameters to filter by
    :return: StacItem
    """
    auth = os.getenv('AUTH')
    bearer = os.getenv('BEARER')
    return stac_service.stub.SearchOne(stac_request, metadata=(
        ('authorization', auth),
        ('bearer', bearer),
    ))


def count(stac_request: stac_pb2.StacRequest) -> int:
    """
    count all the items in the database that match the stac request
    :param stac_request: StacRequest query parameters to apply to count method (limit ignored)
    :return: int
    """
    auth = os.getenv('AUTH')
    bearer = os.getenv('BEARER')
    db_result = stac_service.stub.Count(stac_request, metadata=(
        ('authorization', auth),
        ('bearer', bearer),
    ))
    return db_result.count


def search(stac_request: stac_pb2.StacRequest) -> Iterator[stac_pb2.StacItem]:
    """
    search for stac items by using StacRequest. return a stream of StacItems
    :param stac_request: StacRequest of query parameters to filter by
    :return: stream of StacItems
    """
    auth = os.getenv('AUTH')
    bearer = os.getenv('BEARER')
    results_generator = stac_service.stub.Search(stac_request, metadata=(
        ('authorization', auth),
        ('bearer', bearer),
    ))
    return results_generator


def timezoned(d_utc: datetime.datetime or datetime.date):
    # datetime is child to datetime.date, so if we reverse the order of this instance of we fail
    if isinstance(d_utc, datetime.datetime) and d_utc.tzinfo is None:
        # TODO add warning here:
        print("warning, no timezone provided with datetime, so UTC is assumed")
        d_utc = datetime.datetime(d_utc.year,
                                  d_utc.month,
                                  d_utc.day,
                                  d_utc.hour,
                                  d_utc.minute,
                                  d_utc.second,
                                  d_utc.microsecond,
                                  tzinfo=datetime.timezone.utc)
    elif not isinstance(d_utc, datetime.datetime):
        print("warning, no timezone provided with date, so UTC is assumed")
        d_utc = datetime.datetime.combine(d_utc, datetime.datetime.min.time(), tzinfo=datetime.timezone.utc)
    return d_utc


def timestamp(d_utc: datetime.datetime or datetime.date) -> timestamp_pb2.Timestamp:
    ts = timestamp_pb2.Timestamp()
    ts.FromDatetime(timezoned(d_utc))
    return ts


def duration(d_start: datetime.date or datetime.datetime, d_end: datetime.date or datetime.datetime):
    d = duration_pb2.Duration()
    d.FromTimedelta(timezoned(d_end) - timezoned(d_start))
    return d

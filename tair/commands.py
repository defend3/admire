from typing import Union

from redis import Redis
from redis.asyncio import Redis as AsyncRedis
from redis.client import bool_ok

from tair.tairbloom import TairBloomCommands
from tair.taircpc import CpcUpdate2judResult, TairCpcCommands
from tair.tairdoc import TairDocCommands
from tair.tairgis import TairGisCommands
from tair.tairhash import (
    TairHashCommands,
    parse_exhgetall,
    parse_exhgetwithver,
    parse_exhincrbyfloat,
    parse_exhmgetwithver,
    parse_exhscan,
)
from tair.tairroaring import TairRoaringCommands, parse_tr_scan
from tair.tairsearch import ScandocidResult, TairSearchCommands
from tair.tairstring import (
    TairStringCommands,
    parse_excas,
    parse_exget,
    parse_exincrbyfloat,
    parse_exset,
)
from tair.tairts import TairTsCommands
from tair.tairvector import (
    TairVectorCommands,
    parse_tvs_get_index_result,
    parse_tvs_get_result,
    parse_tvs_hincrbyfloat_result,
    parse_tvs_hmget_result,
    parse_tvs_msearch_result,
    parse_tvs_search_result,
)
from tair.tairzset import TairZsetCommands, parse_tair_zset_items


class TairCommands(
    TairHashCommands,
    TairStringCommands,
    TairZsetCommands,
    TairBloomCommands,
    TairRoaringCommands,
    TairSearchCommands,
    TairGisCommands,
    TairDocCommands,
    TairTsCommands,
    TairCpcCommands,
    TairVectorCommands,
):
    pass


def str_if_bytes(value: Union[str, bytes]) -> str:
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value


def bool_ok(resp) -> bool:
    return str_if_bytes(resp) == "OK"


def int_or_none(response):
    return None if response is None else int(response)


TAIR_RESPONSE_CALLBACKS = {
    # TairString
    "EXSET": parse_exset,
    "EXGET": parse_exget,
    "EXINCRBYFLOAT": parse_exincrbyfloat,
    "EXCAS": parse_excas,
    # TairHash
    "EXHMSET": bool_ok,
    "EXHINCRBYFLOAT": parse_exhincrbyfloat,
    "EXHGETWITHVER": parse_exhgetwithver,
    "EXHMGETWITHVER": parse_exhmgetwithver,
    "EXHGETALL": parse_exhgetall,
    "EXHSCAN": parse_exhscan,
    # TairZset
    "EXZINCRBY": str_if_bytes,
    "EXZSCORE": str_if_bytes,
    "EXZRANGE": parse_tair_zset_items,
    "EXZREVRANGE": parse_tair_zset_items,
    "EXZRANGEBYSCORE": parse_tair_zset_items,
    "EXZREVRANGEBYSCORE": parse_tair_zset_items,
    # TairBloom
    "BF.RESERVE": bool_ok,
    # TairRoaring
    "TR.GETBIT": lambda resp: resp if resp == 1 else 0,
    "TR.APPENDINTARRAY": bool_ok,
    "TR.SETINTARRAY": bool_ok,
    "TR.SETBITARRAY": bool_ok,
    "TR.OPTIMIZE": bool_ok,
    "TR.SCAN": parse_tr_scan,
    "TR.RANGEBITARRAY": lambda resp: resp.decode(),
    "TR.JACCARD": lambda resp: float(resp.decode()),
    # TairSearch
    "TFT.CREATEINDEX": bool_ok,
    "TFT.UPDATEINDEX": bool_ok,
    "TFT.GETINDEX": lambda resp: None if resp is None else resp.decode(),
    "TFT.ADDDOC": lambda resp: resp.decode(),
    "TFT.MADDDOC": bool_ok,
    "TFT.DELDOC": lambda resp: int(resp.decode()),
    "TFT.UPDATEDOCFIELD": bool_ok,
    "TFT.INCRFLOATDOCFIELD": lambda resp: float(resp.decode()),
    "TFT.GETDOC": lambda resp: None if resp is None else resp.decode(),
    "TFT.SCANDOCID": lambda resp: ScandocidResult(resp[0].decode(), [i.decode() for i in resp[1]]),
    "TFT.DELALL": bool_ok,
    "TFT.SEARCH": lambda resp: resp.decode(),
    "TFT.GETSUG": lambda resp: [i.decode() for i in resp],
    "TFT.GETALLSUGS": lambda resp: [i.decode() for i in resp],
    # TairDoc
    "JSON.SET": lambda resp: None if resp is None else resp == b"OK",
    "JSON.TYPE": str_if_bytes,
    # TairTs
    "EXTS.P.CREATE": bool_ok,
    "EXTS.S.CREATE": bool_ok,
    "EXTS.S.ALTER": bool_ok,
    "EXTS.S.ADD": bool_ok,
    "EXTS.S.MADD": lambda resp: [bool_ok(i) for i in resp],
    "EXTS.S.INCRBY": bool_ok,
    "EXTS.S.MINCRBY": lambda resp: [bool_ok(i) for i in resp],
    "EXTS.S.DEL": bool_ok,
    "EXTS.S.RAW_MODIFY": bool_ok,
    "EXTS.S.RAW_MMODIFY": lambda resp: [bool_ok(i) for i in resp],
    "EXTS.S.RAW_INCRBY": bool_ok,
    "EXTS.S.RAW_MINCRBY": lambda resp: [bool_ok(i) for i in resp],
    # TairCpc
    "CPC.UPDATE": bool_ok,
    "CPC.ESTIMATE": lambda resp: float(resp.decode()),
    "CPC.UPDATE2EST": lambda resp: float(resp.decode()),
    "CPC.UPDATE2JUD": lambda resp: CpcUpdate2judResult(float(resp[0].decode()), float(resp[1].decode())),
    "CPC.ARRAY.UPDATE": bool_ok,
    "CPC.ARRAY.ESTIMATE": lambda resp: float(resp.decode()),
    "CPC.ARRAY.ESTIMATE.RANGE": lambda resp: [float(i.decode()) for i in resp],
    "CPC.ARRAY.ESTIMATE.RANGE.MERGE": lambda resp: float(resp.decode()),
    "CPC.ARRAY.UPDATE2EST": lambda resp: float(resp.decode()),
    "CPC.ARRAY.UPDATE2JUD": lambda resp: CpcUpdate2judResult(float(resp[0].decode()), float(resp[1].decode())),
    # TairVector
    "TVS.CREATEINDEX": bool_ok,
    "TVS.GETINDEX": parse_tvs_get_index_result,
    "TVS.DELINDEX": int_or_none,
    "TVS.HSET": int_or_none,
    "TVS.DEL": int_or_none,
    "TVS.HDEL": int_or_none,
    "TVS.HGETALL": parse_tvs_get_result,
    "TVS.HMGET": parse_tvs_hmget_result,
    "TVS.KNNSEARCH": parse_tvs_search_result,
    "TVS.MKNNSEARCH": parse_tvs_msearch_result,
    "TVS.MINDEXKNNSEARCH": parse_tvs_search_result,
    "TVS.MINDEXMKNNSEARCH": parse_tvs_msearch_result,
    "TVS.HINCRBY": int_or_none,
    "TVS.HINCRBYFLOAT": parse_tvs_hincrbyfloat_result,
}


def set_tair_response_callback(redis: Union[Redis, AsyncRedis]):
    for cmd, cb in TAIR_RESPONSE_CALLBACKS.items():
        redis.set_response_callback(cmd, cb)

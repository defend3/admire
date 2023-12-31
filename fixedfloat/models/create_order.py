# generated by datamodel-codegen:
#   timestamp: 2023-02-18T19:48:56+00:00

from __future__ import annotations

from typing import Any, Optional

from melanie import BaseModel, Field


class Tx(BaseModel):
    id: Optional[Any]
    amount: Optional[Any]
    fee: Optional[Any]
    ccyfee: Optional[Any]
    time: Optional[bool]
    time_block: Optional[bool] = Field(None, alias="timeBlock")
    confirmations: Optional[Any]


class Emergency(BaseModel):
    status: Optional[list]
    choice: Optional[str]
    repeat: Optional[int]


class Back(BaseModel):
    currency: Optional[str]
    symbol: Optional[str]
    sub_symbol: Optional[str] = Field(None, alias="subSymbol")
    network: Optional[str]
    name: Optional[str]
    alias: Optional[str]
    qty: Optional[str]
    amount: Optional[str]
    address: Optional[str]
    extra: Optional[str]
    tx: Optional[Tx]


class Data(BaseModel):
    id: Optional[str]
    from_: Optional[Back] = Field(None, alias="from")
    to: Optional[Back]
    back: Optional[Back]
    emergency: Optional[Emergency]
    type: Optional[str]
    email: Optional[str]
    rate: Optional[float]
    rate_rev: Optional[float] = Field(None, alias="rateRev")
    status: Optional[int]
    reg: Optional[int]
    start: Optional[bool]
    finish: Optional[bool]
    update: Optional[int]
    expiration: Optional[int]
    left: Optional[int]
    step: Optional[str]
    token: Optional[str]


class FixedFloatCreateOrderResponse(BaseModel):
    code: Optional[int]
    msg: Optional[str]
    data: Optional[Data]

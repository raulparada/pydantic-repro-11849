from __future__ import annotations

from pydantic import BaseModel


class Foo(BaseModel):
    bar: list[Bar]


class Bar(BaseModel):
    baz: int

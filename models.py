from __future__ import annotations

from pydantic import BaseModel


class Foo(BaseModel):
    bar: Bar


class Bar(BaseModel):
    baz: str

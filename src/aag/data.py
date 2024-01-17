from __future__ import annotations

import datetime
from typing import Literal

from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str


class Group(BaseModel):
    id: str
    platform: str


class LineGroup(Group):
    platform = "line"
    chat_id: str


class DiscordGroup(Group):
    platform = "discord"
    guild_id: str
    channel_id: str


class ExpenseEntry(BaseModel):
    id: str
    group: Group
    time_added: datetime.datetime
    last_updated: datetime.datetime
    amount: float
    currency: str
    paid_by: User
    paid_for: dict[User, float]
    category: str | Literal  # TODO: list default categories.
    emoji: str
    description: str
    parent: ExpenseEntry | None

    @property
    def is_latest(self):
        return self.parent is not None

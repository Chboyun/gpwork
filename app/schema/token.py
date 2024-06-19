#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from app.schema.user import UserDetails
from common.schema import SchemaBase


class GetSwaggerToken(SchemaBase):
    access_token: str
    token_type: str = 'Bearer'
    user: UserDetails


class AccessTokenBase(SchemaBase):
    access_token: str
    access_token_type: str = 'Bearer'
    access_token_expire_time: datetime


class GetLoginToken(AccessTokenBase):
    refresh_token: str
    refresh_token_type: str = 'Bearer'
    refresh_token_expire_time: datetime
    user: UserDetails


class GetNewToken(AccessTokenBase):
    refresh_token: str
    refresh_token_type: str = 'Bearer'
    refresh_token_expire_time: datetime

# -*- coding: utf-8 -*-

import hashlib
import hmac
from datetime import datetime
from typing import List, Set

from .utils import uri_encode, uri_encode_except_slash

BCE_PREFIX: str = 'x-bce-'


def make_auth(
    ak: str, sk: str, method: str, path: str,
    params: dict, headers: dict
) -> str:
    canonical_uri: str = uri_encode_except_slash(path)
    canonical_query_string: str = _to_canonical_query_string(params)
    canonical_headers: str = _to_canonical_headers(headers)
    canonical_request: str = f'{method}\n{canonical_uri}\n{canonical_query_string}\n{canonical_headers}'  # noqa

    timestamp: str = _to_timestamp()

    auth_string_prefix: str = f'bce-auth-v1/{ak}/{timestamp}/1800'

    signing_key: str = hmac.new(
        sk.encode(),
        auth_string_prefix.encode(),
        hashlib.sha256).hexdigest()

    signature: str = hmac.new(
        signing_key.encode(),
        canonical_request.encode(),
        hashlib.sha256).hexdigest()

    return f'bce-auth-v1/{ak}/{timestamp}/1800//{signature}'


def _to_canonical_query_string(params: dict) -> str:
    param_list: List[str] = []
    for k, v in params.items():
        new_k: str = uri_encode(k)
        if v:
            new_v: str = uri_encode(str(v))
        else:
            new_v = ''
        param_list.append(f'{new_k}={new_v}')
    return '&'.join(sorted(param_list))


def _to_canonical_headers(
    headers: dict, headers_to_sign: Set[str] = None
) -> str:
    headers = headers or {}

    if headers_to_sign is None or len(headers_to_sign) == 0:
        headers_to_sign = {
            'host',
            'content-md5',
            'content-length',
            'content-type',
        }

    result: List[str] = []
    for k, v in headers.items():
        k_lower: str = k.strip().lower()

        if k_lower.startswith(BCE_PREFIX) or k_lower in headers_to_sign:
            new_k: str = uri_encode(k_lower)
            new_v: str = uri_encode(str(v).strip())
            result.append(f'{new_k}:{new_v}')

    return '\n'.join(sorted(result))


def _to_timestamp() -> str:
    t = datetime.utcnow().isoformat(timespec='seconds')
    return f'{t}Z'

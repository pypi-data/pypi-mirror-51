# -*- coding: utf-8 -*-

from datetime import datetime
from unittest.mock import Mock, patch

from bceauth.auth import make_auth


def test_make_auth():
    # 参考：https://cloud.baidu.com/doc/Reference/s/wjwvz1xt2
    # 这个用例和上述链接的示例，使用相同的输入，得到相同的输出

    with patch('bceauth.auth.datetime') as mocked:
        mocked.utcnow = Mock(return_value=datetime(2015, 4, 27, 8, 23, 49))

        actual = make_auth(
            ak='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            sk='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
            method='PUT',
            path='/v1/test/myfolder/readme.txt',
            params={
                'partNumber': 9,
                'uploadId': 'a44cc9bab11cbd156984767aad637851',
            },
            headers={
                'Host': 'bj.bcebos.com',
                'Date': 'Mon, 27 Apr 2015 16:23:49 +0800',
                'Content-Type': 'text/plain',
                'Content-Length': 8,
                'Content-Md5': 'NFzcPqhviddjRNnSOGo4rw==',
                'x-bce-date': '2015-04-27T08:23:49Z',
            }
        )

    expect = 'bce-auth-v1/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/2015-04-27T08:23:49Z/1800//d74a04362e6a848f5b39b15421cb449427f419c95a480fd6b8cf9fc783e2999e'  # noqa
    assert expect == actual

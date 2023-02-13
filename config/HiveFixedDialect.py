from pyhive.sqlalchemy_hive import HiveDialect as _HiveDialect


class _HiveFixedDialect(object):

    def create_connect_args(self, url):
        kwargs = {
            'host': url.host,
            'port': url.port,
            #'port': url.port or 10000,
            'username': url.username,
            'password': url.password,
            'database': url.database or 'default',
        }
        kwargs.update(url.query)
        return [], kwargs

_HiveDialect.create_connect_args = _HiveFixedDialect.create_connect_args
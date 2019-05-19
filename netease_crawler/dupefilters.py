# coding: utf-8
from redis import Redis
from scrapy.dupefilters import BaseDupeFilter
from hashlib import md5
from scrapy.utils.request import request_fingerprint
import logging


class RedisDupeFilter(BaseDupeFilter):
    """
    Redis 去重过滤器
    """
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = Redis(host=host, port=port, db=db)
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('REDIS_HOST', 'localhost')
        redis_port = settings.getint('REDIS_PORT')
        redis_db = settings.get('REDIS_DUP_DB')
        return cls(host, redis_port, redis_db)

    def request_seen(self, request):
        fp = request.url
        key = 'UrlFingerprints'
        if not self.redis.sismember(key, fp):
            self.redis.sadd(key, fp)
            return False
        return True

    def log(self, request, spider):
        msg = ("已过滤的重复请求: %(request)s")
        self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)



class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class RedisBloomDupeFilter(BaseDupeFilter):

    def __init__(self, host='localhost', port=6379, db=0, blockNum=1, key='bloomfilter'):
        self.redis = Redis(host=host, port=port, db=db)

        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        _port = settings.getint('REDIS_PORT', 6379)
        _host = settings.get('REDIS_HOST', '127.0.0.1')
        _db = settings.get('REDIS_DUP_DB', 0)
        key = settings.get('BLOOMFILTER_REDIS_KEY', 'bloomfilter')
        block_number = settings.getint(
            'BLOOMFILTER_BLOCK_NUMBER', 1)

        return cls(_host, _port, _db, blockNum=block_number, key=key)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        if self.exists(fp):
            return True

        self.insert(fp)
        return False

    def exists(self, str_input):
        if not str_input:
            return False
        m5 = md5()
        m5.update(str(str_input).encode('utf-8'))
        _input = m5.hexdigest()
        ret = True
        name = self.key + str(int(_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(_input)
            ret = ret & self.redis.getbit(name, loc)
        return ret

    def insert(self, str_input):
        m5 = md5()
        m5.update(str(str_input).encode('utf-8'))
        _input = m5.hexdigest()
        name = self.key + str(int(_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(_input)
            self.redis.setbit(name, loc, 1)

    def log(self, request, spider):
        msg = ("已过滤的重复请求: %(request)s")
        self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        spider.crawler.stats.inc_value(
            'redisbloomfilter/filtered', spider=spider)
import json
from typing import Any, Optional
from datetime import timedelta
import redis
from ..config import settings


class RedisCache:
    """
    Redis 缓存工具类
    用于存储对话历史、Session 等临时数据
    """

    def __init__(self):
        """
        初始化 Redis 连接
        """
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True,
            socket_connect_timeout=5
        )

    def set(self, key: str, value: Any, expire: Optional[timedelta] = None) -> bool:
        """
        设置缓存

        Args:
            key: 缓存键
            value: 缓存值（自动 JSON 序列化）
            expire: 过期时间

        Returns:
            是否成功
        """
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            if expire:
                self.redis_client.setex(key, int(expire.total_seconds()), value)
            else:
                self.redis_client.set(key, value)
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False

    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存

        Args:
            key: 缓存键

        Returns:
            缓存值（自动 JSON 反序列化），不存在返回 None
        """
        try:
            value = self.redis_client.get(key)
            if value:
                try:
                    return json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    return value
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None

    def delete(self, key: str) -> bool:
        """
        删除缓存

        Args:
            key: 缓存键

        Returns:
            是否成功
        """
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False

    def exists(self, key: str) -> bool:
        """
        检查缓存是否存在

        Args:
            key: 缓存键

        Returns:
            是否存在
        """
        try:
            return self.redis_client.exists(key) > 0
        except Exception as e:
            print(f"Redis exists error: {e}")
            return False

    def lpush(self, key: str, value: Any) -> bool:
        """
        列表左侧推送（用于对话历史）

        Args:
            key: 列表键
            value: 值

        Returns:
            是否成功
        """
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            self.redis_client.lpush(key, value)
            return True
        except Exception as e:
            print(f"Redis lpush error: {e}")
            return False

    def lrange(self, key: str, start: int = 0, end: int = -1) -> list:
        """
        获取列表范围

        Args:
            key: 列表键
            start: 起始索引
            end: 结束索引（-1 表示末尾）

        Returns:
            列表数据
        """
        try:
            values = self.redis_client.lrange(key, start, end)
            result = []
            for v in values:
                try:
                    result.append(json.loads(v))
                except (json.JSONDecodeError, TypeError):
                    result.append(v)
            return result
        except Exception as e:
            print(f"Redis lrange error: {e}")
            return []

    def ltrim(self, key: str, start: int = 0, end: int = -1) -> bool:
        """
        修剪列表（保留指定范围的元素）

        Args:
            key: 列表键
            start: 起始索引
            end: 结束索引

        Returns:
            是否成功
        """
        try:
            self.redis_client.ltrim(key, start, end)
            return True
        except Exception as e:
            print(f"Redis ltrim error: {e}")
            return False

    def expire(self, key: str, seconds: int) -> bool:
        """
        设置过期时间

        Args:
            key: 缓存键
            seconds: 过期秒数

        Returns:
            是否成功
        """
        try:
            self.redis_client.expire(key, seconds)
            return True
        except Exception as e:
            print(f"Redis expire error: {e}")
            return False


# 创建全局缓存实例
cache = RedisCache()

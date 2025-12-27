import json
import os
import asyncio

class RedisMock:
    def __init__(self, *args, **kwargs):
        self._db_file = 'redis_data.json'
        self._data = self._load_data()

    def _load_data(self):
        if os.path.exists(self._db_file):
            try:
                with open(self._db_file, 'r') as f:
                    raw_data = json.load(f)
                    for k, v in raw_data.items():
                        if isinstance(v, list):
                            raw_data[k] = set(v)
                    return raw_data
            except:
                return {}
        return {}

    def _save_data(self):
        save_copy = {}
        for k, v in self._data.items():
            if isinstance(v, set):
                save_copy[k] = list(v)
            else:
                save_copy[k] = v
        with open(self._db_file, 'w') as f:
            json.dump(save_copy, f)

    def get(self, key):
        val = self._data.get(str(key))
        if isinstance(val, (dict, set)):
            return None
        return val

    def set(self, key, value, *args, **kwargs):
        self._data[str(key)] = str(value)
        self._save_data()
        return True

    def delete(self, *args):
        for key in args:
            self._data.pop(str(key), None)
        self._save_data()
        return True

    def exists(self, key):
        return str(key) in self._data

    def ping(self):
        return True

    def hget(self, name, key):
        hash_data = self._data.get(str(name), {})
        if isinstance(hash_data, dict):
            return hash_data.get(str(key))
        return None

    def hset(self, name, key, value):
        name = str(name)
        if name not in self._data or not isinstance(self._data[name], dict):
            self._data[name] = {}
        self._data[name][str(key)] = str(value)
        self._save_data()
        return True

    def smembers(self, name):
        data = self._data.get(str(name))
        if isinstance(data, set):
            return data
        return set()

    def sadd(self, name, *values):
        name = str(name)
        if name not in self._data or not isinstance(self._data[name], set):
            self._data[name] = set()
        for v in values:
            self._data[name].add(str(v))
        self._save_data()
        return True

    def srem(self, name, *values):
        name = str(name)
        if name in self._data and isinstance(self._data[name], set):
            for v in values:
                self._data[name].discard(str(v))
        self._save_data()
        return True

    def keys(self, pattern):
        import fnmatch
        return [k for k in self._data.keys() if fnmatch.fnmatch(k, pattern)]

    def __getattr__(self, name):
        def mock_method(*args, **kwargs):
            return None
        return mock_method

class AsyncRedisMock(RedisMock):
    async def get(self, key): return super().get(key)
    async def set(self, key, value, *args, **kwargs): return super().set(key, value, *args, **kwargs)
    async def delete(self, *args): return super().delete(*args)
    async def hget(self, name, key): return super().hget(name, key)
    async def hset(self, name, key, value): return super().hset(name, key, value)
    async def smembers(self, name): return super().smembers(name)
    async def sadd(self, name, *values): return super().sadd(name, *values)
    async def srem(self, name, *values): return super().srem(name, *values)
    async def keys(self, pattern): return super().keys(pattern)
    async def exists(self, key): return super().exists(key)
    async def ping(self): return True

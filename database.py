import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)


class Database:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def get_client(self):
        pass

    def set_entry(self, key, value):
        return redis_client.hmset(key, value)

    def get_entry(self, key, member):
        return redis_client.hget(key, member).decode('utf-8')

    def delete_entry(self, key):
        return redis_client.delete(key)

    def is_user_exists(self, key):
        return redis_client.exists(key)

    def get_entry_all(self, key):
        return redis_client.hgetall(key)

    def set_geo_point(self, key, longitude, latitude, member):
        return redis_client.geoadd(key, longitude, latitude, member)

    def get_nearby_locations(self, key, longitude, latitude, dist, unit):
        return redis_client.georadius(key, longitude, latitude, dist, unit)



import hashlib
import requests

class DataUnchanged(Exception):
  pass

def always(*args, **kwargs):
  return True

def fetch_and_cache(url, redis_connection, cache_control=always):
  if not cache_control():
    raise DataUnchanged
  return redis_connection.set(hashlib.sha1(url).hexdigest(), requests.get(url).text)

def cached_fetch(url, redis_connection, cache_control=always):
  if not cache_control():
    raise DataUnchanged
  return redis_connection.get(hashlib.sha1(url).hexdigest())

import os
from celery import Celery
from redis import Redis
import celeryconfig
from config import Config
import parsers
from fetch import fetch_and_cache, cached_fetch
from destinations import write

redis = Redis(celeryconfig.REDIS_SERVER)

app = Celery('service_layer') # without this explicit name Celery will list the app as "__main__"
app.config_from_object(celeryconfig)

@app.task
def update_all(config_file):
  config = Config(config_file)
  for feed in config:
    print "destination: {destination}\nparser: {parser}\nurl: {url}\n\n".format(**feed)
    fetch_and_schedule.delay(feed)

@app.task
def parse_from_cache(feed):
  data = cached_fetch(feed.url, redis)
  parsed = getattr(parsers, feed.parser)(data)
  write(feed.destination, parsed)

@app.task
def fetch_and_schedule(feed):
  fetch_and_cache(feed.url, redis)
  parse_from_cache.delay(feed)


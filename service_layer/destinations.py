from __future__ import print_function
import os
import simplejson as json
import re
import boto
from service_layer.entrypoints import entrypoints

class UnknowScheme(Exception):
  pass

class UnrecognizedUri(Exception):
  pass

def write(uri, data):
  scheme_handler = get_scheme_handler(uri)
  if not isinstance(data, str):
    data = json.dumps(data)
  scheme_handler(uri, data)

def get_scheme_handler(uri):
  try:
    scheme = parse_uri(uri)['scheme']
  except (IndexError,):
    raise UnknowScheme
  else:
    if scheme not in scheme_handlers.keys():
      raise UnknowScheme
    else:
      return scheme_handlers[scheme]

def parse_uri(uri):
  try:
    match = pattern_uri.match(uri)
    groupdict = match.groupdict()
    groupdict.update({'subpath': groupdict['path'] + groupdict['basename']})
    return groupdict
  except (AttributeError,):
    raise UnrecognizedUri

def scheme_handler_s3(uri, data):
  parsed_uri = parse_uri(uri)
  s3 = boto.connect_s3()
  bucket = s3.get_bucket(parsed_uri['authority'])
  key = bucket.new_key(parsed_uri['path'] + parsed_uri['basename'])
  key.content_type = 'application/json'
  key.set_contents_from_string(data, policy='public-read')

def scheme_handler_file(uri, data):
  filepath = parse_uri(uri)['fullpath']
  filepath = os.path.join(entrypoints.config.destination_prefix, filepath)
  path = os.path.dirname(filepath)
  if not os.path.exists(path):
    os.makedirs(path)
  with open(filepath, 'w') as fh:
    fh.write(data)
  
pattern_uri = re.compile('^(?P<uri>(?P<scheme>\w+)://(?P<fullpath>(?P<dirname>(?P<authority>[^/]*)(?P<path>.*/))?(?P<basename>[^/]*)))')
scheme_handlers = {
  's3': scheme_handler_s3,
  'file': scheme_handler_file,
  'http': print, # this doesn't store anything at all. It just prints it to the console.
}

import os
import yaml
import celeryconfig
from const import *

"""
This is an example of the expected YAML format. The only required fields are
url, parser, destination. Any other field is optional and can only be access by
a dictionary key.

## config.yml
# One of the main reasons for choosing YAML over JSON is being able to use comments

# First Feed
-
  url: http://example.com
  parser: parser_example
  destination: file://www-example-com/index.html
  # I don't use s3 examples in the sample, but this is how you would do them
  # The first (domain-like) path component is the Bucket and the rest is the Key
  #destination: s3://www-example-com/index.html

# Second Feed
-
  category: Top News
  subcategory: Top News
  url: http://www.filltext.com/?rows=10&fname={firstName}&lname={lastName}&tel={phone|format}&address={streetAddress}&city={city}&state={usState|abbr}&zip={zip}
  parser: parser_example
  destination: file://www-example-com/index.html

# Third Feed
-
  category: News
  subcategory: Local
  url: http://beta.json-generator.com/api/json/get/FrBbyBY
  parser: parser_example
  destination: file://www-example-com/index.html

# Forth Feed
-
  category: News
  subcategory: Crime & Law
  url: http://www.json-generator.com/api/json/get/bSCtXmzOEO?indent=0
  parser: parser_example
  destination: file://www-example-com/index.html
"""

class ConfigDict(dict):
  pass

class Config(list):

  # required entries
  yaml = YAML
  destination_prefix = DESTINATION_PREFIX
  redis_server = REDIS_SERVER
  celeryconfig = celeryconfig

  def __init__(self):
    config_file = os.path.join(os.path.dirname(__file__), self.yaml)
    for entry in yaml.load(open(config_file, 'r')):
      self.append(ConfigDict(entry))
      # make attributes out of the required fields
      self[-1].url = self[-1]['url']
      self[-1].parser = self[-1]['parser']
      self[-1].destination = self[-1]['destination']

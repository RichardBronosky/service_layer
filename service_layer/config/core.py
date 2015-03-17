"""Defines the list derived Config class used to construct the config_object.

This is an example of the expected YAML format. The only required fields are
url, parser, destination. Any other field is optional and can only be access by
a dictionary key.

Example:

## config.yml
# One of the main reasons for choosing YAML over JSON is being able to use
# comments

# First Feed
-
  url: http://example.com
  parser: parser_example
  destination: file://example/index.html
  # I don't use s3 examples in the sample, but this is how you would do them
  # The 1st (domain-like) path component is the Bucket and the rest is the Key
  #destination: s3://www-example-com/index.html
"""

import os
import yaml
import celeryconfig
from const import YAML, DESTINATION_PREFIX, REDIS_SERVER


class ConfigDict(dict):

    """A direct subclass of dict."""

    pass


class Config(list):

    """A list of entries from the config YAML.

    Includes additional attribute constants. Each list item is a dictionary
    with 3 required fields accessible as attributes. Additional fields are only
    accessible as keys.
    """

    # required entries
    yaml = YAML
    destination_prefix = DESTINATION_PREFIX
    redis_server = REDIS_SERVER
    celeryconfig = celeryconfig

    def __init__(self):
        """Load the content of the config YAML."""
        config_file = os.path.join(os.path.dirname(__file__), self.yaml)
        for entry in yaml.load(open(config_file, 'r')):
            self.append(ConfigDict(entry))
            # make attributes out of the required fields
            self[-1].url = self[-1]['url']
            self[-1].parser = self[-1]['parser']
            self[-1].destination = self[-1]['destination']

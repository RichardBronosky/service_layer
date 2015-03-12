import pkg_resources
import config

"""
Usage: from service_layer.entrypoints import entrypoints

Returns an EntryPoints dictionary-like object

One of the design goals it to allow everything to be accessed by either key or
attribute. The values from plugin packages should always trump the defaults in
this package.

"""

class EntryPoints(dict):
  config = ()

  def add(self, name, value):
    self[name] = value
    setattr(self, name, self[name])

def _package_of(obj):
  return obj.__module__.split('.',1)[0]

entrypoints = EntryPoints()
_package = _package_of(entrypoints)

for ep in pkg_resources.iter_entry_points(group='service_layer_group_id'):
  name = ep.name
  value = ep.load()
  print "Handling " + name + " in " + value.__module__
  # add the entrypoint if it doesn't exist or the existing one is from this package
  if entrypoints.has_key(name) == False or _package_of(entrypoints[name]) == _package:
    entrypoints.add(name, value)


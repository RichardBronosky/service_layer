"""
A collection of parsers that should match those listed in the config YAML file.

Each parser must be added as an entrypoint. This allows MSL plugins that only
define parsers.
"""


def parser_example(data):
    """Manipulate incoming data and return the modified data."""
    return data

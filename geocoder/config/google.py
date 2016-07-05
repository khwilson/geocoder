"""
A little wrapper around a Google API key list.
"""
import io


class GoogleApiKeyReader(object):
    """A simple wrapper around a list of Google API keys """
    def __init__(self, filename):
        self.f = io.open(filename, 'r')

    def __enter__(self):
        return self.f.close()

    def __exit__(self, *args):
        self.f.close()

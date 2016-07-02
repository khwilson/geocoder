from os import path as _path


with open(_path.join(_path.dirname(__file__), 'VERSION'), 'r') as f:
    __version__ = f.read().strip()

"""
CSV compatibility between Python 2 and 3. Ganked from::

    http://python3porting.com/problems.html

but with added compatibility for gzipped csvs
"""
import codecs
import csv
import gzip
import sys


PY3 = sys.version_info > (3,)


class UnicodeCsvReader:
    def __init__(self, filename, dialect=csv.excel, encoding="utf-8", **kw):
        self.filename = filename
        self.dialect = dialect
        self.encoding = encoding
        self.kw = kw

    def __enter__(self):
        if PY3:
            if self.filename.endswith('.gz'):
                self.f = gzip.open(self.filename, 'rt')
                #reader = codecs.getreader('utf-8')(self.f)
                #self.reader = csv.reader(reader)
            else:
                self.f = open(self.filename, 'rt',
                              encoding=self.encoding, newline='')
        else:
            if self.filename.endswith('.gz'):
                self.f = gzip.open(self.filename)
            else:
                self.f = open(self.filename, 'rb')
        self.reader = csv.reader(self.f, dialect=self.dialect,
                                 **self.kw)
        return self

    def __exit__(self, type, value, traceback):
        self.f.close()

    def next(self):
        row = next(self.reader)
        if PY3:
            return row
        return [s.decode("utf-8") for s in row]

    __next__ = next

    def __iter__(self):
        return self

    def readrows(self):
        return list(self)


class UnicodeCsvWriter:
    def __init__(self, filename, dialect=csv.excel,
                 encoding="utf-8", **kw):
        self.filename = filename
        self.dialect = dialect
        self.encoding = encoding
        self.kw = kw

    def __enter__(self):
        if PY3:
            if self.filename.endswith('.gz'):
                self.f = gzip.open(self.filename, 'wt')
                #writer = codecs.getwriter('utf-8')(self.f)
                #self.writer = csv.writer(writer, dialect=self.dialect, **self.kw)
            else:
                self.f = open(self.filename, 'wt', encoding=self.encoding, newline='')
        else:
            if self.filename.endswith('.gz'):
                self.f = gzip.open(self.filename, 'wb')
            else:
                self.f = open(self.filename, 'wb')
        self.writer = csv.writer(self.f, dialect=self.dialect, **self.kw)
        return self

    def __exit__(self, type, value, traceback):
        self.f.close()

    def writerow(self, row):
        if not PY3:
            row = [s.encode(self.encoding) for s in row]
        self.writer.writerow(row)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

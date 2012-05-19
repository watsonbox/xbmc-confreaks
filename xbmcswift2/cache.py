'''
    xbmcswift2.cache
    ----------------

    This module contains persistent caching classes.

    :copyright: (c) 2012 by Jonathan Beluch
    :license: GPLv3, see LICENSE for more details.
'''
import os
import csv
import json
import time
import pickle
import shutil
import collections
from datetime import datetime
from xbmcswift2 import logger


class PersistentDictMixin(object):
    ''' Persistent dictionary with an API compatible with shelve and anydbm.

    The dict is kept in memory, so the dictionary operations run as fast as
    a regular dictionary.

    Write to disk is delayed until close or sync (similar to gdbm's fast mode).

    Input file format is automatically discovered.
    Output file format is selectable between pickle, json, and csv.
    All three serialization formats are backed by fast C implementations.
    '''

    def __init__(self, filename, flag='c', mode=None, file_format='pickle'):
        self.flag = flag                    # r=readonly, c=create, or n=new
        self.mode = mode                    # None or an octal triple like 0644
        self.file_format = file_format      # 'csv', 'json', or 'pickle'
        self.filename = filename
        if flag != 'n' and os.access(filename, os.R_OK):
            log.debug('Reading %s cache from disk at "%s"' % (self.file_format, self.filename))
            fileobj = open(filename, 'rb' if file_format == 'pickle' else 'r')
            with fileobj:
                self.load(fileobj)

    def sync(self):
        '''Write the dict to disk'''
        if self.flag == 'r':
            return
        filename = self.filename
        tempname = filename + '.tmp'
        fileobj = open(tempname, 'wb' if self.file_format == 'pickle' else 'w')
        try:
            self.dump(fileobj)
        except Exception:
            os.remove(tempname)
            raise
        finally:
            fileobj.close()
        shutil.move(tempname, self.filename)    # atomic commit
        if self.mode is not None:
            os.chmod(self.filename, self.mode)

    def close(self):
        '''Calls sync'''
        self.sync()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()

    def dump(self, fileobj):
        '''Handles the writing of the dict to the file object'''
        if self.file_format == 'csv':
            csv.writer(fileobj).writerows(self.raw_dict().items())
        elif self.file_format == 'json':
            json.dump(self.raw_dict(), fileobj, separators=(',', ':'))
        elif self.file_format == 'pickle':
            pickle.dump(dict(self.raw_dict()), fileobj, 2)
        else:
            raise NotImplementedError('Unknown format: ' +
                                      repr(self.file_format))

    def load(self, fileobj):
        '''Load the dict from the file object'''
        # try formats from most restrictive to least restrictive
        for loader in (pickle.load, json.load, csv.reader):
            fileobj.seek(0)
            try:
                return self.initial_update(loader(fileobj))
            except Exception as e:
                print e
                pass
        raise ValueError('File not in a supported format')

    def raw_dict(self):
        '''Returns the underlying dict'''
        raise NotImplementedError


class Cache(collections.MutableMapping, PersistentDictMixin):
    '''A dict with the ability to persist to disk'''

    def __init__(self, filename, file_format='pickle'):
        '''Acceptable formats are 'csv', 'json' and 'pickle'.'''
        self._items = {}
        PersistentDictMixin.__init__(self, filename, file_format=file_format)

    def __setitem__(self, key, val):
        self._items.__setitem__(key, val)

    def __getitem__(self, key):
        return self._items.__getitem__(key)

    def __delitem__(self, key):
        self._items.__delitem__(key)

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return self._items.__len__

    def raw_dict(self):
        '''Returns the wrapped dict'''
        return self._items

    initial_update = collections.MutableMapping.update


class TimedCache(Cache):
    '''A dict with the ability to persist to disk and ttl for items.'''

    def __init__(self, filename, file_format='pickle', ttl=None):
        '''ttl if provided should be a datetime.timedelta. Any entries
        older than the provided ttl will be removed upon load and upon item
        access.
        '''
        self.ttl = ttl
        Cache.__init__(self, filename, file_format=file_format)

    def __setitem__(self, key, val, raw=False):
        if raw:
            self._items[key] = val
        else:
            self._items[key] = (val, time.time())

    def __getitem__(self, key):
        val, timestamp = self._items[key]
        if self.ttl and (datetime.utcnow() -
            datetime.utcfromtimestamp(timestamp) > self.ttl):
            del self._items[key]
            return self._items[key][0]  # Will raise KeyError
        return val

    def initial_update(self, mapping):
        '''Initially fills the underlying dictionary with keys, values and
        timestamps.
        '''
        for key, val in mapping.items():
            _, timestamp = val
            if not self.ttl or (datetime.utcnow() -
                datetime.utcfromtimestamp(timestamp) < self.ttl):
                self.__setitem__(key, val, raw=True)

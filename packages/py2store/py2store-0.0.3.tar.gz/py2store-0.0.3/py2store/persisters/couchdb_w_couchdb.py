from py2store.base import Persister
from py2store.util import ModuleNotFoundErrorNiceMessage

with ModuleNotFoundErrorNiceMessage():
    from couchdb import Server


class CouchDbPersister(Persister):
    """
    A basic couchDB persister.
    Note that the couchDB persister is designed not to overwrite the value of a key if the key already exists.
    You can subclass it and use update_one instead of insert_one if you want to be able to overwrite data.

    >>> s = CouchDbPersister()
    >>> for _id in s:  # deleting all docs in tmp
    ...     del s[_id]
    >>> k = {'_id': 'foo'}
    >>> v = {'val': 'bar'}
    >>> k in s  # see that key is not in store (and testing __contains__)
    False
    >>> len(s)
    0
    >>> s[k] = v
    >>> len(s)
    1
    >>> list(s)
    [{'_id': 'foo'}]
    >>> s[k]
    {'val': 'bar'}
    >>> s.get(k)
    {'val': 'bar'}
    >>> s.get({'not': 'a key'}, {'default': 'val'})  # testing s.get with default
    {'default': 'val'}
    >>> list(s.values())
    [{'val': 'bar'}]
    >>> k in s  # testing __contains__ again
    True
    >>> del s[k]
    >>> len(s)
    0
    >>>
    >>> s = CouchDbPersister(db_name='py2store', key_fields=('name',), data_fields=('yob', 'proj', 'bdfl'))
    >>> for _id in s:  # deleting all docs in tmp
    ...     del s[_id]
    >>> s[{'name': 'guido'}] = {'yob': 1956, 'proj': 'python', 'bdfl': False}
    >>> s[{'name': 'vitalik'}] = {'yob': 1994, 'proj': 'ethereum', 'bdfl': True}
    >>> for key, val in s.items():
    ...     print(f"{key}: {val}")
    {'name': 'guido'}: {'yob': 1956, 'proj': 'python', 'bdfl': False}
    {'name': 'vitalik'}: {'yob': 1994, 'proj': 'ethereum', 'bdfl': True}
    """

    # CouchDb sets _id and _rev keys on documents and we need to keep them internally
    # we can't use user provided _id since couch expects string
    # to do that we replacing user provided _id and _rev during save and recover user values during retrieving
    ID_REPLACE = 'id_replace_autogenerated_JSI7R6CuWYH6k'
    REV_REPLACE = 'rev_replace_autogenerated_10fonAGPcRuZM'
    SPECIAL_KEYS = {'_id': ID_REPLACE, '_rev': REV_REPLACE}

    def clear(self):
        raise NotImplementedError(
            "clear is disabled by default, for your own protection! "
            "Loop and delete if you really want to."
        )

    def __init__(
            self,
            user='admin',
            password='admin',
            url='http://127.0.0.1:5984',
            db_name='py2store',
            key_fields=('_id',),
            couchdb_client_kwargs=None
    ):
        if couchdb_client_kwargs is None:
            couchdb_client_kwargs = {}
        if user and password:
            # put credentials in url if provided like https://username:password@example.com:5984/
            if '//' in url:  # if scheme present
                url = f'{url.split("//")[0]}//{user}:{password}@{url.split("//")[1]}'
            else:
                url = f'http//{user}:{password}@{url}'
        self._couchdb_server = Server(url=url, **couchdb_client_kwargs)
        self._db_name = db_name
        # if db not created
        if db_name not in self._couchdb_server:
            self._couchdb_server.create(db_name)
        self._cdb = self._couchdb_server[db_name]
        if isinstance(key_fields, str):
            key_fields = (key_fields,)

        self._key_fields = key_fields

    def __get_item_internal(self, k):
        # some methods need original couch docs, so __getitem__ is divided on two methods
        k = self.__replace_internals(k)
        mango_q = {
            'selector': k,
        }
        docs = self._cdb.find(mango_q)
        docs = list(docs)
        if docs:
            return docs[0]
        else:
            raise KeyError(f"No document found for query: {k}")

    def __getitem__(self, k):
        return self.__get_doc_filter(self.__get_item_internal(k))

    def __setitem__(self, k, v):
        doc = self.__replace_internals(dict(k, **v))
        # to override right one trying to get existed doc
        try:
            existed = self.__get_item_internal(k)
            for key in self.SPECIAL_KEYS:
                doc[key] = existed[key]
        except KeyError:
            pass
        return self._cdb.save(doc)

    def __delitem__(self, k):
        if len(k) > 0:
            doc = self.__get_item_internal(k)
            self._cdb.delete(doc)
        else:
            raise KeyError(f"You can't remove that key: {k}")

    def __iter__(self):
        mango_q = {
            'selector': {},
            'fields': self._key_fields + tuple(self.SPECIAL_KEYS.values())
        }
        yield from self._cdb.find(mango_q, self.__recover_internals)

    def __len__(self):
        return self._cdb.info()['doc_count']

    def __recover_internals(self, doc):
        # removing internal values and turn back user ones
        doc = dict(doc)
        for special_key in self.SPECIAL_KEYS:
            replace_key = self.SPECIAL_KEYS[special_key]
            if replace_key in doc:
                doc[special_key] = doc[replace_key]
                del doc[replace_key]
            elif special_key in doc:
                del doc[special_key]
        return doc

    def __replace_internals(self, doc):
        # moving user provided _id and _rev to predefined fields to keep values
        doc = dict(doc)
        for special_key in self.SPECIAL_KEYS:
            replace_key = self.SPECIAL_KEYS[special_key]
            if special_key in doc:
                doc[replace_key] = doc[special_key]
                del doc[special_key]
        return doc

    def __get_doc_filter(self, doc):
        # remove keys from doc
        doc = self.__recover_internals(doc)
        for key in self._key_fields:
            if key in doc:
                del doc[key]
        return doc

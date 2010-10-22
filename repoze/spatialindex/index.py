import os

from persistent import Persistent
from BTrees.IOBTree import IOBTree

from zope.interface import implements

from rtree import Rtree
from rtree.index import RT_Disk

from repoze.catalog.indexes.common import CatalogIndex
from repoze.catalog.interfaces import ICatalogIndex

class SpatialIndex(Persistent):

    def __init__(self, *args):
        self.rtree_args = args
        self.rtree = Rtree(*args)
        self.backward = IOBTree()

    def index_doc(self, docid, value):
        if docid in self.backward:
            self.unindex_doc(docid)
        self.backward[docid] = value
        self.rtree.add(docid, value, obj=docid)

    def unindex_doc(self, docid):
        value = self.backward.get(docid)
        if value is None:
            return
        self.rtree.delete(docid, value)
        del self.backward[docid]

    def apply(self, value):
        return [x.object for x in self.rtree.intersection(value, objects=True)]

    def clear(self):
        self.backward.clear()
        props = self.rtree.properties
        if props.storage == RT_Disk:
            self.rtree.close()
            fname = props.filename
            try:
                os.unlink('%s.%s' % (fname, props.dat_extension))
            except OSError:
                pass
            try:
                os.unlink('%s.%s' % (fname, props.idx_extension))
            except OSError:
                pass
        self.rtree = Rtree(*self.rtree_args)

    def count(self, value):
        return self.rtree.count(value)

class CatalogSpatialIndex(CatalogIndex, SpatialIndex):
    implements(ICatalogIndex)

    def __init__(self, discriminator, *rtree_args):
        CatalogIndex.__init__(self, discriminator)
        SpatialIndex.__init__(self, *rtree_args)

    def reindex_doc(self, docid, value):
        # the base index's index_doc method special-cases a reindex
        return self.index_doc(docid, value)
